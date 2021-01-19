import configparser
import os
import time
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from configparser import ConfigParser
from json import loads
from threading import Thread

import grpc

from auto import get_container_stat, calculate_time, get_container_config
from util import logger

import auto_pb2
import auto_pb2_grpc

from util.util import get_docker0_IP

LOG = "/var/log/cmdrpc-cli.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)

DEFAULT_PORT = '19999'


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


def submit_group(group):
    # init group
    # group

    # submit stat
    while True:
        stat = get_container_stat(id)
        cpu_percent = calculate_time(stat)
        set = {
            'kind': 'set',
            'data': {
                'group': 222,
                'cid': 1,
                'cpu': [2]
            }
        }
        submit()


def get_all_group():
    CWD = os.getcwd()
    cfg = "%s/auto.conf" % CWD
    config_raw = configparser.ConfigParser()
    config_raw.read(cfg)
    groups = {}
    # ch = config_raw.sections()
    for g in config_raw['groups'].keys():
        # print()
        groups[g] = loads(config_raw.get('groups', g))

        # set origin cpu limit
        config = get_container_config('d1526144706d')
        limit = config['NanoCpus'] / 1000000000
    return groups


groups = get_all_group()

for gid in groups.keys():
    submit_group(groups[gid])






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
