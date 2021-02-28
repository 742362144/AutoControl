import matplotlib.pyplot as plt
import numpy as np

plt.style.use(['science', 'high-contrast', 'no-latex'])

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体以便支持中文

x = np.arange(2)  # 柱状图在横坐标上的位置
# 列出你要显示的数据，数据的列表长度与x长度相同
y1 = [249.6, 37.75]
y2 = [5396.42, 27183.052]

tick_label = ['compute', 'storage']

plt.subplots(figsize=(5, 3), dpi=300)
plt.subplot(121)
bar_width = 0.3
# {'/', '\', '|', '-', '+', 'x', 'o', 'O', '.', '*'}
plt.bar(x, y1, bar_width, color='green', hatch='//', label='Math calculate')
# plt.bar(x + bar_width, y2, bar_width, color='lightsalmon', hatch='O', label='O')
plt.legend(loc='best', fontsize=8)  # 显示图例，即label
plt.xticks(x, tick_label)  # 显示x坐标轴的标签,即tick_label,调整位置，使其落在两个直方图中间位置

plt.subplot(122)
# plt.bar(x, y1, bar_width, color='burlywood', hatch='xxx', label='xxx')
plt.bar(x + bar_width, y2, bar_width, color='red', hatch='xx', label='Social graph algorithm')
plt.legend(loc='best', fontsize=8)
plt.xticks(x, tick_label)

# 防止坐标轴重叠
plt.tight_layout()
plt.show()
