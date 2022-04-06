import numpy as np
import matplotlib.pyplot as plt
"""concrete column"""
# Create some mock data
data1 = [2,3,4,5]
data2 = [1197,604,503,177]
data3 = [63.8,31.4,27.8,25.9]

ax1 = plt.subplot(131)
color = 'tab:red'
ax1.plot(data1, data3, color=color,marker='o')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
color = 'tab:blue'
ax2.plot(data1, data2, color=color,marker='o',linestyle = '--')
ax2.tick_params(axis='y', labelcolor=color)
ax2.grid(axis='both')
#fig.tight_layout()  # otherwise the right y-label is slightly clipped

"""reaction wall"""
data1 = [2,3,4,5]
data2 = [19454,18503,16939,15246]
data3 = [269.5,212.4,164.0,119.1]

ax3 = plt.subplot(132)
color = 'tab:red'
ax3.plot(data1, data3, color=color,marker='o')
ax3.tick_params(axis='y', labelcolor=color)

ax4 = ax3.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax4.plot(data1, data2, color=color,marker='o',linestyle = '--')
ax4.tick_params(axis='y', labelcolor=color)
ax4.grid(axis='both')
#fig.tight_layout()  # otherwise the right y-label is slightly clipped

"""timber struct"""
data1 = [2,3,4,8]
data2 = [4238,1757,1135,262]
data3 = [329.56,42.67,14.07,1.02]

ax5 = plt.subplot(133)
color = 'tab:red'
ax5.plot(data1, data3, color=color, marker='o')
ax5.tick_params(axis='y', labelcolor=color)

ax6 = ax5.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax6.plot(data1, data2, color=color,marker='o',linestyle = '--' )
ax6.tick_params(axis='y', labelcolor=color)
#fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax6.grid(axis='both')
plt.show()
