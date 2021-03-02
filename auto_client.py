import configparser
import os
import time
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from configparser import ConfigParser
from json import loads, dumps
from threading import Thread

import docker
import grpc

from auto import get_container_stat, calculate_time, get_container_config, get_all_container, calculate_cpu_percent, \
    get_container_stats_stream, update_container
from util import logger

import auto_pb2
import auto_pb2_grpc

from util.util import get_docker0_IP

LOG = "/var/log/auto.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)

DEFAULT_PORT = '8090'


def submit(cmd):
    logger.debug(cmd)
    try:
        host = get_docker0_IP()
        channel = grpc.insecure_channel("{0}:{1}".format(host, DEFAULT_PORT))
        client = auto_pb2_grpc.AutoControlStub(channel)
        # ideally, you should have try catch block here too
        response = client.Submit(auto_pb2.Request(cmd=cmd))
        result = loads(str(response.json))
        return result
    except grpc.RpcError as e:
        logger.debug(traceback.format_exc())
        # ouch!
        # lets print the gRPC error message
        # which is "Length of `Name` cannot be more than 10 characters"
        logger.debug(e.details())
        # lets access the error code, which is `INVALID_ARGUMENT`
        # `type` of `status_code` is `grpc.StatusCode`
        status_code = e.code()
        # should print `INVALID_ARGUMENT`
        logger.debug(status_code.name)
        # should print `(3, 'invalid argument')`
        logger.debug(status_code.value)
        # want to do some specific action based on the error?
        if grpc.StatusCode.INVALID_ARGUMENT == status_code:
            # do your stuff here
            pass
    except Exception:
        logger.debug(traceback.format_exc())


# set = {
#     'kind': 'set',
#     'data': {
#         'group': 222,
#         'cid': 1,
#         'cpu': [2]
#     }
# }
#
# group = {
#     'kind': 'group',
#     'data': {
#         'gid': 222,
#         'storage': [
#             {
#                 'cid': 1,
#                 'cpu': 2
#             },
#             {
#                 'cid': 2,
#                 'cpu': 2
#             }
#         ],
#         'compute': [
#             {
#                 'cid': 2,
#                 'cpu': 2
#             }
#         ],
#     }
# }


def submit_group():
    groups = get_all_group()
    for gid in groups.keys():
        submit(dumps(groups[gid]))
    return groups


def get_all_group():
    CWD = os.getcwd()
    cfg = "%s/auto.conf" % CWD
    config_raw = configparser.ConfigParser()
    config_raw.read(cfg)
    groups = {}
    # ch = config_raw.sections()
    cons = get_all_container()
    for gid in config_raw['groups'].keys():
        # print()
        g_config = loads(config_raw.get('groups', gid))
        config_storage = g_config['storage']
        config_compute = g_config['compute']
        print(g_config)
        # set origin cpu limit
        group = {
            'kind': 'group',
            'gid': gid
        }
        for cid in config_storage:
            if cid in cons:
                config = get_container_config(cid)
                limit = config['NanoCpus'] / 1000000000
                group[cid] = {
                    'kind': 'storage',
                    'limit': limit
                }

        for cid in config_compute:
            if cid in cons:
                config = get_container_config(cid)
                limit = config['NanoCpus'] / 1000000000
                group[cid] = {
                    'kind': 'compute',
                    'limit': limit
                }
        groups[gid] = group
    return groups


def parallel_submit(group):
    import multiprocessing as mp

    lock = mp.Lock()
    gid = group['gid']

    def stats(group, cid, lock):
        MAX_CPU = group[cid]['limit']
        stream = get_container_stats_stream(cid)

        count = 0
        usage = []
        predict = []
        for stat in stream:
            # print(stat)
            # print(type(stat))
            u, p = submit_container(gid, cid, stat, MAX_CPU)
            usage.append(u)
            predict.append(p)
            count = count + 1
            if count > 2000:
                print('container: %s' % cid)
                with open('usage.txt', 'w') as f:
                    f.write(dumps(usage))
                with open('predict.txt', 'w') as f:
                    f.write(dumps(predict))
                return

    processes = []
    for cid in group.keys():
        if cid in ['gid', 'kind']:
            pass
        processes.append(mp.Process(target=stats, args=(group, cid, lock)))

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()


def submit_container(gid, cid, stat, MAX_CPU):
    set = {
        'kind': 'set',
        'group': gid,
        'cid': cid
    }
    predict = None
    cpu = []
    set['cpu'] = cpu
    usage = None
    try:
        usage = calculate_cpu_percent(stat)
        # print(usage)
        cpu.append(usage)
    except Exception:
        traceback.print_exc()
    if usage is None:
        print('error: %s' % dumps(stat))
    else:
        try:
            res = submit(dumps(set))
            # print(res)
            if 'predict' in res['data'].keys():
                predict = res['data']['predict']
                print('predict: %s' % predict)
                print('usage: %s' % usage)
                update_container(cid, predict, MAX_CPU)

        except Exception:
            traceback.print_exc()
    return usage, predict


def run_service():
    groups = submit_group()
    for gid in groups.keys():
        print('start subbmit group %s' % gid)
        parallel_submit(groups[gid])

    while True:
        time.sleep(5)


run_service()

# print(get_all_group())

# with ThreadPoolExecutor(max_workers=10) as executor:
#     groups = {}
#     threads = {}
#     while True:
#         current_groups = get_all_group()
#         for gid in current_groups.keys():
#             if gid not in groups.keys():
#                 group = {}
#                 # thread = Thread(target=submit(group))
#                 # thread.daemon = True
#                 # thread.name = 'group'
#                 # thread.start()
#         time.sleep(5)
