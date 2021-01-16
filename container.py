import subprocess

import docker
import json
from util.util import calculate_cpu_percent


# client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
# for i in client.containers.list():
#      # print(i.stats(stream=False)['id'])
#      for stat in i.stats():
#           print(type(stat))
#           d = json.loads(stat)
#           print(d)
#           print(calculate_cpu_percent(d))

time = 10000
def runCmd(cmd):
    res = []
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout
        std_err = p.stderr
        if std_out:
            msg = ''
            total = 0
            for line in std_out:
                if total >= time:
                    with open('test.txt', 'w') as f:
                        json.dump(res, f)
                    return
                cpu = str(line).split()[2].replace('%', '')
                if cpu != 'NAME':
                    print(cpu)
                    res.append(cpu)
                    total = total + 1
            return msg
        if std_err:
            raise Exception('RunCmdError')
    finally:
        p.stdout.close()
        p.stderr.close()

runCmd('docker stats de4abadcf4f927c0f86f26c60120fda8ad1552a5bf635524d9ea3701a7dcc55f')