import open3d as o3d
import matplotlib.pyplot as plt
from Input import model
from module10 import final_scanplan
from module2 import pts
import numpy as np
# """ for our object """
# Load mesh and convert to open3d.t.geometry.TriangleMesh
mesh = o3d.io.read_triangle_mesh(model)

mesh = o3d.t.geometry.TriangleMesh.from_legacy(mesh)
triangle_indices = mesh.triangle['indices']
triangle_vertices = mesh.vertex["positions"]
triangle_ids = np.arange(0,len(triangle_indices))

scene = o3d.t.geometry.RaycastingScene()
scene.add_triangles(mesh)

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
ans = scene.cast_rays(rays_data)

"""
't_hit' distance to the intersection
'geometry_ids' the geometry hit by the ray
'primitive_ids' triangle index of the triangle that was hit 
"""

hit = ans['t_hit'].isfinite()
# calculate cast points
points = rays_data[hit][:,:3] + rays_data[hit][:,3:]*ans['t_hit'][hit].reshape((-1,1))
pcd = o3d.t.geometry.PointCloud(points)
o3d.io.write_point_cloud("../simulated_ptcloud/hit_ptcloud.pcd", pcd.to_legacy())

""" the area rays not hitted """
non_hit = set(triangle_ids).difference(set(ans['primitive_ids'].numpy()))
print(f" not hitted mesh no. : {len(non_hit)}")
non_hit_vertices = o3d.t.geometry.PointCloud(triangle_vertices[list(non_hit)])
o3d.io.write_point_cloud("../simulated_ptcloud/non_hit_vertices.pcd", non_hit_vertices.to_legacy())


