from module1 import res_deg,qr_hr,qr_vr
import numpy as np
from module2 import pts, pt_normal
from module4 import final_psl
from module6 import satisfied, visible
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import module6
from module10 import final_scanplan
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

final_psl_ = final_scanplan
for psl in final_psl_:
    ax.scatter(psl[0],psl[1],psl[2])
"""get satisfied"""
satisfied_ ={}
visible_ = {}
visible_list =[]
scx =pts[:,0]
scy =pts[:,1]
scz =pts[:,2]

nx = pt_normal[:,0]
ny = pt_normal[:,1]
nz = pt_normal[:,2]

for a,i in enumerate(final_psl_):
    # get omcodemce angle
    pslx = final_psl_[a][0]
    psly = final_psl_[a][1]
    pslz = final_psl_[a][2]

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
    #print(ia)
    dist2_ = module6.distance_2d(rayx, rayy)
    v_range = module6.distance_2d(pslx, psly)
    nonocclu_index = np.where((ia < 90) & (dist2_ < v_range))[0]
    occlu_index = np.where((ia > 90))[0]
    visible_[a]=nonocclu_index
    visible_list.append(nonocclu_index)
visible_ = set(np.concatenate(visible_list))
all_point = set(np.arange(0, len(pts)))
non_visible_= all_point.difference(visible_)
print(len(visible_))
print(len(non_visible_))
print(len(all_point))

list_visible_ = list(visible_)
list_non_visible_ = list(non_visible_)

np.savetxt("non_occluded_points.csv",pts[list_visible_],delimiter=",")
np.savetxt("occluded_points.csv",pts[list_non_visible_],delimiter=",")
#print(pts[visible_])
#print(pts[non_visible])

    #ax.scatter(pts[occlu_index][:,0],pts[occlu_index][:,1],pts[occlu_index][:,2],color='red')
    #ax.scatter(pts[nonocclu_index][:,0],pts[nonocclu_index][:,1],pts[nonocclu_index][:,2],color='green')
#ax.scatter(pts[:,0], pts[:,1], pts[:,2], color='grey', alpha = 0.1)
plt.show()

#ax.scatter(map_coord[0],map_coord[1],map_coord[2],color='black')

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
