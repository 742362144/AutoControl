import pandas as pd
import statsmodels.api as sm

from statsmodels.graphics.tsaplots import plot_acf
import matplotlib.pyplot as plt


dta = [10930, 10318, 10595, 10972, 7706, 6756, 9092, 10551, 9722, 10913, 11151, 8186, 6422,
       6337, 11649, 11652, 10310, 12043, 7937, 6476, 9662, 9570, 9981, 9331]
dta = pd.Series(dta)
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('1996', '2019'))


plt.plot(dta)
plt.show()
plt.close()
plot_acf(dta).show()

diff1 = dta.diff(1).dropna()
diff1.columns = [u'diff']
# diff1.plot()

plt.plot(diff1)
# plt.show()
# plt.close()

from statsmodels.stats.diagnostic import acorr_ljungbox
print('white noise: ', acorr_ljungbox( diff1, lags=1))


from statsmodels.graphics.tsaplots import plot_acf
plot_acf(diff1).show()

from statsmodels.graphics.tsaplots import plot_pacf
plot_pacf(dta).show()


from statsmodels.tsa.arima_model import ARIMA
model = ARIMA(diff1, (0,1,1)).fit()
model.summary2()

print(model.forecast(5))
