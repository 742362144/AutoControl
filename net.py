import os
import subprocess

import docker
import json
import time
import traceback
import matplotlib.pyplot as plt

from util.util import runCmd, runCmdAndGetOutput

TOTAL_MEM_USAGE = 64 * 1024 * 1024
data_size = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]


def idle():
    times = 100
    cid = start_redis()
    print('cid: %s' % cid)
    old = get_container_stat(cid)
    print('old: %s' % old)
    time.sleep(times)
    now = get_container_stat(cid)
    print('now: %s' % now)
    return (now - old) / times


YCSB_DIR = '/root/ycsb-redis'


def load_ycsb(workload):
    # load data
    runCmd(
        '%s/bin/ycsb load redis -s -P %s -p "redis.host=127.0.0.1" -p "redis.port=6379"' % (
            YCSB_DIR, workload))


def run_ycsb(workload):
    # run
    output = runCmdAndGetOutput(
        '%s/bin/ycsb run redis -s -P %s -p "redis.host=127.0.0.1" -p "redis.port=6379"' % (
            YCSB_DIR, workload))
    print(output)


def set_data_size(workload, dsize):
    fieldlength = runCmdAndGetOutput("cat %s | grep fieldlength" % workload).strip().split('=')
    fieldcount = runCmdAndGetOutput("cat %s | grep fieldcount" % workload).strip().split('=')
    recordcount = runCmdAndGetOutput("cat %s | grep recordcount" % workload).strip().split('=')
    fieldlength = fieldlength[-1]
    fieldcount = fieldcount[-1]
    recordcount = recordcount[-1]
    # print(fieldlength)
    # print(fieldcount)
    # print(recordcount)

    n_fieldcount = str(int(dsize / int(fieldlength)))
    n_recordcount = str(int(TOTAL_MEM_USAGE / dsize))
    print('start test datasize : %d' % dsize)
    runCmd("sed -i 's#fieldcount=%s#fieldcount=%s#g' %s " % (fieldcount, n_fieldcount, workload))
    runCmd("sed -i 's#recordcount=%s#recordcount=%s#g' %s " % (recordcount, n_recordcount, workload))

    print('start load data...., datasize %d, datacount: %s, operationcount: %d' % (dsize, n_recordcount, 500000))


def bench():
    res = {}
    CWD = os.getcwd()
    WORKLOADS_DIR = '%s/workloads' % CWD
    WORKLOAD = '%s/read' % WORKLOADS_DIR
    for i in data_size:
        set_data_size(WORKLOAD, i)
        cid = start_redis()
        load_ycsb(WORKLOAD)
        print('finish load data....')
        time.sleep(100)
        old = get_container_stat(cid)
        print('start run test....')
        run_ycsb(WORKLOAD)
        now = get_container_stat(cid)
        print('finish run test....')
        # print(json.dumps(old))
        # print(json.dumps(now))
        # print('cpu_total: %s' % (str(now['cpu_usage']['total_usage'] - old['cpu_usage']['total_usage'])))
        case = []
        case.append(old)
        case.append(now)
        res[i] = case
        print(json.dumps(res))
        stop_redis()
    with open('net.txt', 'w') as f:
        json.dump(json.dumps(res), f)


def get_container_id():
    return runCmdAndGetOutput("docker ps -a | grep redis-bench | awk  '{print $1}'")

# docker run -d --name redis-bench -p 6379:6379 redis
def start_redis():
    cid = get_container_id()
    if cid:
        runCmd('docker start %s' % cid)
    else:
        cid = runCmdAndGetOutput('docker run -itd --name redis-bench -p 6379:6379 redis')

    return cid.strip()


def stop_redis():
    runCmd('docker stop redis-bench')
    runCmd('docker rm -f redis-bench')
    # cid = runCmdAndGetOutput("docker ps | grep redis | awk  '{print $1}'")


def get_container_stat(id):
    # print('get_container_stat: id %s' % id)
    # print('get_container_stat: id %s' % type(id))
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    for c in client.containers.list():
        if c.id.find(id) == 0:
            cpu = c.stats(stream=False)
            return cpu

        # print(i.stats(stream=False))
        # for stat in i.stats():
        #      print(type(stat))
        #      d = json.loads(stat)
        #      print(d)
        #      print(calculate_cpu_percent(d))


# print(get_container_stat('d6412d090ae6'))
# print(idle())
stop_redis()
bench()

# set_data_size('/tmp/AutoControl/workloads/read', 16)


#
def collect():
    res = []
    with open('net.txt', 'r') as f:
        print(os.listdir())
        data = json.load(f)
        for key in data.keys():
            old = float(data[key][0]['precpu_stats']['cpu_usage']['total_usage'])
            now = float(data[key][1]["cpu_stats"]['cpu_usage']['total_usage'])

            # float(d["cpu_stats"]["cpu_usage"]["total_usage"]) - \
            # float(d["precpu_stats"]["cpu_usage"]["total_usage"])

            # print(now)
            # print(old)
            res.append(now - old)
    plt.plot(res)
    plt.show()
    print(json.dumps(res))

# collect()
