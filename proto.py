from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt


# proto
# X = []
# i = read
# while i <= 1024 * 1024:
#     X.append(i)
#     i = i * 2
# print(X)


x = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576]
y = [98, 112, 175, 109, 109, 186, 187, 235, 278, 372, 589, 1085, 2104, 4107, 8371, 17259, 34141]

plt.plot(x, y)
plt.show()

X = np.array(x).reshape(-1, 1)
Y = np.array(y).reshape(-1, 1)
lin_reg = LinearRegression()
lin_reg.fit(X, Y)

y_predict = lin_reg.predict(X)
print(y_predict)
# plt.scatter(X, y)
# plt.plot(X, y_predict, color='r')
# plt.show()


# X2 = np.hstack([X, X**2])
# print(X2.shape)
# lin_reg2 = LinearRegression()
# lin_reg2.fit(X2, y)
# y_predict2 = lin_reg2.predict(X2)
# plt.scatter(X, y)
# plt.plot(np.sort(X), y_predict2[np.argsort(x)], color='r')
# plt.show()