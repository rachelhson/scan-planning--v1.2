""" 11-11-2020 """
import numpy as np
import open3d as o3d
from Input import model, qr_hr, qr_vr, d_min, d_site, h_site, h_min, h_mid
import time

start_time = time.time()
"""============================================================================"""
mesh = o3d.io.read_triangle_mesh(model)
mesh.compute_vertex_normals()

"""set maximum object area"""
bound_size = mesh.get_max_bound() - mesh.get_min_bound()

h = bound_size[2] * 1000  # mm
w = bound_size[0] * 1000  # mm
l = bound_size[1] * 1000  # mm

print(f'=== bounding dimension : {h:.2f},{w:.2f},{l:.2f} ===')

""" resolution dictionary """

res_dic = {1: 0.009, 2: 0.018, 3: 0.035, 4: 0.044, 5: 0.070, 6: 0.088, 7: 0.141, 8: 0.176, 9: 0.281}

""" point-to-point analysis on the maximum dimension of the object """


def rad(deg):
    rad_ = np.deg2rad(deg)
    return rad_


""" fov check """

# Fov selection
min_fov = 45  # degree
max_fov = 90  # degree

fov_1 = np.arctan(np.max([w, l, np.sqrt(w ** 2 + l ** 2)]) / (2 * d_min))  # rad
fov_1 = np.rad2deg(fov_1 * 2)

fov_2 = np.arctan(np.max([w, l, np.sqrt(w ** 2 + l ** 2)]) / (2 * d_site))  # rad
fov_2 = np.rad2deg(fov_2 * 2)

print(f'field of view : {fov_1:.2f}, {fov_2:.2f}')  ## 90 180 360

if fov_1 < 90:
    fov = 90
elif fov_1 > 90 and fov_1 < 180:
    fov = 180
elif fov_1 < 360:
    fov = 360

# print (f'==== fov = {fov} ===')

""" horizontal
    incidence angle = 45 """
# possible ranges (d)
range = np.arange(d_min, d_site + 100, 100);  # mm
qm_h_dic = {}
for i in res_dic.keys():
    # print(res_dic[i])
    res_h = res_dic[i]
    alpha_h = 45  ## incidence angle

    qm_h_range_dic = {}
    for j in range:
        r = j / np.cos(rad(alpha_h))
        """horizontal quality model"""
        qm_h = np.sin(rad(res_h)) * r / np.cos(rad(alpha_h - res_h))
        qm_h_range_dic[j] = qm_h
        qm_h_list = list(qm_h_range_dic.values())
    # print(qm_h_range_dic)
    qm_h_dic[i] = np.array(qm_h_list)
# print(f'horizontal for 45 ia :{qm_h_dic}')

""" horizontal
    incidence angle = 60 """
# possible ranges (d)
range = np.arange(d_min, d_site + 100, 100);
qm_h_dic = {}
for i in res_dic.keys():
    # print(res_dic[i])
    res_h = res_dic[i]
    alpha_h = 60  ## incidence angle

    qm_h_range_dic = {}
    for j in range:
        r = j / np.cos(rad(alpha_h))
        """horizontal quality model"""
        qm_h = np.sin(rad(res_h)) * r / np.cos(rad(alpha_h - res_h))
        qm_h_range_dic[j] = qm_h
        qm_h_list = list(qm_h_range_dic.values())
    # print(qm_h_range_dic)
    qm_h_dic[i] = np.array(qm_h_list)
# print(f'horizontal for 60 ia :{qm_h_dic}')

""" horizontal for average """
for i in res_dic.keys():
    # print(res_dic[i])
    res_h = res_dic[i]
    alpha_h1 = 45  ## incidence angle
    alpha_h2 = 60  ## incidence angle

    qm_h_range_dic = {}
    for j in range:
        r = j / np.cos(rad(alpha_h))
        """horizontal quality model"""
        qm_h1 = np.sin(rad(res_h)) * r / np.cos(rad(alpha_h1 - res_h))
        qm_h2 = np.sin(rad(res_h)) * r / np.cos(rad(alpha_h2 - res_h))
        qm_h_range_dic[j] = np.average([qm_h1, qm_h2])
        qm_h_list = list(qm_h_range_dic.values())
    # print(qm_h_range_dic)
    qm_h_dic[i] = np.array(qm_h_list)
# print(f'horizontal for ave. ia :{qm_h_dic}')


""" only for horizontal """
h_valid_res = set()
for i in res_dic.keys():
    # print(qm_h_dic[i])
    if len(np.where(qm_h_dic[i] < qr_hr)[0]) > len(qm_h_dic[i]) / 2:
        h_valid_res.add(i)
        # print(f'horizontal satisfied resolution : {i}')
# print(f'horizontal satisfied resolution : {h_valid_res}')


""" vertical for h_min """
qm_v_dic = {}
for i in res_dic.keys():
    res_v = res_dic[i]
    range = np.arange(d_min, d_site + 100, 100);
    qm_v_range_dic = {}
    for j in range:
        alpha_v = np.rad2deg(np.arctan((h - h_min) / j))  ## tangent bounding box angle
        """vertical quality model"""
        r = np.sqrt(j ** 2 + (h - h_mid) ** 2)  ## ray distance
        qm_v = np.sin(rad(res_v)) * r / np.cos(rad(alpha_v - res_v))
        qm_v_range_dic[j] = qm_v
        qm_v_list = list(qm_v_range_dic.values())
    # print(qm_v_range_dic)
    qm_v_dic[i] = np.array(qm_v_list)
# print(f'vertical w/h_min : {qm_v_dic}')

""" vertical for h_max """
qm_v_dic = {}
for i in res_dic.keys():
    res_v = res_dic[i]
    range = np.arange(d_min, d_site + 100, 100);
    qm_v_range_dic = {}
    for j in range:
        alpha_v = np.rad2deg(np.arctan((h - h_site) / j))  ## tangent bounding box angle
        """vertical quality model"""
        r = np.sqrt(j ** 2 + (h - h_mid) ** 2)  ## ray distance
        qm_v = np.sin(rad(res_v)) * r / np.cos(rad(alpha_v - res_v))
        qm_v_range_dic[j] = qm_v
        qm_v_list = list(qm_v_range_dic.values())
    # print(qm_v_range_dic)
    qm_v_dic[i] = np.array(qm_v_list)
# print(f'vertical w/h_site : {qm_v_dic}')

""" vertical for h_mid for scanner height"""
qm_v_dic = {}
for i in res_dic.keys():
    res_v = res_dic[i]
    range = np.arange(d_min, d_site + 100, 100);
    qm_v_range_dic = {}
    for j in range:
        alpha_v = np.rad2deg(np.arctan((h - h_mid) / j))  ## tangent bounding box angle
        """vertical quality model"""
        r = np.sqrt(j ** 2 + (h - h_mid) ** 2)  ## ray distance
        qm_v = np.sin(rad(res_v)) * r / np.cos(rad(alpha_v - res_v))
        qm_v_range_dic[j] = qm_v
        qm_v_list = list(qm_v_range_dic.values())
    # print(qm_v_range_dic)
    qm_v_dic[i] = np.array(qm_v_list)
# print(f'vertical w/h_mid : {qm_v_dic}')

""" only for vertical """
v_valid_res = set()
for i in res_dic.keys():
    # print(qm_v_dic[i])
    if len(np.where(qm_v_dic[i] < qr_vr)[0]) > len(qm_v_dic[i]) / 2:
        v_valid_res.add(i)
        # print(f'vertical satisfied resolution : {i}')
# print(f'vertical satisfied resolution : {v_valid_res}')

"""Final hor/vertical valid resolution"""
valid_res = h_valid_res.intersection(v_valid_res)
res_deg = res_dic[np.max(list(valid_res))]

# print(valid_res)
# print(list(valid_res))
print(f"result of module 1 | res : {valid_res} | FoV :{fov} | chosen res: {res_deg}")
print(f'processing time (module1) {time.time() - start_time} second')
