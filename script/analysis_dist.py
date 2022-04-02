from module2 import downpcd
import open3d as o3d
import time
start_time = time.time()
voxeledpcd = downpcd.voxel_down_sample(voxel_size=0.005)
#o3d.visualization.draw_geometries([voxeledpcd])
pcdfilename = "../output/voxeledpcd_exp1.pcd"
o3d.io.write_point_cloud(pcdfilename, voxeledpcd)
print( f'processing time (analysis - distribution) {time.time()-start_time:.2f} second')