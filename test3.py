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

client = docker.from_env()
client_lowlevel = docker.APIClient(base_url='unix://var/run/docker.sock')
client_stats = client_lowlevel.stats(container='09780b44a317', stream=False)
print(json.dumps(client_stats))