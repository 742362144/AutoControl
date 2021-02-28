from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import PolynomialFeatures


x = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288,
      1048576, 2097152, 4194304, 8388608, 16777216]
y = [754326, 816252, 702338, 713058, 707751, 681619, 700898, 690466, 702017, 825832, 822247, 874179, 727937, 752400,
      760544, 816799, 927918, 1013490, 1169714, 1732919, 2893101, 6046031, 8467145, 12473026, 19080712]


plt.plot(range(1, len(x) + 1), y)

x = np.array(x).reshape(-1, 1)
poly = PolynomialFeatures(degree=2)
poly.fit(x)
X2 = poly.transform(x)

print(X2.shape)

Y = np.array(y).reshape(-1, 1)
lin_reg = LinearRegression()
lin_reg.fit(X2, Y)

y_predict = lin_reg.predict(X2)
y_predict = y_predict - 50000
print(y_predict.ravel().tolist())

plt.plot(range(1, len(x) + 1), y_predict, color='r')
plt.show()


