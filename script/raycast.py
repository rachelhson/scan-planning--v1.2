import open3d as o3d
import matplotlib.pyplot as plt
from Input import model
from module10 import final_scanplan
from module2 import pts
import numpy as np
# """ for our object """
## read mesh
mesh = o3d.io.read_triangle_mesh(model)
mesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
print("mesh")
print(mesh)

scene = o3d.t.geometry.RaycastingScene()
mesh_id = scene.add_triangles(mesh)
print(mesh_id)

#casting rays
# The first ray starts at (0.5,0.5,10) and has direction (0,0,-1).
# The second ray start at (-1,-1,-1) and has direction (0,0,-1).
# rays = o3d.core.Tensor([[0.5, 0.5, 10, 0, 0, -1], [-1, -1, -1, 0, 0, -1]],
#                        dtype=o3d.core.Dtype.Float32)
final_psl_ = final_scanplan
rays = []
for a,i in enumerate(final_psl_):
    start = final_psl_[a]
    direction = pts - start
    # make Tensor
    starts = np.tile(start,(len(pts),1))
    ray_data = np.hstack((starts, direction))
    rays.append(ray_data)
rays = np.concatenate(rays)
#print(rays)
rays_data = o3d.core.Tensor(rays, dtype=o3d.core.Dtype.Float32)
# #print(ray_data)
ans = scene.cast_rays(rays_data)
print(ans.keys())
print(ans['t_hit'].numpy(), ans['primitive_ids'].numpy())


hit = ans['t_hit'].isfinite()
points = rays_data[hit][:,:3] + rays_data[hit][:,3:]*ans['t_hit'][hit].reshape((-1,1))
pcd = o3d.t.geometry.PointCloud(points)
print(pcd)
#o3d.visualization.draw_geometries([pcd.to_legacy()])
o3d.io.write_point_cloud("simulated_ptcloud.pcd", pcd.to_legacy())

