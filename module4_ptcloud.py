"""11-13-2020 Potential Scan Locations - using surface normal"""
#from module1 import model
from module1 import min_d, max_d, h_site, h_min, d_site
from module2 import pts, pt_normal
#from module3 import mesh_vertices,vertices_index,surface_normal
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time 
import open3d as o3d 
from numba import jit


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
start_time = time.time()
# =============================================================================
# """call point cloud model """
# mesh  = o3d.io.read_triangle_mesh(model)#read 3D model
# num_sample = len(mesh.vertices)
# print(f' number of sampling points : {num_sample}')
# pcd = mesh.sample_points_uniformly(number_of_points=num_sample) 
# final_num_sample = int(num_sample/2)
# final_pcd = mesh.sample_points_poisson_disk(number_of_points=final_num_sample, pcl=pcd)
# print(f' number of sampling points : {final_num_sample}')
# 
# pt_normal = np.asarray(final_pcd.normals)
# pts = np.asarray(final_pcd.points)
# """ """
# =============================================================================
#@jit(nopython =True)
def dist_2d(x1,x2,y1,y2):
    dist = np.sqrt((x1-x2)**2+(y1-y2)**2)
    return dist

pts_x = np.vstack(pts[:,0])
pts_y = np.vstack(pts[:,1])
pts_z = np.vstack(pts[:,2])

## Get psl from the pts
""" max_d gives more choice"""
max_d = 1500
d = np.linspace(min_d/1000,max_d/1000,num=3)
psl = np.concatenate([pts+d_*pt_normal for d_ in d])
np.savetxt('../output/psl.csv', psl, delimiter=',')

# =============================================================================
# """ draw max/min boundary of psl"""
# min_bound = np.array(pts+min_d/1000*pt_normal) 
# dist = dist_2d(min_bound[:,0],pts_x,min_bound[:,1],pts_y)
# max_bound = np.array(pts+max_d/1000*pt_normal)
# 
# np.savetxt('../output/min_bound.csv', min_bound, delimiter=',')
# np.savetxt('../output/max_bound.csv', max_bound, delimiter=',')
# =============================================================================
# =============================================================================
# """ for debug"""
# for i in range(3000,3001):
#     d_ = 600/1000   
#     psl =pts[i]+d_*pt_normal[i]
#     ax.scatter(pts[i][0],pts[i][1],pts[i][2], color='blue')
#     ax.scatter(psl[0], psl[1],psl[2], color='red')
# """ end-debug code """
# ax.scatter(pts[:,0],pts[:,1],pts[:,2],color = 'grey',alpha=0.1)
# =============================================================================

#qualified_psl_index =set()
qualified_psl_index =[]
for a,psl_ in enumerate (psl):
    
    psl_x = psl_[0]
    psl_y = psl_[1]
    psl_z = psl_[2]       
    dist = dist_2d(psl_x,pts_x,psl_y,pts_y)
    
    if np.all(dist >= min_d/1000) and psl_z > h_min/1000 and psl_z < h_site/1000:
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
np.savetxt('../output/final_pts_normal.csv', final_pts_normal, delimiter=',')
## Plot Object & satisfied psls
# =============================================================================
ax.scatter(final_psl[:,0],final_psl[:,1],final_psl[:,2],color='blue')
ax.scatter(pts[:,0],pts[:,1],pts[:,2],color='grey')
# =============================================================================
plt.title('final_psl - considered site condition')
plt.show()
print( f'{len(final_psl)/len(psl) *100} of psls are qualified')
print( f'The number of final_psl is {len(final_psl)}')
print( f'processing time (module4) {time.time()-start_time} second')






