
""" Simulate low score points"""

from module2 import pts, pt_normal
from module4_ptcloud import final_psl
from module7_ptcloud import score_,mu,std
from module6_ptcloud import satisfied ## contains for each psl : satisfied point cloud 
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

start_time = time.time()
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

## define low_score criteria : low_score_criteria
def getlow_score_criteria(mu,std):
    low_score_criteria = mu-2*std# (30%)
    if low_score_criteria < 0:
        low_score_criteria = mu-std #(60%)
    else:
        low_score_criteria = low_score_criteria
    return low_score_criteria

low_score_criteria = getlow_score_criteria(mu,std)
print(f"low_score_criteria is {low_score_criteria:.2f}")
lowscore_index = np.where(score_ < low_score_criteria)

# ax.scatter(pts[lowscore_index][:,0], pts[lowscore_index][:,1], pts[lowscore_index][:,2], color ='red')
# ax.scatter(pts[:,0], pts[:,1], pts[:,2], color ='grey', alpha = 0.01)

lowscore_count = {}
for psl in satisfied.keys():
    
    satisfied_points = satisfied[psl]
    a = [x for x in satisfied_points if x in lowscore_index[0]]
    lowscore_length = len(a)
    lowscore_count[psl]=lowscore_length
    
# Find which PSL has as many as low score points 
values = list(lowscore_count.values())
keys = list(lowscore_count.keys())
max_lowpoint_index = np.argmax(values)

print(f' PSL point index {max_lowpoint_index} can capture {np.amax(values)} object points among total {len(lowscore_index[0])}low score points')
# plot the psl that capture low score points

#ax.scatter(final_psl[max_lowpoint_index][0],final_psl[max_lowpoint_index][1],final_psl[max_lowpoint_index][2],color='green')
# plt.show()

print( f'processing tiem (module8) {time.time()-start_time:.2f} second')


