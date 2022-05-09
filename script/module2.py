from Input import sampling_interval_factor
from module1 import mesh,qr_hr
import open3d as o3d 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 
import numpy as np
import time

start_time = time.time()
qr = qr_hr
# =============================================================================
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# =============================================================================

#mesh  = o3d.io.read_triangle_mesh(model)#read 3D model

#Visualize Wireframe
#o3d.visualization.draw_geometries([mesh], mesh_show_wireframe = True)
# print(len(np.asarray(mesh.vertices)))# numb of vertices
# print(len(np.asarray(mesh.triangles)))# numb of triangles
# print(np.asarray(mesh.triangle_normals)) # get normal vectors of each mesh surface
""" making sample point from mesh """
num_sample = len(mesh.vertices)*2
#print(f'number of sampling points : {num_sample}')
pcd = mesh.sample_points_uniformly(number_of_points=num_sample)
point_cloud = qr*sampling_interval_factor/1000 #m
print(f"Downsample the point cloud with a spacing of {point_cloud*1000}mm")
downpcd = pcd.voxel_down_sample(voxel_size=point_cloud)
#print(f'number of downsample points : {len(downpcd.points)}')
# visualize the 3d model in sample points
#o3d.visualization.draw_geometries([downpcd])
# #final_num_sample = int(num_sample)
# #final_pcd = mesh.sample_points_poisson_disk(number_of_points=final_num_sample, pcl=pcd)
downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=5)) ## calculate normal
#o3d.visualization.draw_geometries([downpcd],point_show_normal=True) # show normal for each point

""" pcd convert to numpy array"""
pt_normal = np.asarray(downpcd.normals)
pts = np.asarray(downpcd.points)

""" remove the points bottom points (what we dont need to plan for) """
nonexist_points = np.where(pts[:,2]<0.01)[0]
pt_normal = np.delete(pt_normal,nonexist_points,0)
pts = np.delete(pts,nonexist_points,0)
print(f'after removing the bottom # of pts : {len(pts)}')

"""output the final sample object """
#np.savetxt('../output/sampled_points.csv', pts, delimiter=',')
#np.savetxt('../output/pt_normal.csv', pt_normal, delimiter=',')
#o3d.visualization.draw_geometries([pcd])
"""statistics for spacing between sample point"""
pcdfilename = "../output/downpcd.pcd"
o3d.io.write_point_cloud(pcdfilename, downpcd)
dist= o3d.geometry.PointCloud.compute_nearest_neighbor_distance(downpcd)
mu = np.average(dist)
var = np.var(dist)
print(f'spacing average: {mu}, variance: {var}') #mm
#print( f'processing time (module2) {time.time()-start_time:.2f} second')
