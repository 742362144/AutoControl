# pip install statsmodels==v0.12.1
import datetime
import json
import os
import time

import docker
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import multiprocessing as mp

# pip install py-cpuinfo
# https://stackoverflow.com/questions/4842448/getting-processor-information-in-python
import cpuinfo
from util.util import runCmdAndGetOutput
from util import logger


LOG = "/var/log/auto.log"

logger = logger.set_logger(os.path.basename(__file__), LOG)


def get_model(data):
    original_observations = pd.Series(data)
    mod = sm.tsa.SARIMAX(original_observations)
    res = mod.fit()
    return res


class Model(object):
    def __init__(self, data):
        self.lock = mp.Lock()
        self.model = get_model(data)

    def update_model(self, data):
        # new_observations = pd.Series(data, index=index+1)
        # print(new_observations)
        logger.debug('appending data')
        # self.lock.acquire()
        updated_res = self.model.append(data, refit=True)
        # updated_res = self.model.append(data)
        # self.lock.release()
        logger.debug('finish append data')
        # print(updated_res.params)
        # print('-------------------')
        # print(updated_res.fittedvalues)
        # print('-------------------')
        # print(updated_res.forecast(1))
        predict = updated_res.forecast(1)
        self.model = updated_res
        return predict.tolist()[0]

def get_container_stat(id):
    # print('get_container_stat: id %s' % id)
    # print('get_container_stat: id %s' % type(id))
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    for c in client.containers.list():
        if c.id.find(id) == 0:
            cpu = c.stats(stream=False)
            return cpu


def get_container_stats_stream(id):
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    for c in client.containers.list():
        if c.id.find(id) == 0:
            return c.stats(stream=True, decode=True)


def parallel_container_stat():
    import multiprocessing as mp
    output = mp.Queue()

    lock = mp.Lock()

    def stats(server, lock):
        client = docker.from_env()
        client_lowlevel = docker.APIClient(base_url='unix://var/run/docker.sock')
        client_stats = client_lowlevel.stats(container=server, stream=False)
        output.put(client_stats)

    processes = [mp.Process(target=stats, args=(server, lock)) for server in ('d1526144706d', '2b02193ba7dd')]

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    print(output.get())
    print(output.get())


# def test(id):
#     client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
#     for c in client.containers.list():
#         if c.id.find(id) == 0:
#             for i in c.stats(stream=True):
#                 print(i)


def get_time(utc):
    utc = utc[:-4] + 'Z'
    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    utcTime = datetime.datetime.strptime(utc, UTC_FORMAT)
    return utcTime


def calculate_time(d):
    now = get_time(d['read'])
    last = get_time(d['preread'])

    return (now - last).total_seconds()


def calculate_cpu_percent(d):
    cpu_count = len(d["cpu_stats"]["cpu_usage"]["percpu_usage"])
    cpu_percent = 0.0
    cpu_delta = float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
                float(d["precpu_stats"]["cpu_usage"]["total_usage"])
    system_delta = float(d["cpu_stats"]["system_cpu_usage"]) - \
                   float(d["precpu_stats"]["system_cpu_usage"])
    if system_delta > 0.0:
        cpu_percent = cpu_delta / system_delta * 100.0 * cpu_count
    return cpu_percent


def get_container_config(id):
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    # for c in client.containers.list():
    #     if c.id.find(id) == 0:
    #         print(json.dumps(c.attrs))

    return client.api.inspect_container(id)['HostConfig']


# def get_container_config(id):
#     output = runCmdAndGetOutput('docker inspect %s' % id)
#     print(output)
#     config = json.loads(output)[0]
#     HostConfig = config['HostConfig']
#     print(json.dumps(HostConfig))

# api https://docker-py.readthedocs.io/en/stable/containers.html
def update_container(cid, target, MAX_CPU=None):
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    if MAX_CPU and target <= MAX_CPU:
        client.api.update_container(container=cid, cpu_quota=int(target * 1000000000))
    # for c in client.containers.list():
    #     if c.id.find(id) == 0:
    #         # cpu = c.stats(stream=False)
    #         c.update(blkio_weight=1, cpu_period=1, cpu_quota=1, cpu_shares=1, cpuset_cpus='', cpuset_mems='',
    #                  mem_reservation=1, memswap_limit=1, kernel_memory=1, restart_policy=dict)
    #         # c.update(blkio_weight=1, cpu_period=1, cpu_quota=1, cpu_shares=1, cpuset_cpus='', cpuset_mems='',
    #         #          mem_reservation=1, memswap_limit=1, kernel_memory=1, restart_policy=dict)
    #         # return cpu['cpu_stats']


def get_cpu_speed():
    # print( cpuinfo.get_cpu_info())
    # print(cpuinfo.get_cpu_info()['brand_raw'])  # get only the brand name
    cpu = cpuinfo.get_cpu_info()['brand_raw']
    return float(cpu.strip().split()[-1].replace('GHz', '')) * 1000000000


def get_all_container():
    res = []
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    for c in client.containers.list():
        res.append(c.short_id)
    return res

# parallel_container_stat()

# print(get_all_container())

# data = get_container_stat('2b02193ba7dd')
#
# print(calculate_cpu_percent(data))

# data = []
# with open('test.txt', 'r') as f:
#     strs = json.load(f)
#     for s in strs:
#         data.append(float(s))

# d1 = pd.Series(data[:100])

# res = get_model(d1)
# index = d1.index
# for i in range(50):
#     update = data[100+i*2: 100+(i+1)*2]
#     res = update_model(res, update, index)
#     index = index + len(update) + 1
#     print(res.forecast(1).tolist()[0])
