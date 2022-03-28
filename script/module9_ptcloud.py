"""11-29-2020 Find next best view"""


from module2 import pts
from module4_ptcloud import final_psl
from module4_ptcloud import final_psl, dist_2d
from module6_ptcloud import satisfied, distance,visible
from module8_ptcloud import max_lowpoint_index

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

start_time = time.time()


## For 3D plot 
# =============================================================================
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# =============================================================================

## For 2D plot 
fig = plt.figure()
ax = plt
first_scan_index = max_lowpoint_index
first_scan = final_psl[first_scan_index]
## plot the first scan
ax.scatter(first_scan[0],first_scan[1],first_scan[2],color='green')  
#np.savetxt('../output/first_scan.csv', first_scan[None,:], delimiter=',')
#np.savetxt('../output/sat_first.csv', pts[satisfied[first_scan_index]], delimiter=',')
#np.savetxt('../output/visible_first.csv', pts[visible[first_scan_index]], delimiter=',')
## plan the second scan 
## set range among fninal_psl in the range 
min_next_range = 2200 # mm 
max_next_range = 3000 # mm

## plan Second scan
second_psl_index = set()
for a,psl_ in enumerate (final_psl):
    
    psl_x = psl_[0]
    psl_y = psl_[1]
    psl_z = psl_[2]  
    first_scan_x=first_scan[0]
    first_scan_y=first_scan[1]
    first_scan_z=first_scan[2]
    ## define the direction of potential scan points
      
    direction = (first_scan_x) * (psl_y) - (first_scan_y) * (psl_x)
    #print(direction)
    #if direction >1 : right  direction<1: left
    ## define the distnace from the scan assigned     
    dist = dist_2d(psl_x,first_scan_x,psl_y,first_scan_y)
    
    if np.all(dist > min_next_range/1000 and dist < max_next_range/1000) and direction > 1 :
        second_psl_index.add(a)
        
second_psl_index_list = list(second_psl_index)        
second_psl = final_psl[list(second_psl_index)]


# potential second_psls
#ax.scatter(second_psl[:,0],second_psl[:,1],second_psl[:,2], color = 'blue', alpha=0.1)

if len(second_psl_index_list)>2:
    
    overlap_length = {}
    for i in second_psl_index_list:
        a = set(visible[i])
        b = set(visible[first_scan_index])
        ab_intersection = a.intersection(b)
        #print(len(ab_indersection))
        overlap_length[i]=len(ab_intersection)
        second_index = max(overlap_length, key = overlap_length.get)
        
else: 
    second_index = second_psl_index 
        
second_psl = final_psl[second_index]    
np.savetxt('../output/second_scan.csv', second_psl[None,:], delimiter=',')
print(f'overlap ratio = {overlap_length[second_index]/len(satisfied[first_scan_index])}')
#np.savetxt('../output/sat_second.csv', pts[satisfied[second_index]], delimiter=',')
#np.savetxt('../output/visible_second.csv', pts[visible[second_index]], delimiter=',')
## plot second-scan possible positions 
ax.scatter(second_psl[0],second_psl[1],second_psl[2], color='blue')
ax.scatter(pts[:,0],pts[:,1],pts[:,2],color='grey')
plt.title('second psl')

print(f'dist to first scan (2) : {dist_2d(first_scan_x,second_psl[0],first_scan_y,second_psl[1])}')
dist_to_first = dist_2d(first_scan_x,second_psl[0],first_scan_y,second_psl[1])
if dist_to_first < 2.5 : 
    print(" planning set is ready")
else: 
    print("need another scan")

## plan Third scan
third_psl_index = set()
for a,psl_ in enumerate (final_psl):
    
    psl_x = psl_[0]
    psl_y = psl_[1]
    psl_z = psl_[2]  
    second_scan_x=final_psl[second_index][0]
    second_scan_y=final_psl[second_index][1]
    second_scan_z=final_psl[second_index][2]
    ## define the direction of potential scan points
      
    direction = (second_scan_x) * (psl_y) - (second_scan_y) * (psl_x)
    #print(direction)
    #if direction >1 : right  direction<1: left
    dist = dist_2d(psl_x,second_scan_x,psl_y,second_scan_y)
    
    if np.all(dist > min_next_range/1000 and dist < max_next_range/1000) and direction > 1 :
        third_psl_index.add(a)
third_psl_index_list = list(third_psl_index)        
third_psl = final_psl[list(third_psl_index)]

# potential third_psls
#ax.scatter(third_psl[:,0],third_psl[:,1],third_psl[:,2], color = 'purple', alpha=0.1)


overlap_length = {}
for i in third_psl_index_list:
    a = set(visible[i])
    b = set(visible[second_index])
    ab_intersection = a.intersection(b)
    #print(len(ab_indersection))
    overlap_length[i]=len(ab_intersection)

third_index = max(overlap_length, key = overlap_length.get)
third_psl = final_psl[third_index]    

print(f'overlap ratio = {overlap_length[third_index]/len(satisfied[second_index])}')
#np.savetxt('../output/third_scan.csv', third_psl[None,:], delimiter=',')
#np.savetxt('../output/sat_third.csv', pts[satisfied[third_index]], delimiter=',')
#np.savetxt('../output/visible_third.csv', pts[visible[third_index]], delimiter=',')
## plot third-scan possible positions 
ax.scatter(third_psl[0],third_psl[1],third_psl[2], color='purple')
ax.scatter(pts[:,0],pts[:,1],pts[:,2],color='grey')
plt.title('third psl')

print(f'dist to first scan (3) : {dist_2d(first_scan_x,third_psl[0],first_scan_y,third_psl[1])}')
dist_to_first = dist_2d(first_scan_x,third_psl[0],first_scan_y,third_psl[1])
if dist_to_first < 2.5 : 
    print(" planning set is ready")
else: 
    print("need another scan")
    
## plan Forth scan
forth_psl_index = set()
for a,psl_ in enumerate (final_psl):
    
    psl_x = psl_[0]
    psl_y = psl_[1]
    psl_z = psl_[2]  
    third_scan_x=final_psl[third_index][0]
    third_scan_y=final_psl[third_index][1]
    third_scan_z=final_psl[third_index][2]
    ## define the direction of potential scan points
      
    direction = (third_scan_x) * (psl_y) - (third_scan_y) * (psl_x)
    #print(direction)
    #if direction >1 : right  direction<1: left
    dist = dist_2d(psl_x,third_scan_x,psl_y,third_scan_y)
    
    if np.all(dist > min_next_range/1000 and dist < max_next_range/1000) and direction > 1 :
        forth_psl_index.add(a)
forth_psl_index_list = list(forth_psl_index)        
forth_psl = final_psl[list(forth_psl_index)]

# potential forth_psls
#ax.scatter(forth_psl[:,0],forth_psl[:,1],forth_psl[:,2], color = 'yellow', alpha=0.1)
overlap_length = {}
for i in forth_psl_index_list:
    a = set(visible[i])
    b = set(visible[third_index])
    ab_intersection = a.intersection(b)
    #print(len(ab_indersection))
    overlap_length[i]=len(ab_intersection)

forth_index = max(overlap_length, key = overlap_length.get)
forth_psl = final_psl[forth_index]    
#np.savetxt('../output/forth_scan.csv', forth_psl[None,:], delimiter=',')
print(f'overlap ratio = {overlap_length[forth_index]/len(satisfied[third_index])}')
#np.savetxt('../output/sat_forth.csv', pts[satisfied[forth_index]], delimiter=',')
#np.savetxt('../output/visible_forth.csv', pts[visible[forth_index]], delimiter=',')
## plot forth-scan possible positions 
ax.scatter(forth_psl[0],forth_psl[1],forth_psl[2], color='orange')
ax.scatter(pts[:,0],pts[:,1],pts[:,2],color='grey')

print(f'dist to first scan (4) : {dist_2d(first_scan_x,forth_psl[0],first_scan_y,forth_psl[1])}')

dist_to_first = dist_2d(first_scan_x,forth_psl[0],first_scan_y,forth_psl[1])
if dist_to_first < 2.5 : 
    print(" planning set is ready")
else: 
    print("need another scan")

## plan Fifth scan
fifth_psl_index = set()
for a,psl_ in enumerate (final_psl):
    
    psl_x = psl_[0]
    psl_y = psl_[1]
    psl_z = psl_[2]  
    forth_scan_x=final_psl[forth_index][0]
    forth_scan_y=final_psl[forth_index][1]
    forth_scan_z=final_psl[forth_index][2]
    ## define the direction of potential scan points
      
    direction = (forth_scan_x) * (psl_y) - (forth_scan_y) * (psl_x)
    #print(direction)
    #if direction >1 : right  direction<1: left
    dist = dist_2d(psl_x,forth_scan_x,psl_y,forth_scan_y)
    
    if np.all(dist > min_next_range/1000 and dist < max_next_range/1000) and direction > 1 :
        fifth_psl_index.add(a)
fifth_psl_index_list = list(fifth_psl_index)        
fifth_psl = final_psl[list(fifth_psl_index)]

#ax.scatter(fifth_psl[:,0],fifth_psl[:,1],fifth_psl[:,2], color = 'red', alpha=0.1)
overlap_length = {}
for i in fifth_psl_index_list:
    a = set(visible[i])
    b = set(visible[forth_index])
    ab_intersection = a.intersection(b)
    #print(len(ab_indersection))
    overlap_length[i]=len(ab_intersection)

fifth_index = max(overlap_length, key = overlap_length.get)
fifth_psl = final_psl[fifth_index]    
#np.savetxt('../output/fifth_scan.csv', fifth_psl[None,:], delimiter=',')
print(f'overlap ratio = {overlap_length[fifth_index]/len(satisfied[forth_index])}')
#np.savetxt('../output/sat_fifth.csv', pts[satisfied[fifth_index]], delimiter=',')
#np.savetxt('../output/sat_fifth.csv', pts[satisfied[fifth_index]], delimiter=',')
#np.savetxt('../output/visible_fifth.csv', pts[visible[fifth_index]], delimiter=',')
## plot forth-scan possible positions 
ax.scatter(fifth_psl[0],fifth_psl[1],fifth_psl[2], color='red')
ax.scatter(pts[:,0],pts[:,1],pts[:,2],color='grey')
plt.title('forth psl')
print(f'dist to first scan (5) : {dist_2d(first_scan_x,fifth_psl[0],first_scan_y,fifth_psl[1])}')

dist_to_first = dist_2d(first_scan_x,fifth_psl[0],first_scan_y,fifth_psl[1])
if dist_to_first < 2.5 : 
    print(" planning set is ready")
else: 
    print("need another scan")
    
## plan sixth scan
sixth_psl_index = set()
for a,psl_ in enumerate (final_psl):
    
    psl_x = psl_[0]
    psl_y = psl_[1]
    psl_z = psl_[2]  
    fifth_scan_x=final_psl[fifth_index][0]
    fifth_scan_y=final_psl[fifth_index][1]
    fifth_scan_z=final_psl[fifth_index][2]
    ## define the direction of potential scan points
      
    direction = (fifth_scan_x) * (psl_y) - (fifth_scan_y) * (psl_x)
    #print(direction)
    #if direction >1 : right  direction<1: left
    dist = dist_2d(psl_x,fifth_scan_x,psl_y,fifth_scan_y)
    
    if np.all(dist > min_next_range/1000 and dist < max_next_range/1000) and direction > 1 :
        sixth_psl_index.add(a)
sixth_psl_index_list = list(sixth_psl_index)        
sixth_psl = final_psl[list(sixth_psl_index)]

#ax.scatter(sixth_psl[:,0],sixth_psl[:,1],sixth_psl[:,2], color = 'black', alpha=0.1)
overlap_length = {}
for i in sixth_psl_index_list:
    a = set(visible[i])
    b = set(visible[fifth_index])
    ab_intersection = a.intersection(b)
    #print(len(ab_indersection))
    overlap_length[i]=len(ab_intersection)

sixth_index = max(overlap_length, key = overlap_length.get)
sixth_psl = final_psl[sixth_index]    
#np.savetxt('../output/sixth_scan.csv', sixth_psl[None,:], delimiter=',')
print(f'overlap ratio = {overlap_length[sixth_index]/len(satisfied[fifth_index])}')
##np.savetxt('../output/sat_sixth.csv', pts[satisfied[sixth_index]], delimiter=',')
#np.savetxt('../output/visible_sixth.csv', pts[satisfied[sixth_index]], delimiter=',')
## plot sixth-scan possible positions 
ax.scatter(sixth_psl[0],sixth_psl[1],sixth_psl[2], color='black')
ax.scatter(pts[:,0],pts[:,1],pts[:,2],color='grey')
plt.title('sixth psl')
print(f'dist to first scan (6) : {dist_2d(first_scan_x,sixth_psl[0],first_scan_y,sixth_psl[1])}')

dist_to_first = dist_2d(first_scan_x,sixth_psl[0],first_scan_y,sixth_psl[1])
if dist_to_first < 2.5 : 
    print(" planning set is ready")
else: 
    print("need another scan")



remove = np.concatenate((satisfied[first_scan_index],satisfied[second_index],satisfied[third_index],satisfied[forth_index],satisfied[fifth_index],satisfied[sixth_index]))
removed = np.delete(pts,remove,0)
#np.savetxt('../output/non_qualified.csv', removed, delimiter=',')
visible_remove = np.concatenate((visible[first_scan_index],visible[second_index],visible[third_index],visible[forth_index],visible[fifth_index],satisfied[sixth_index]))
removed = np.delete(pts,visible_remove,0)
#np.savetxt('../output/non_qualified.csv', removed, delimiter=',')

# =============================================================================
# ## plan seventh scan
# seventh_psl_index = set()
# for a,psl_ in enumerate (final_psl):
#     
#     psl_x = psl_[0]
#     psl_y = psl_[1]
#     psl_z = psl_[2]  
#     sixth_scan_x=final_psl[sixth_index][0]
#     sixth_scan_y=final_psl[sixth_index][1]
#     sixth_scan_z=final_psl[sixth_index][2]
#     ## define the direction of potential scan points
#       
#     direction = (sixth_scan_x) * (psl_y) - (sixth_scan_y) * (psl_x)
#     #print(direction)
#     #if direction >1 : right  direction<1: left
#     dist = dist_2d(psl_x,sixth_scan_x,psl_y,sixth_scan_y)
#     
#     if np.all(dist > min_next_range/1000 and dist < max_next_range/1000) and direction > 1 :
#         seventh_psl_index.add(a)
# seventh_psl_index_list = list(seventh_psl_index)        
# seventh_psl = final_psl[list(seventh_psl_index)]
# 
# ax.scatter(seventh_psl[:,0],seventh_psl[:,1],seventh_psl[:,2], color = 'cyan', alpha=0.1)
# overlap_length = {}
# for i in seventh_psl_index_list:
#     a = set(visible[i])
#     b = set(visible[sixth_index])
#     ab_intersection = a.intersection(b)
#     #print(len(ab_indersection))
#     overlap_length[i]=len(ab_intersection)
# 
# seventh_index = max(overlap_length, key = overlap_length.get)
# seventh_psl = final_psl[seventh_index]    
# np.savetxt('../output/seventh_scan.csv', seventh_psl[None,:], delimiter=',')
# print(f'overlap ratio = {overlap_length[seventh_index]/len(satisfied[sixth_index])}')
# 
# ## plot forth-scan possible positions 
# ax.scatter(seventh_psl[0],seventh_psl[1],seventh_psl[2], color='cyan')
# ax.scatter(pts[:,0],pts[:,1],pts[:,2],color='grey')
# plt.title('sixth psl')
# print(f'dist to first scan (7) : {dist_2d(first_scan_x,seventh_psl[0],first_scan_y,seventh_psl[1])}')
# dist_to_first = dist_2d(first_scan_x,seventh_psl[0],first_scan_y,seventh_psl[1])
# 
# if dist_to_first < 2.5 : 
#     print(" planning set is ready")
# else: 
#     print("need another scan")
#     
# ## plan eigth scan
# eighth_psl_index = set()
# for a,psl_ in enumerate (final_psl):
#     
#     
#     psl_x = psl_[0]
#     psl_y = psl_[1]
#     psl_z = psl_[2]  
#     seventh_scan_x=final_psl[seventh_index][0]
#     seventh_scan_y=final_psl[seventh_index][1]
#     seventh_scan_z=final_psl[seventh_index][2]
#     ## define the direction of potential scan points
#       
#     direction = (seventh_scan_x) * (psl_y) - (seventh_scan_y) * (psl_x)
#     #print(direction)
#     #if direction >1 : right  direction<1: left
#     dist = dist_2d(psl_x,seventh_scan_x,psl_y,seventh_scan_y)
#     
#     if np.all(dist > min_next_range/1000 and dist < max_next_range/1000) and direction > 1 :
#         eighth_psl_index.add(a)
# eighth_psl_index_list = list(eighth_psl_index)        
# eighth_psl = final_psl[list(eighth_psl_index)]
# 
# ax.scatter(eighth_psl[:,0],eighth_psl[:,1],eighth_psl[:,2], color = 'olive', alpha=0.1)
# overlap_length = {}
# for i in eighth_psl_index_list:
#     a = set(visible[i])
#     b = set(visible[seventh_index])
#     ab_intersection = a.intersection(b)
#     #print(len(ab_indersection))
#     overlap_length[i]=len(ab_intersection)
# 
# eighth_index = max(overlap_length, key = overlap_length.get)
# eighth_psl = final_psl[eighth_index]    
# np.savetxt('../output/eighth_scan.csv', eighth_psl[None,:], delimiter=',')
# print(f'overlap ratio = {overlap_length[eighth_index]/len(satisfied[seventh_index])}')
# 
# ## plot forth-scan possible positions 
# ax.scatter(eighth_psl[0],eighth_psl[1],eighth_psl[2], color='olive')
# ax.scatter(pts[:,0],pts[:,1],pts[:,2],color='grey')
# plt.title('sixth psl')
# print(f'dist to first scan (8) : {dist_2d(first_scan_x,eighth_psl[0],first_scan_y,eighth_psl[1])}')
# 
# dist_to_first = dist_2d(first_scan_x,eighth_psl[0],first_scan_y,eighth_psl[1])
# if dist_to_first < 2.5 : 
#     print(" planning set is ready")
# else: 
#     print("need another scan")
# 
# 
# ## plan nineth scan
# nineth_psl_index = set()
# for a,psl_ in enumerate (final_psl):
#     
#     psl_x = psl_[0]
#     psl_y = psl_[1]
#     psl_z = psl_[2]  
#     eighth_scan_x=final_psl[eighth_index][0]
#     eighth_scan_y=final_psl[eighth_index][1]
#     eighth_scan_z=final_psl[eighth_index][2]
#     ## define the direction of potential scan points
#     dist_to_first = dist_2d(first_scan_x,eighth_scan_x,first_scan_y,eighth_scan_y)
#     direction = (eighth_scan_x) * (psl_y) - (eighth_scan_y) * (psl_x)
#     #print(direction)
#     #if direction >1 : right  direction<1: left
#     dist = dist_2d(psl_x,eighth_scan_x,psl_y,eighth_scan_y)
#     
#     if np.all(dist > min_next_range/1000 and dist < max_next_range/1000) and direction > 1 and dist_to_first < 2.5 :
#         nineth_psl_index.add(a)
# nineth_psl_index_list = list(nineth_psl_index)        
# nineth_psl = final_psl[list(nineth_psl_index)]
# 
# ax.scatter(nineth_psl[:,0],nineth_psl[:,1],nineth_psl[:,2], color = 'pink', alpha=0.1)
# overlap_length = {}
# for i in nineth_psl_index_list:
#     a = set(visible[i])
#     b = set(visible[eighth_index])
#     ab_intersection = a.intersection(b)
#     #print(len(ab_indersection))
#     overlap_length[i]=len(ab_intersection)
# 
# nineth_index = max(overlap_length, key = overlap_length.get)
# nineth_psl = final_psl[nineth_index]    
# np.savetxt('../output/nineth_scan.csv', nineth_psl[None,:], delimiter=',')
# print(f'overlap ratio = {overlap_length[nineth_index]/len(satisfied[eighth_index])}')
# 
# ## plot forth-scan possible positions 
# ax.scatter(nineth_psl[0],nineth_psl[1],nineth_psl[2], color='pink')
# ax.scatter(pts[:,0],pts[:,1],pts[:,2],color='grey')
# plt.title('sixth psl')
# print(f'dist to first scan (9) : {dist_2d(first_scan_x,nineth_psl[0],first_scan_y,nineth_psl[1])}')
# 
# =============================================================================
plt.show()

print( f'processing time (module9) {time.time()-start_time} second')

