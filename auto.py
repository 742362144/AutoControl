import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#data = sm.datasets.co2.load_pandas()
#y = data.data

# y = df
# y.drop(y.columns.difference(['delay']), 1, inplace=True)
#
# # The 'MS' string groups the data in buckets by start of the month
# y = y['delay'].resample("4H", how="mean")
#
# # The term bfill means that we use the value before filling in missing values
# y = y.fillna(y.bfill())

y = [10930, 10318, 10595, 10972, 7706, 6756, 9092, 10551, 9722, 10913, 11151, 8186, 6422,
       6337, 11649, 11652, 10310, 12043, 7937, 6476, 9662, 9570, 9981, 9331]

y.extend(y)
y.extend(y)

y = pd.Series(y)
# y.index = pd.Index(sm.tsa.datetools.dates_from_range('1996', '2019'))

print(y)

y.plot(figsize=(15, 6))
plt.show()

# Define the p, d and q parameters to take any value between 0 and 2
p = d = q = range(0, 2)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

warnings.filterwarnings("ignore") # specify to ignore warning messages

for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit()

            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
        except:
            continue

# mod = sm.tsa.statespace.SARIMAX(y,
#                                 order=(1, 1, 1),
#                                 seasonal_order=(1, 1, 1, 12),
#                                 enforce_stationarity=False,
#                                 enforce_invertibility=False)
#
# results = mod.fit()
#
# print(results.summary().tables[1])
#
# results.plot_diagnostics(figsize=(15, 12))
# plt.show()
# pred = results.get_prediction(start=pd.to_datetime('2016-11-20 00:00:00'), dynamic=False)
# pred_ci = pred.conf_int()
#
# ax = y['2016-10-30 04:00:00':].plot(label='observed')
# pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)
#
# ax.set_xlabel('Date')
# ax.set_ylabel('Delays')
# plt.legend()
#
# plt.show()
#
# y_forecasted = pred.predicted_mean
# y_truth = y['2016-11-20 00:00:00':]
#
# # Compute the mean square error
# mse = ((y_forecasted - y_truth) ** 2).mean()
# print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
#
# pred_dynamic = results.get_prediction(start=pd.to_datetime('2016-11-20 00:00:00'), dynamic=True, full_results=True)
# pred_dynamic_ci = pred_dynamic.conf_int()
#
# ax = y['2016-10-30 04:00:00':].plot(label='observed', figsize=(20, 15))
# pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)
#
# ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('2016-11-20 00:00:00'), y.index[-1],
#                  alpha=.1, zorder=-1)
#
# ax.set_xlabel('Date')
# ax.set_ylabel('Delays')
#
# plt.legend()
# plt.show()
#
# y_forecasted = pred_dynamic.predicted_mean
# y_truth = y['2016-11-20 00:00:00':]
#
# # Compute the mean square error
# mse = ((y_forecasted - y_truth) ** 2).mean()
# print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
#
# # Get forecast 500 steps ahead in future
# pred_uc = results.get_forecast(steps=32)
#
# # Get confidence intervals of forecasts
# pred_ci = pred_uc.conf_int()
# print(pred_ci.iloc[:, 1])
#
# ax = y.plot(label='observed', figsize=(20, 15))
# pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
# ax.fill_between(pred_ci.index,
#                 pred_ci.iloc[:, 0],
#                 pred_ci.iloc[:, 1], color='k', alpha=.25)
# ax.set_xlabel('Date')
# ax.set_ylabel('Delays')
#
# plt.legend()
# plt.show()


