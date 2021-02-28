import matplotlib.pyplot as plt
import numpy as np

plt.style.use(['science', 'high-contrast', 'no-latex'])

# labels = ['Math calculate', 'Social graph algorithm']
labels = ['compute', 'storage']
data_a = [37.75, 249.6]
data_b = [27183.052, 5396.42]
x = np.arange(len(labels))
width = .25

# plots
fig, ax = plt.subplots(figsize=(5, 3), dpi=200)
bar_a = ax.bar(x / 2, data_a, width)
bar_b = ax.bar(x + width / 2, data_b, width, label='storage')


ax.set_xticklabels(labels, size=10)
ax.set_xticks(x + .1)
ax.legend()

text_font = {'size': '14', 'weight': 'bold', 'color': 'black'}
ax.text(.35, -.13, "Math calculate", transform=ax.transAxes, fontdict=text_font, zorder=4)
# ax.text(.87,-.08,'\nVisualization by DataCharm',transform = ax.transAxes,
#         ha='center', va='center',fontsize = 5,color='black',fontweight='bold',family='Roboto Mono')
# plt.savefig(r'F:\DataCharm\学术图表绘制\Python-matplotlib\SciencePlots\bar_sci_high-contrast.png',width=5,height=3,
#             dpi=900,bbox_inches='tight')
plt.show()
