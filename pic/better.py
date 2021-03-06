# pip install SciencePlots

import matplotlib.pyplot as plt
import numpy as np

plt.style.use(['science', 'high-contrast', 'no-latex'])

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体以便支持中文


def auto_label(rects):
    for rect in rects:
        height = rect.get_height()
        plt.annotate('{}'.format(height),  # put the detail data
                     xy=(rect.get_x() + rect.get_width() / 2, height),  # get the center location.
                     xytext=(0, 3),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom')


def auto_text(rects):
    for rect in rects:
        plt.text(rect.get_x(), rect.get_height(), rect.get_height(), ha='left', va='bottom')


plt.figure(figsize=(5, 4), dpi=300)

x = np.arange(1)  # 柱状图在横坐标上的位置
# 列出你要显示的数据，数据的列表长度与x长度相同
y1 = [2026.37]
y2 = [31967.02]
y3 = [34062.92]
# y4 = [27183.052]

# tick_label = ['compute', 'storage']

bar_width = 0.8
# {'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}
b1 = plt.bar(1, y1, bar_width, color='green', hatch='//', label='without scheduling')
b2 = plt.bar(2, y2, bar_width, color='red', hatch='\\\\', label='with scheduling')
b3 = plt.bar(3, y3, bar_width, color='blue', hatch='xx', label='compute only')
plt.xticks([])

auto_text(b1)
auto_text(b2)
auto_text(b3)

text_font = {'size': '10', 'weight': 'bold', 'color': 'black'}
plt.text(1.5, -1800, "Math calculate", fontdict=text_font, zorder=4)

plt.legend(loc='best', fontsize=8)  # 显示图例，即label

# plt.xticks(x, tick_label)  # 显示x坐标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置

# 防止坐标轴重叠
plt.tight_layout()
plt.show()
