import matplotlib.pyplot as plt
import numpy as np

plt.style.use(['science', 'high-contrast', 'no-latex'])

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体以便支持中文

# x = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216]
# y = [754326, 816252, 702338, 713058, 707751, 681619, 700898, 690466, 702017, 825832, 822247, 874179, 727937, 752400,
#      760544, 816799, 927918, 1013490, 1169714, 1732919, 2893101, 6046031, 8467145, 12473026, 19080712]

x_label1 = ['1b', '2b', '4b', '8b', '16b', '32b', '64b', '128b', '256b', '512b', '1kb', '2kb', '4kb', '8kb', '16kb',
            '32kb', '64kb', '128kb', '256kb', '512kb', '1mb', '2mb', '4mb', '8mb', '16mb']
x1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288,
      1048576, 2097152, 4194304, 8388608, 16777216]
y1 = [754326, 816252, 702338, 713058, 707751, 681619, 700898, 690466, 702017, 825832, 822247, 874179, 727937, 752400,
      760544, 816799, 927918, 1013490, 1169714, 1732919, 2893101, 6046031, 8467145, 12473026, 19080712]

p = [754472.270792571, 754474.2043265924, 754478.0713943291, 754485.8055285788, 754501.2737921828, 754532.2102998096, 754594.0832367378, 754717.828797293, 754965.3186651991, 755460.2933881936, 756450.2227829115, 758430.0013672634, 762389.2377156315, 770306.4271310247, 786135.6728364393, 817773.6317457817, 880967.4195585189, 1007026.4751602027, 1257830.5062684077, 1754182.2481041667, 2725860.4502530834, 4585115.7284605075, 7967221.780513721, 13385815.86717361, 18840531.97070724]

x1 = np.array(x1[:20])
y1 = np.array(y1[:20])
p = np.array(p[:20])
x_label1 = x_label1[:20]
# plt.plot(range(1, len(x)+1), y, label="net")
#
# plt.xticks(range(1, len(x)+1), x_label, rotation='vertical')
#
# plt.legend(loc='best', fontsize=10)
# # 防止坐标轴重叠
# # plt.tight_layout()
# plt.show()


# tick_label = ['compute', 'storage']

plt.subplots(figsize=(5, 3), dpi=300)
plt.subplot(121)

plt.plot(range(1, len(x1) + 1), y1, label="net")
plt.plot(range(1, len(x1) + 1), p, label="model")

plt.xticks(range(1, len(x1) + 1), x_label1, rotation='vertical')

text_font = {'size': '10', 'weight': 'bold', 'color': 'black'}
plt.text(4, 250000, "Network cost model", fontdict=text_font, zorder=4)

plt.legend(loc='best', fontsize=8)  # 显示图例，即label

# plt.xticks(x, tick_label)  # 显示x坐标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置

plt.subplot(122)

x_label2 = ['128b', '256b', '512b', '1kb', '2kb', '4kb', '8kb', '16kb', '32kb', '64kb', '128kb']
x2 = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072]
y2 = [2447, 3013, 4330, 6033, 8632, 14891, 22768, 53646, 93485, 213157, 431445]
x2 = np.array(x2)
y2 = np.array(y2)
plt.plot(range(1, len(x2) + 1), y2, label="protobuf")

x3 = ['128b', '256b', '512b', '1kb', '2kb', '4kb', '8kb', '16kb', '32kb', '64kb', '128kb']
y3 = [109, 109, 186, 187, 235, 278, 372, 589, 1085, 2104, 4107]
x3 = np.array(x3)
y3 = np.array(y3)
plt.plot(range(1, len(x3) + 1), y3, label="redis")

plt.xticks(range(1, len(x2) + 1), x_label2, rotation='vertical')

text_font = {'size': '10', 'weight': 'bold', 'color': 'black'}
plt.text(2, -200000, "Serialization cost model", fontdict=text_font, zorder=4)

plt.legend(loc='best', fontsize=8)
# plt.xticks(x, tick_label)

# 防止坐标轴重叠
plt.tight_layout()
plt.show()
