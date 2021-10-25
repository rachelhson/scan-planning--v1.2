
""" 11-12-2020 Making dense data - not using this since we can use it in blender"""

from module1 import model,qr

import open3d as o3d 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 
import numpy as np
import time 
start_time = time.time()

# =============================================================================
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# =============================================================================

mesh  = o3d.io.read_triangle_mesh(model)#read 3D model

""" surface normal """
mesh.compute_vertex_normals()
#print(np.asarray(mesh.triangle_normals))
#o3d.visualization.draw_geometries([mesh])
 

#print(np.asarray(mesh.triangle_normals))
#print(mesh)
#print(len(np.asarray(mesh.vertices)))# numb of vertices
#print(len(np.asarray(mesh.triangles)))# numb of triangles

# Visualize Mesh
#o3d.visualization.draw_geometries([mesh])

# uniformly samples points from the 3D surface based on the triangle area
num_sample = len(mesh.vertices)*2
print(f'number of sampling points : {num_sample}')
pcd = mesh.sample_points_uniformly(number_of_points=num_sample) 
point_cloud = qr*2/1000 #m
print(f"Downsample the point cloud with a voxel of {point_cloud}")
downpcd = pcd.voxel_down_sample(voxel_size=point_cloud)
#o3d.visualization.draw_geometries([downpcd])
#o3d.visualization.draw_geometries([pcd],point_show_normal=False)
#final_num_sample = int(num_sample)
#final_pcd = mesh.sample_points_poisson_disk(number_of_points=final_num_sample, pcl=pcd)
downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.04, max_nn=5))
#o3d.visualization.draw_geometries([downpcd],point_show_normal=True)

""" pcd convert to numpy array"""
pt_normal = np.asarray(downpcd.normals)
pts = np.asarray(downpcd.points)
print(f'before removing the bottom # of pts : {len(pts)}')

""" remove the points not observed ( delete bottom points) """
nonexist_points = np.where(pts[:,2]<0.01)[0]
pt_normal = np.delete(pt_normal,nonexist_points,0)
pts = np.delete(pts,nonexist_points,0)
print(f'after removing the bottom # of pts : {len(pts)}')
"""output the final sample object """ 
np.savetxt('../output/sampled_points.csv', pts, delimiter=',')
np.savetxt('../output/pt_normal.csv', pt_normal, delimiter=',')
# number_of_points = how many points are sampled from the triangle surface
#o3d.visualization.draw_geometries([pcd])

#tri_mesh= o3d.geometry.LineSet.create_from_triangle_mesh(mesh)
#o3d.visualization.draw_geometries([tri_mesh],mesh_show_wireframe=True,point_show_normal=True)

#pcdfilename = "../data/con_column.pcd"
#o3d.io.write_point_cloud(pcdfilename, pcd)
#dist= o3d.geometry.PointCloud.compute_nearest_neighbor_distance(pcd)
#print(dist) #mm

#mu, std = norm.fit(dist)
#print(mu) #mm


print( f'processing time (module2) {time.time()-start_time} second')
