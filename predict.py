import numpy as np, pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

plt.rcParams.update({'figure.figsize': (9, 7), 'figure.dpi': 120})

# Import data
df = pd.read_csv('usage.csv', names=['value'], header=0)
# print(type(df.value))
df.value = df.value / 2 - 20
# print(df.values.tolist())

cpu_usage = df.value

from statsmodels.tsa.arima_model import ARIMA

# 1,1,2 ARIMA Model
model = ARIMA(cpu_usage, order=(1, 1, 2))
model_fit = model.fit(disp=0)
# print(model_fit.summary())

# 1,1,1 ARIMA Model
model = ARIMA(cpu_usage, order=(1, 1, 1))
model.fit(disp=0)
res = model.predict(cpu_usage)
print(cpu_usage)
print(res)
# Plot residual errors
# residuals = pd.DataFrame(model_fit.resid)
# fig, ax = plt.subplots(1,2)
# print ax[0]
# print ax[1]
# residuals.plot(title="Residuals", ax=ax[0])
# residuals.plot(kind='kde', title='Density', ax=ax[1])
# plt.show()

# Actual vs Fitted
plt = model_fit.plot_predict()
# model_fit.plot_predict(dynamic=False)

ax = plt.gca()
line = ax.lines[0]
print(line.get_xdata().tolist())
print(line.get_ydata().tolist())

line = ax.lines[1]
print(line.get_xdata().tolist())
print(line.get_ydata().tolist())
plt.show()
