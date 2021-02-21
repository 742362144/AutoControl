# coding=utf-8
import json
import os
import socket
import subprocess
import sys
import threading
import time
import traceback
from threading import Thread

import grpc
from json import dumps
from concurrent import futures

from auto import Model
from util.util import get_host_ip, get_docker0_IP, runCmd, runCmdAndGetOutput

sys.path.append('%s/' % os.path.dirname(os.path.realpath(__file__)))

from util import logger

import auto_pb2, auto_pb2_grpc

LOG = "/var/log/auto.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)

DEFAULT_PORT = '8090'

resource = {}


# group = {
#     'kind': 'group',
#     'data': {
#         'gid': 222,
#         'storage': [
#             {
#                 'cid':1,
#                 'cpu': 2
#             },
#             {
#                 'cid':2,
#                 'cpu': 2
#             }
#         ],
#         'compute': [
#             {
#                 'cid':2,
#                 'cpu': 2
#             }
#         ],
#     }
# }
#
# set = {
#     'kind': 'set',
#     'data': {
#         'group': 222,
#         'cid': 1,
#         'cpu': 2
#     }
# }
#
# get = {
#     'kind': 'get',
#     'data': {
#         'group': 222,
#         'cid': 1,
#         'cpu': 2
#     }
# }


def parse_group(cmd):
    print(cmd)
    gid = cmd['gid']
    resource[gid] = cmd
    #
    # group['storage'] = data['storage']
    # group['compute'] = data['compute']


# def parse_set(cmd):
#     gid = cmd['group']
#     print(1)
#     predict = None
#     if gid in resource.keys():
#         group = resource[gid]
#         cid = cmd['cid']
#         cpu = cmd['cpu']
#         if cid not in group.keys():
#             container = {'history': []}
#             group[cid] = container
#         else:
#             container = group[cid]
#         print(2)
#
#         # handle data
#         if len(container['history']) < 20:
#             print(2.1)
#             container['history'].extend(cpu)
#         elif len(container['history']) > 30:
#             print(2.2)
#             container['history'] = container['history'][1:].extend(cpu)
#
#         print(3)
#         # update model
#         print('container %s update model....' % cid)
#         if 'model' not in container.keys():
#             if len(container['history']) >= 20:
#                 container['model'] = get_model(container['history'])
#         else:
#             container['model'] = update_model(container['model'], cpu)
#
#         print(4)
#         if 'model' in container.keys():
#             predict = container['model'].forecast(1)
#         else:
#             print('not have enough data')
#         print(5)
#     else:
#         print('warning: unknown group!!!')
#     return predict

def parse_set(cmd):
    # print(resource)
    gid = cmd['group']
    predict = None
    if gid in resource.keys():
        group = resource[gid]
        cid = cmd['cid']
        cpu = cmd['cpu']

        container = group[cid]
        if 'history' not in container.keys():
            container['history'] = []

        # container['history'].extend(cpu)
        if len(container['history']) < 20:
            container['history'].extend(cpu)
        # elif len(container['history']) > 30:
        #     # print(2.2)
        #     container['history'] = container['history'][-20:].extend(cpu)

        # print('%s %s' % (cid, dumps(container['history'])))

        if 'model' not in container.keys():
            if len(container['history']) >= 10:
                container['model'] = Model(container['history'])
        else:
            print('container %s update model....' % cid)
            predict = container['model'].update_model(cpu)

        # # update model
        # if 'model' in container.keys():
        #     print(group.keys())
        #     predict = container['model'].forecast(1)
        #     print('container %s predict: %s' % (cid, predict))
        # else:
        #     print(len(container['history']))
    else:
        print('warning: unknown group!!!')
    # print('predict: %s' % predict)
    return predict


def parse_get(cmd):
    gid = cmd['group']
    if gid in resource.keys():
        group = resource[gid]
        cid = cmd['cid']
        cpu = cmd['cpu']
        if cid in group.keys():
            container = group[cid]
            container['history'].append(cpu)


def cmd_parser(cmd):
    cmd = json.loads(cmd)
    if cmd['kind'] == 'group':
        # print('parse group %s' % cmd)
        return parse_group(cmd)
    elif cmd['kind'] == 'set':
        # print('parse set %s' % cmd)
        return parse_set(cmd)
    elif cmd['kind'] == 'get':
        return parse_get(cmd)


class AutoControlServicer(auto_pb2_grpc.AutoControlServicer):
    def Submit(self, request, context):
        try:
            cmd = str(request.cmd)
            # print(request)
            predict = cmd_parser(cmd)
            if predict:
                print('predict: %s' % predict)
                res = dumps({'result': {'code': 0, 'msg': 'successful'}, 'data': {'predict': predict}})
            else:
                res = dumps({'result': {'code': 0, 'msg': 'successful'}, 'data': {}})
            return auto_pb2.Response(json=res)
        except Exception:
            print(traceback.format_exc())
            return auto_pb2.Response(json=dumps(
                {'result': {'code': 1, 'msg': 'rpc call kubesds-adm cmd failure %s' % traceback.format_exc()},
                 'data': {}}))


def run_server():
    # 多线程服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 实例化 计算len的类
    servicer = AutoControlServicer()
    # 注册本地服务,方法CmdCallServicer只有这个是变的
    auto_pb2_grpc.add_AutoControlServicer_to_server(servicer, server)
    # 监听端口
    logger.debug("%s:%s" % (get_docker0_IP(), DEFAULT_PORT))
    server.add_insecure_port("%s:%s" % (get_docker0_IP(), DEFAULT_PORT))
    # 开始接收请求进行服务
    server.start()

    return server
    # 使用 ctrl+c 可以退出服务
    # try:
    #     print("rpc server running...")
    #     time.sleep(1000)
    # except KeyboardInterrupt:
    #     print("rpc server stopping...")
    #     server.stop(0)


def keep_alive():
    server = run_server()
    server.wait_for_termination()


def stop():
    output = None
    try:
        output = runCmdAndGetOutput('ps -ef|grep kubesds-rpc-service')
    except Exception:
        logger.debug(traceback.format_exc())
    if output:
        lines = output.splitlines()
        if len(lines) <= 1:
            return
        else:
            pid = lines[0].split()[1]
            runCmd('kill -9 %s' % pid)


def daemonize():
    help_msg = 'Usage: python %s <start|stop|restart|status>' % sys.argv[0]
    if len(sys.argv) != 2:
        print(help_msg)
        sys.exit(1)
    pid_fn = '/var/run/kubesds-rpc.pid'
    log_fn = '/var/log/kubesds-rpc.log'
    err_fn = '/var/log/kubesds-rpc.log'
    if sys.argv[1] == 'start':
        keep_alive()
    elif sys.argv[1] == 'stop':
        stop()
    elif sys.argv[1] == 'restart':
        stop()
        keep_alive()
    else:
        print('invalid argument!')
        print(help_msg)


if __name__ == '__main__':
    daemonize()
