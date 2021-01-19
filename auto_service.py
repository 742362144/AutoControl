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

from auto import get_model, update_model
from util.util import get_host_ip, get_docker0_IP, runCmd, runCmdAndGetOutput

sys.path.append('%s/' % os.path.dirname(os.path.realpath(__file__)))

from util import logger

import auto_pb2, auto_pb2_grpc

LOG = "/var/log/kubesds-rpc.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)

DEFAULT_PORT = '19999'

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
    data = cmd['data']
    gid = data['gid']
    group = {}
    resource[gid] = group
    for c in data['storage']:
        cid = c['cid']
        cpu = c['cpu']
        container = {'cpu': cpu, 'kind': 'storage'}
        group[cid] = container

    for c in data['compute']:
        cid = c['cid']
        cpu = c['cpu']
        container = {'cpu': cpu, 'kind': 'compute'}
        group[cid] = container
    #
    # group['storage'] = data['storage']
    # group['compute'] = data['compute']


def parse_set(cmd):
    data = cmd['data']
    gid = data['group']
    if gid in resource.keys():
        group = resource[gid]
        cid = data['cid']
        cpu = data['cpu']
        if cid not in group.keys():
            container = {'history': []}
            group[cid] = container
        else:
            container = group[cid]

        # handle data
        if len(container['history']) < 20:
            container['history'].extend(cpu)
        else:
            container['history'] = container['history'][1:].extend(cpu)

        # update model
        if 'model' not in container.keys():
            if len(container['history']) == 20:
                container['model'] = get_model(container['history'])
        else:
            container['model'] = update_model(container['model'], cpu)

        predict = None
        if 'model' in container.keys():
            predict = container['model'].forecast(1)

        return predict



def parse_get(cmd):
    data = cmd['data']
    gid = data['group']
    if gid in resource.keys():
        group = resource[gid]
        cid = data['cid']
        cpu = data['cpu']
        if cid in group.keys():
            container = group[cid]
            container['history'].append(cpu)



def cmdParser(cmd):
    cmd = json.loads(cmd)
    if cmd['kind'] == 'group':
        parse_group(cmd)
    elif cmd['kind'] == 'set':
        parse_set(cmd)
    elif cmd['kind'] == 'get':
        parse_get(cmd)


class AutoControlServicer(auto_pb2_grpc.AutoControlServicer):
    def Submit(self, request, context):
        try:
            cmd = str(request.cmd)
            logger.debug(cmd)
            op = runCmd(cmd)
            op.execute()

            logger.debug(request)
            return auto_pb2.Response(
                json=dumps({'result': {'code': 0, 'msg': 'rpc call kubesds-adm cmd %s successful.' % cmd}, 'data': {}}))
        except Exception:
            logger.debug(traceback.format_exc())
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
