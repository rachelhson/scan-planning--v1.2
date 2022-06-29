"""11-29-2020 Find next best view"""
from module2 import pts
from module4 import final_psl, dist_2d
from module6 import satisfied, distance,visible
from module8 import max_lowpoint_index

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import time

start_time = time.time()

min_next_range = 2200 # mm
max_next_range = 3000 # mm

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# for 2d
#ax = plt
"""first scan is defined from previous module - based on low-scored object points"""
first_scan_index = max_lowpoint_index
first_scan = final_psl[first_scan_index]
ax.scatter(first_scan[0], first_scan[1], first_scan[2], color='purple')

def get_nextscan(pre_scan,pre_scan_index):
    next_psl_index = set()
    for a, psl_ in enumerate(final_psl):
        psl_x, psl_y, psl_z = psl_[0], psl_[1], psl_[2]
        previous_scan_x, previous_scan_y, previous_scan_z =pre_scan[0],pre_scan[1],pre_scan[2]
        """ creating direction """
        direction = (previous_scan_x) * (psl_y) - (previous_scan_y) * (psl_x)
        dist = dist_2d(psl_x, previous_scan_x, psl_y, previous_scan_y)
        if np.all(dist > min_next_range / 1000 and dist < max_next_range / 1000) and direction > 1:
            next_psl_index.add(a)
    next_psl_index_list = list(next_psl_index)
    next_psl = final_psl[list(next_psl_index)]

    if len(next_psl_index_list) > 2:

        overlap_length = {}
        for i in next_psl_index_list:
            a = set(visible[i])
            b = set(visible[pre_scan_index])
            ab_intersection = a.intersection(b)
            # print(len(ab_indersection))
            overlap_length[i] = len(ab_intersection)
            next_index = max(overlap_length, key=overlap_length.get)

    else:
        next_index = next_psl_index

    next_psl = final_psl[next_index]
    ax.scatter(next_psl[0], next_psl[1], next_psl[2])


    dist_to_first = dist_2d(first_scan[0], next_psl[0], first_scan[1], next_psl[1])
    if dist_to_first < 2.5:
        print(" planning set is ready")
    else:
        print("need another scan")
    return next_psl, next_index, dist_to_first

second_scan, second_index, dist_to_first= get_nextscan(first_scan, first_scan_index)
third_scan, third_index, dist_to_first= get_nextscan(second_scan, second_index)

print(f'1 scan : {first_scan}')
print(f'1 scan index: {first_scan_index}')

print(f'2 scan : {second_scan}')
print(f'2 scan index: {second_index}')

print(f'3 scan : {third_scan}')
print(f'3 scan index: {third_index}')

scan_i = 3
pre_scan = third_scan
pre_index = third_index
final_scanplan = [first_scan,second_scan,third_scan]
final_scanplan_index = [first_scan_index,second_index,third_index]
print(f'final_scanplan : {final_scanplan}')
while dist_to_first > 2.5:
    next_scan, next_index, dist_to_first= get_nextscan(pre_scan, pre_index)
    scan_i = scan_i + 1
    print(f'{scan_i} scan : {next_scan}')
    print(f'{scan_i} scan index : {next_index}')
    pre_scan = next_scan
    pre_index = next_index
    final_scanplan.append(next_scan)
    final_scanplan_index.append(next_index)
ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], color='grey')
ax.grid(False)
plt.axis('off')
plt.show()
print(f'final_scanplan : {final_scanplan}')
print(f'final_scanplan : {final_scanplan_index}')
print( f'processing tiem (module9) {time.time()-start_time:.2f} second')

## wirte text file for final_scanplan & index
with open('final_scanplan.txt', 'w') as f:
    for item in final_scanplan:
        f.write("%s\n" % item)
    for index in final_scanplan_index:
        f.write("%s\n" % index)
    f.close()
