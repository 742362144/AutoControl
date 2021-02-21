import json

import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')
import numpy as np


def diff():
    x = np.linspace(0, 10, 50)
    dy = 0.8
    y = np.sin(x) + dy * np.random.randn(50)

    # 误差线
    plt.errorbar(x, y, yerr=dy, fmt='.k')
    plt.show()


# ----------------predict------------------------
def predict():
    with open('usage.txt', 'r') as f:
        usage = json.load(f)
    with open('predict.txt', 'r') as f:
        predict = json.load(f)
    plt.plot(usage[30:115])
    plt.plot(predict[30:115])
    plt.show()


predict()
