# start redis docker container
# docker pull uluyol/ycsb:0.8.0-dev-12

# docker network create net1
#
# docker run run -itd  --name redis-test  --net net1 redis
#
# docker run -itd  --name ycsb-test  --net net1 centos:7.6.1810
#
# docker cp /root/ycsb-redis d1526144706d:/root/
#
# docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-test
# docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ycsb-test
#
# yum install java-1.8.0-openjdk -y
# cd /root/ycsb-redis
# ./bin/ycsb load redis -s -P workloads/workloada -p "redis.host=172.18.0.2" -p "redis.port=6379"
#
# docker commit d1526144706d ycsb-redis:1.0
# docker save -o ycsb-redis.img ycsb-redis:1.0
import docker


# api https://docker-py.readthedocs.io/en/stable/containers.html
def update_container():
    client = docker.DockerClient(base_url='unix:///var/run/docker.sock')
    for c in client.containers.list():
        if c.id.find(id) == 0:
            # cpu = c.stats(stream=False)
            c.update(blkio_weight=1, cpu_period=1, cpu_quota=1, cpu_shares=1, cpuset_cpus='', cpuset_mems='',
                     mem_reservation=1, memswap_limit=1, kernel_memory=1, restart_policy=dict)
            # c.update(blkio_weight=1, cpu_period=1, cpu_quota=1, cpu_shares=1, cpuset_cpus='', cpuset_mems='',
            #          mem_reservation=1, memswap_limit=1, kernel_memory=1, restart_policy=dict)
            # return cpu['cpu_stats']

