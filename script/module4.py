"""11-13-2020 Potential Scan Locations"""
#from module1 import model
from Input import d_min, d_site,h_site, h_min
from module2 import pts, pt_normal
import numpy as np
import matplotlib
#matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time 
import open3d as o3d 
#from numba import jit

start_time = time.time()

#@jit(nopython =True)
def dist_2d(x1,x2,y1,y2):
    dist = np.sqrt((x1-x2)**2+(y1-y2)**2)
    return dist

pts_x = np.vstack(pts[:,0])
pts_y = np.vstack(pts[:,1])
pts_z = np.vstack(pts[:,2])

## Get psl from the pts
""" max_d gives more choice"""
d = np.linspace(d_min/1000,d_site/1000,num=3)
psl = np.concatenate([pts+d_*pt_normal for d_ in d])
#np.savetxt('../output/psl.csv', psl, delimiter=',')

#qualified_psl_index =set()
qualified_psl_index =[]
for a,psl_ in enumerate (psl):
    
    psl_x = psl_[0]
    psl_y = psl_[1]
    psl_z = psl_[2]       
    dist = dist_2d(psl_x,pts_x,psl_y,pts_y)
    
    if np.all(dist >= d_min/1000) and psl_z > h_min/1000 and psl_z < h_site/1000:
        #qualified_psl_index.add(a)
        qualified_psl_index.append(a)
      #  print(psl_z)
    #print(f"======================{a}=============================")
        
"""remove less than minimum range/ remove over eligible height"""
final_psl =psl[list(qualified_psl_index)]
#np.savetxt('../output/final_psl.csv', final_psl, delimiter=',')


""" 2D"""
pts = np.hstack((pts_x,pts_y,pts_z))
pts = np.repeat(pts,len(d),0)
final_pts = pts[list(qualified_psl_index)]
final_pts_normal = final_pts-final_psl
#np.savetxt('../output/final_pts_normal.csv', final_pts_normal, delimiter=',')

"""Plot Object & satisfied psls"""
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# # =============================================================================
# ax.scatter(final_psl[:,0],final_psl[:,1],final_psl[:,2],color='blue')
# ax.scatter(pts[:,0],pts[:,1],pts[:,2],color='grey')
# # =============================================================================
# plt.title('final_psl - considered site condition')
# plt.show()
print( f'The number of final_psl is {len(final_psl)}')
#print( f'processing time (module4) {time.time()-start_time:.2f} second')






