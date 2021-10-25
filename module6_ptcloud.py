""" For each PSL check which points can capture"""

from module1 import hor_step, ver_step,qr_hr,qr_vr
from module2 import pts, pt_normal
from module4_ptcloud import final_psl
from module4_ptcloud import final_psl

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

start_time = time.time()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


def dot_product(psl_x,psl_y,psl_z,sc_x,sc_y,sc_z):
    dot = psl_x*sc_x + psl_y*sc_y + psl_z*sc_z
    return dot 

def dot_product2d(psl_x,psl_y,sc_x,sc_y):
    dot = psl_x*sc_x + psl_y*sc_y 
    return dot 


def distance(x,y,z):
    dist = np.sqrt(x**2+y**2+z**2)
    return dist

def distance_2d(x,y):
    dist = np.sqrt(x**2+y**2)
    return dist

def gamma_f(x1,x2,y1,y2,z1,z2):
    nomi = np.abs(z1-z2)
    deltax = x1-x2
    deltay = y1-y2
    denomi = distance_2d(deltax,deltay)
    gamma  = np.arctan(nomi/denomi)
    gamma_ = np.rad2deg(gamma)
    return gamma_

def sin_f (deg):
    sin_rad = np.sin(np.deg2rad(deg))
    return sin_rad

def cos_f (deg):
    cos_rad = np.cos(np.deg2rad(deg))
    return cos_rad

""" based on psl, non occlude/occlude surface capture"""
satisfied ={}
visible = {}

scx =pts[:,0]
scy =pts[:,1]
scz =pts[:,2]

nx = pt_normal[:,0]
ny = pt_normal[:,1]
nz = pt_normal[:,2]


for j in range(len(final_psl)):
    """ incidence angle """
    pslx = final_psl[j,0]
    psly = final_psl[j,1]
    pslz = final_psl[j,2]
      
    rayx = pslx-scx 
    rayy = psly-scy 
    rayz = pslz-scz 
    
    
# =============================================================================
#     """ psl """
#     #ax.scatter(pslx,psly,pslz, color ='red')
#     psl_coord = np.hstack((pslx,psly,pslz))
#     np.savetxt('../output/psl_coord.csv', psl_coord[None,:],delimiter=',')
# =============================================================================
    """ 3D """
    dot = dot_product(nx,ny,nz,rayx,rayy,rayz) 
    abs_normal = distance(nx,ny,nz)
    abs_ray = distance(rayx,rayy,rayz)
    cosia = dot/(abs_normal*abs_ray)
    cosia = cosia.round(decimals=4)
    ia = np.rad2deg(np.arccos(cosia))
    #print(ia)
    nonocclu_index = np.where(ia<90)[0]
    visible[j]=nonocclu_index  
    
    """ 2D """
# =============================================================================
#     dot = dot_product2d(nx,ny,rayx,rayy) 
#     abs_normal = distance_2d(nx,ny)
#     abs_ray = distance_2d(rayx,rayy)
#     cosia = dot/(abs_normal*abs_ray)
#     #print(f"incidence angle:{cosia}")
#     cosia_= np.where(cosia >=1, int(1), cosia) # over1 == 1
#     
#     ia = np.rad2deg(np.arccos(cosia_))
# =============================================================================
    #print(f"incidence angle:{ia}")
    #print(ia)
    #nonocclu_index = np.where(ia<90)[0]
    #visible[j]=nonocclu_index
      

    """ quality check """
    dx = pslx-pts[:,0]
    dy = psly-pts[:,1] 
    dz = pslz-pts[:,2] 
    actual_d =distance(dx,dy,dz) 
    
    """ vertical quality check"""
    gamma = gamma_f(pslx,scx,psly,scy,pslz,scz)
    dmax_ver = (qr_vr/1000)*sin_f(90+gamma-ver_step)/sin_f(ver_step)
    
    """ horizontal quality check"""
    dmax_hor = (qr_hr/1000)*sin_f(ia+90-hor_step)/sin_f(hor_step) 
        
    deltax = pslx-scx
    deltay = psly-scy
    deltaz = pslz-scz 
    
    real_d = distance(deltax,deltay,deltaz)
    loq_index = np.where((real_d < dmax_hor) & (real_d <dmax_ver) )
    s_loq_index = set(loq_index[0])
    s_nonocclu_index = set(nonocclu_index)
    s_index = s_loq_index.intersection(s_nonocclu_index)
    l_index = list(s_index)
    
    satisfied[j]=l_index
    

    #ax.scatter(pts[l_index][:,0],pts[l_index][:,1],pts[l_index][:,2])
print( f'processing tiem (module6) {time.time()-start_time} second')   