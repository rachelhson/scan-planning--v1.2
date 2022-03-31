from module2 import pts
from module4_ptcloud import final_psl
from module6_ptcloud import satisfied
from module9_ptcloud import final_scanplan, final_scanplan_index

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pts[:,0], pts[:,1], pts[:,2], color ='grey', alpha = 0.01)

for i in range(len(final_scanplan_index)):
    index = final_scanplan_index[i]
    # colored red which scan position
    ax.scatter(final_psl[index][:,0], final_psl[index][:,1], final_psl[index][:,2], color ='red')
    # colored green which are satisfied
    ax.scatter(pts[satisfied[index]][0],pts[satisfied[index]][1],pts[satisfied[index]][2], color = 'green')
plt.show()






