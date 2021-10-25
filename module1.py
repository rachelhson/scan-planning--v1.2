""" 11-11-2020 """
import numpy as np
import open3d as o3d

## Input - model and quality requirement
model = '../input/test_column.ply'
qr = 5 # mm  quality requirement

## quality specification
qr_hr= qr
qr_vr= qr*2

#if the site is limited 
d_min = 1000 #mm 
d_site = 1500 #mm
h_site = 1500 #mm 
h_min = 700 #mm

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

# Resolution 

horstep_dic ={1:0.009, 2:0.018, 3:0.035, 
              4:0.044,5:0.070, 6:0.088,
              7:0.141,8:0.176, 9:0.281}

# =============================================================================
# verstep_dic ={1:0.019, 2:0.039, 3:0.077, 
#               4:0.097,5:0.155, 6:0.193,      
#               7:0.309,8:0.382, 9:0.619}
# =============================================================================

verstep_dic ={1:0.009, 2:0.018, 3:0.035, 
              4:0.044,5:0.070, 6:0.088,
              7:0.141,8:0.176, 9:0.281}



def rad(deg):
    rad_ = np.deg2rad(deg)
    return rad_

### get the pt2pt distance when d = 1000
l_total_hor={}
for index, res in horstep_dic.items():
    """ l = d/cos(fov)/sin(180-(90-fov)-res)*sin(res)"""
    side = d/np.cos(rad(fov))
    l = side/np.sin(rad(180-(90-fov)-res))*np.sin(rad(res))
    l_total_hor[index]=float(format(l, '.2f'))  
print(f'p2p:{l_total_hor}')

l_total_ver={}
for index, res in verstep_dic.items():
    """ l = d/cos(fov)/sin(180-(90-fov)-res)*sin(res)"""
    side = d/np.cos(rad(fov))
    l = side/np.sin(rad(180-(90-fov)-res))*np.sin(rad(res))
    l_total_ver[index]=float(format(l, '.2f'))  
print(f'p2p_ver:{l_total_ver}')

"""Based on the distance analysis, select the resolution"""
hor_index = dict((index, l) for index, l in l_total_hor.items() if l < qr_hr)
final_res_hor = {key: horstep_dic[key] for key in hor_index.keys()}
""" this resolutions can be used for planning"""
print(f'final_resolution based on hor: {final_res_hor}')

ver_index = dict((index, l) for index, l in l_total_ver.items() if l < qr_vr)
final_res_ver = {key: verstep_dic[key] for key in ver_index.keys()}
""" this resolutions can be used for planning"""
print(f'final_resolution based on ver: {final_res_ver}')

keys = set()
for hor_key in hor_index.keys():
    if hor_key in ver_index.keys():
        keys.add(hor_key)

# Distance
def to_obj_dist(res):
    d = qr*np.sin(rad(180-(90-fov)-res))/np.sin(rad(res))*np.cos(rad(fov))
    return float(format(d,'.2f'))
min_d = 800 #mm
max_d = {key: to_obj_dist(final_res_hor[key]) for key in keys}
print(f' max_distasnce :{max_d}')

""" select resolution"""
exam_res = input('enter resolution key:')
print(f'selected hor_resolution is  {final_res_hor[float(exam_res)]}')
print(f'selected ver_resolution is  {final_res_ver[float(exam_res)]}')

#output of module1 
max_d = max_d[float(exam_res)]

# final max_d 
if d_site < min_d:
    print('site requires more space for scanning') 
    
elif d_site > max_d:
    max_d = max_d
    print(f'maximum distance :{max_d}')
else:
    max_d = d_site
    print(f'maximum distance :{max_d}')
hor_step = final_res_hor[float(exam_res)]
ver_step = final_res_ver[float(exam_res)]
