from module1 import res_deg,qr_hr,qr_vr
import numpy as np
from module2 import pts, pt_normal
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import module6
""" Input """
origin = [8.4, 8.25]
final_psl = [[10.03995104,9.48401606, 0.8],
             [7.93262523, 10.11863157,0.8 ],
             [6.48940344, 8.45147331,1.2],
             [7.57735704, 6.438159,1.2  ],
             [9.76989055, 6.72397669,0.8],
            [10.29668756,  8.86510563,1.2]]

"""get satisfied"""
satisfied ={}
visible = {}

scx =pts[:,0]
scy =pts[:,1]
scz =pts[:,2]

nx = pt_normal[:,0]
ny = pt_normal[:,1]
nz = pt_normal[:,2]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for a,i in enumerate(final_psl):
    # get omcodemce angle
    pslx = final_psl[a][0]-origin[0]
    psly = final_psl[a][1]-origin[1]
    pslz = final_psl[a][2]

    rayx = pslx-scx
    rayy = psly-scy
    rayz = pslz-scz
    """ 3D """
    dot = module6.dot_product(nx,ny,nz,rayx,rayy,rayz)
    abs_normal = module6.distance(nx,ny,nz)
    abs_ray = module6.distance(rayx,rayy,rayz)
    cosia = dot/(abs_normal*abs_ray)
    cosia = cosia.round(decimals=4)
    ia = np.rad2deg(np.arccos(cosia))
    print(ia)
    dist2_ = module6.distance_2d(rayx, rayy)
    v_range = module6.distance_2d(pslx, psly)
    nonocclu_index = np.where((ia < 90) & (dist2_ < v_range))[0]
    visible[a]=nonocclu_index
    ax.scatter(pts[nonocclu_index][:,0],pts[nonocclu_index][:,1],pts[nonocclu_index][:,2],color='green')
#ax.scatter(pts[:,0], pts[:,1], pts[:,2], color='grey')
plt.show()
#     """ vertical quality check"""
#     gamma = module6.gamma_f(pslx,scx,psly,scy,pslz,scz)
#     dmax_ver = (qr_vr/1000)*module6.sin_f(90+gamma-res_deg)/module6.sin_f(res_deg)
#
#     """ horizontal quality check"""
#     dmax_hor = (qr_hr/1000)*module6.sin_f(ia+90-res_deg)/module6.sin_f(res_deg)
#
#     deltax = pslx-scx
#     deltay = psly-scy
#     deltaz = pslz-scz
#
#     real_d = module6.distance(deltax,deltay,deltaz)
#     loq_index = np.where((real_d < dmax_hor) & (real_d <dmax_ver) )
#     s_loq_index = set(loq_index[0])
#     s_nonocclu_index = set(nonocclu_index)
#     s_index = s_loq_index.intersection(s_nonocclu_index)
#     l_index = list(s_index)
#
#     satisfied[a]=l_index
#     print(l_index)
#     ax.scatter(pts[l_index][:,0],pts[l_index][:,1],pts[l_index][:,2],color='green')
# plt.show()
#print( f'processing tiem (module6) {time.time()-start_time:.2f} second')
