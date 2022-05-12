import numpy as np
import open3d as o3d
"================================================================"
## Input - model and quality requirement
model = 'exp1_str.ply'
qr = 5 # mm  quality requirement

## quality specification
qr_hr= qr
qr_vr= qr*2

## for point cloud sampling for object
sampling_interval_factor = 2

#if the site is limited
d_min = 1000 #mm
d_site = 1500 #mm
h_site = 1200 #mm # Jackal
h_min = 870 #mm
"================================================================"
h_mid = (h_min+h_site)/2

# Bounding Box size of the Object
mesh  = o3d.io.read_triangle_mesh(model)#read 3D model
bound_size = mesh.get_max_bound() - mesh.get_min_bound()

h = bound_size[2]*1000 #mm
w = bound_size[0]*1000 #mm
l = bound_size[1]*1000 #mm

""" set up FOV and scan resolution based on the minimum range"""
d =max(d_min,d_site) #mm

# Fov selection
min_fov = 45 # degree
max_fov = 90 # degree

fov_1 = np.arctan(np.max([w,l])/(2*d)) # rad
fov_1 = np.rad2deg(fov_1)

if fov_1 < min_fov:
    fov = min_fov
elif fov_1 > max_fov:
    fov = max_fov
else:
    fov = fov_1
print(f'field of view : {fov}')
