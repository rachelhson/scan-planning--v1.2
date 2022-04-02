import open3d as o3d
import time 
start_time = time.time()
file = 'exp1_woodstruct/scan_exp1.pcd'
pcd = o3d.io.read_point_cloud(file)
voxled_pcd = pcd.voxel_down_sample(voxel_size=0.0045)
voxeledfile = 'exp1_woodstruct/voxeledpcd_exp1.pcd'
o3d.io.write_point_cloud(voxeledfile,voxled_pcd)
print( f'processing time (analysis - distribution) {time.time()-start_time:.2f} second')
