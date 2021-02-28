import matplotlib.pyplot as plt
import numpy as np

plt.style.use(['science', 'high-contrast', 'no-latex'])

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体以便支持中文



plt.subplots(figsize=(5, 3), dpi=300)
plt.subplot(121)

x_label = ['128b', '256b', '512b', '1kb', '2kb', '4kb', '8kb', '16kb', '32kb', '64kb', '128kb']
x2 = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]
y2 = [2447, 3013, 4330, 6033, 8632, 14891, 22768, 53646, 93485, 213157, 431445]
x2 = np.array(x2)
y2 = np.array(y2)
plt.plot(range(1, len(x2) + 1), y2, label="protobuf")
plt.xticks(range(1, len(x2) + 1), x_label, rotation='vertical')

text_font = {'size': '8', 'weight': 'bold', 'color': 'black'}
plt.text(4, -150000, "Protobuf", fontdict=text_font, zorder=4)

plt.legend(loc='best', fontsize=8)  # 显示图例，即label

# plt.xticks(x, tick_label)  # 显示x坐标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置

plt.subplot(122)



x3 = ['128b', '256b', '512b', '1kb', '2kb', '4kb', '8kb', '16kb', '32kb', '64kb', '128kb']
y3 = [109, 109, 186, 187, 235, 278, 372, 589, 1085, 2104, 4107]
x3 = np.array(x3)
y3 = np.array(y3)
plt.plot(range(1, len(x3) + 1), y3, label="resp", color='r')

plt.xticks(range(1, len(x2) + 1), x_label, rotation='vertical')

text_font = {'size': '8', 'weight': 'bold', 'color': 'black'}
plt.text(2, -1300, "Redis Serialization Protocol", fontdict=text_font, zorder=4)

plt.legend(loc='best', fontsize=8)
# plt.xticks(x, tick_label)

# 防止坐标轴重叠
plt.tight_layout()
plt.show()
