from module2 import pts
from module4_ptcloud import final_psl
from module6_ptcloud import satisfied,visible
from module9_ptcloud import final_scanplan, final_scanplan_index

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time
start_time = time.time()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# ax.scatter(pts[:,0], pts[:,1], pts[:,2], color ='grey', alpha = 0.01)

collect_all_satisfied_points = []
collect_all_visible_points = []
for i in range(len(final_scanplan_index)):
    index = final_scanplan_index[i]
    # colored red which scan position
    #print(index)
    #ax.scatter(final_psl[index][0], final_psl[index][1], final_psl[index][2])
    collect_all_satisfied_points.append(satisfied[index])

    collect_all_satisfied_points.append(visible[index])
    # colored green which are satisfied
    #ax.scatter(pts[satisfied[index]][0],pts[satisfied[index]][1],pts[satisfied[index]][2], color = 'green')


"""total satisifed points """
satisfied_ratio= len(set(np.concatenate(collect_all_satisfied_points)))/ len(pts)*100
satisfied_index = list(set(np.concatenate(collect_all_satisfied_points)))
print(pts[satisfied_index][:,0])
## show satisfied area
ax.scatter(pts[satisfied_index][:,0],pts[satisfied_index][:,1],pts[satisfied_index][:,2])
plt.show()
print( f'satisfied_ratio {satisfied_ratio:.2f} %')
print( f'processing tiem (show_qualified) {time.time()-start_time:.2f} second')






