import re
import socket
import subprocess
import traceback
from json import dumps

import psutil


# 获取网卡名称和其ip地址，不包括回环
def get_docker0_IP():
    info = psutil.net_if_addrs()
    for k, v in info.items():
        for item in v:
            if k == 'docker0' and re.match(
                    '^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$', item[1]):
                return item[1]

    return None


def get_host_ip():
    return socket.gethostbyname(socket.gethostname())


def runCmd(cmd):
    print(cmd)
    if not cmd:
        #         logger.debug('No CMD to execute.')
        return
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        msg = ''
        if std_out:
            for index, line in enumerate(std_out):
                if not str.strip(line.decode("utf-8")):
                    continue
                if index == len(std_out) - 1:
                    line = str.strip(line.decode("utf-8")) + '. '
                    msg = msg + line
                else:
                    line = str.strip(line.decode("utf-8")) + ', '
                    msg = msg + line
                print(line)

        p.wait()

        if std_err:
            error_msg = ''
            for index, line in enumerate(std_err):
                error_msg = error_msg + line.decode("utf-8")
            if error_msg.strip() != '' and p.returncode != 0:
                print(error_msg)
                raise Exception
        return msg
    finally:
        p.stdout.close()
        p.stderr.close()


def runCmdAndGetOutput(cmd):
    print(cmd)
    if not cmd:
        return

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        std_out = p.stdout.readlines()
        std_err = p.stderr.readlines()
        if std_out:
            msg = ''
            for line in std_out:
                msg = msg + line.decode("utf-8")
                print(line.decode("utf-8"))
            return msg
        if std_err:
            traceback.print_exc()
            error_msg = ''
            for index, line in enumerate(std_err):
                if not str.strip(line.decode("utf-8")):
                    continue
                else:
                    line = str.strip(line.decode("utf-8")) + ', '
                    error_msg = error_msg + line
            if error_msg.strip() != '':
                print(error_msg)
                raise Exception()
    except Exception:
        traceback.print_exc()
    finally:
        p.stdout.close()
        p.stderr.close()


def success_print(msg, data):
    return dumps({"result": {"code": 0, "msg": msg}, "data": data})


def error_print(code, msg, data=None):
    if data is None:
        return dumps({"result": {"code": code, "msg": msg}, "data": {}})
    else:
        return dumps({"result": {"code": code, "msg": msg}, "data": data})
