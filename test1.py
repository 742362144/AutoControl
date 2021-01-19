# pip install statsmodels==v0.12.1
import json

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

# index = pd.period_range(start='2000', periods=2, freq='A')
data = []
with open('test.txt', 'r') as f:
    strs = json.load(f)
    for s in strs:
        data.append(float(s))

data = pd.Series(data)


original_observations = data[:9000]
mod = sm.tsa.SARIMAX(original_observations)
res = mod.fit()
print(res.params)
print('-------------------')
print(res.fittedvalues)
print('-------------------')
print(res.forecast(1))
print('-------------------')
# print(original_observations)
#
# exit(0)
ori = []
pre = []
diff = []
for i in range(9700, 9900, 2):
    new_observations = data[i: i+2]
    # print(new_observations)
    updated_res = res.append(new_observations.tolist())
    print(updated_res.params)
    print('-------------------')
    print(updated_res.fittedvalues)
    print('-------------------')
    print(updated_res.forecast(1))
    res = updated_res
    ori.append(data[i+2].tolist())
    p = updated_res.forecast(1).tolist()[0]
    pre.append(round(p, 2))

    d = abs(ori[-1] - pre[-1])
    diff.append(d)

print(ori)
plt.plot(ori)
print(pre)
plt.plot(pre)
# print(diff)
# plt.plot(diff)
plt.show()