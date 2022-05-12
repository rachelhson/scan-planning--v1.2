import numpy as np
from module2 import pt_normal
from module9 import final_scanplan, final_scanplan_index
#final_scanplan = [[1,1,0],[2,1,1]]

# -----> y
# down x

def cosine(theta): #theta degree
    cos = np.cos(np.deg2rad(theta))
    return cos

def sine(theta): #theta degree
    sin = np.sin(np.deg2rad(theta))
    return sin

origin = [-0.381, 5.62]
matrix = [[cosine(90), -sine(90),origin[0]],
          [sine(90), cosine(90), origin[1]],
          [0,                0,         1]]
direction_matrix = [[cosine(180), -sine(180)],
                    [sine(180), cosine(180)]]

height = np.vstack(final_scanplan)[:,2]

actuator_h = []
for h in height:
    if h<1.0:
        actuator_extend_time = 0
        actuator_h.append([actuator_extend_time])
    elif h > 1.0 and h < 1.2:
        actuator_extend_time = 5
        actuator_h.append([actuator_extend_time])
    else:
        actuator_extend_time = 10
        actuator_h.append([actuator_extend_time])

final_scanplan = np.vstack(final_scanplan)[:,0:2]
"""for transformation matrix """
ones = [[1] for _ in range(len(final_scanplan))]
final_scanplan = np.hstack((final_scanplan,ones))

for a,scan_pose in enumerate(final_scanplan):
    map_coord = np.dot(matrix, scan_pose)
    print(f'scan_{a} :')
    print(map_coord[:2])
    print(f'actuator_extend_time:')
    print(actuator_h[a])
    print(f'normal vector:') # rotate normal vector 180 degree then it will be robot direction
    print(pt_normal[a][:2])
    print(f'robot direction:')
    orientation = np.dot(direction_matrix, pt_normal[a][:2])
    print(orientation)




