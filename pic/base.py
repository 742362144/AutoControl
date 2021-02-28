# https://cloud.tencent.com/developer/article/1709954
import matplotlib.pyplot as plt
import numpy as np

plt.style.use(['science', 'high-contrast', 'no-latex'])

labels = ['L1', 'L2', 'L3', 'L4', 'L5']
data_a = [20, 34, 30, 35, 27]
data_b = [25, 32, 34, 20, 25]
data_c = [12, 20, 24, 17, 16]
x = np.arange(len(labels))
width = .25
# plots
fig, ax = plt.subplots(figsize=(5, 3), dpi=200)
bar_a = ax.bar(x - width / 2, data_a, width, label='category_A')
bar_b = ax.bar(x + width / 2, data_b, width, label='category_B')
bar_c = ax.bar(x + width * 3 / 2, data_c, width, label='category_C')
ax.set_xticks(x + .1)
ax.set_xticklabels(labels, size=10)
ax.legend()

text_font = {'size': '14', 'weight': 'bold', 'color': 'black'}
ax.text(.03, .9, "(a)", transform=ax.transAxes, fontdict=text_font, zorder=4)
ax.text(.87, -.08, '\nVisualization by DataCharm', transform=ax.transAxes,
        ha='center', va='center', fontsize=5, color='black', fontweight='bold', family='Roboto Mono')
plt.savefig(r'F:\DataCharm\学术图表绘制\Python-matplotlib\SciencePlots\bar_sci_high-contrast.png', width=5, height=3,
            dpi=900, bbox_inches='tight')
plt.show()
