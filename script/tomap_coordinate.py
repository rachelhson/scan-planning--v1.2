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
""" change map => change origin"""
origin = [-0.381, 5.62]
matrix = [[cosine(90), -sine(90),origin[0]],
          [sine(90), cosine(90), origin[1]],
          [0,                0,         1]]

direction_matrix = [[cosine(180), -sine(180)],
                    [sine(180), cosine(180)]]

def get_theta(orientation, x ): # between normalvector and global y axis
    global_yaxis = [origin[0]-x,0] # map  x axis up
    theta_rad = np.arccos(np.dot(global_yaxis,orientation)/(np.linalg.norm(global_yaxis)*np.linalg.norm(orientation)))
    theta_deg = np.rad2deg(theta_rad)
    return theta_deg


def convert_theta_to_quaternion(theta):
    z = cosine(theta/2)
    w = sine(theta/2)
    return z,w
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
"""for applying transformation matrix """
ones = [[1] for _ in range(len(final_scanplan))]
final_scanplan = np.hstack((final_scanplan,ones))

## it converts to all map coordinates - which will be input in nav_test.py
for a,scan_pose in enumerate(final_scanplan):
    map_coord = np.dot(matrix, scan_pose)
    print(f'scan_{a}============================================================:')
    print(map_coord[:2])
    print(f'actuator_extend_time:')
    print(actuator_h[a])

    """ compute the angle between yaxis to scantoorigin"""
    vector_scan_to_origin = origin - map_coord[:2]
    theta = get_theta(vector_scan_to_origin, map_coord[0])
    print(f'direction :')
    print(vector_scan_to_origin)
    if vector_scan_to_origin[0] <0 and vector_scan_to_origin[1]<0:
        print(f"left {theta}")
        z,w = convert_theta_to_quaternion(theta)
        print(f"quaternion :"
              f"z :{z}"
              f"w :{w}")
    elif vector_scan_to_origin[0] <0 and vector_scan_to_origin[1]>0:
        print(f"right {theta+180}")
        z,w = convert_theta_to_quaternion(theta)
        print(f"quaternion :"
              f"z :{z}"
              f"w :{w}")
    elif vector_scan_to_origin[0]>0 and vector_scan_to_origin[1]>0:
        print(f"right {theta+180}")
        z,w = convert_theta_to_quaternion(theta)
        print(f"quaternion :"
              f"z :{z}"
              f"w :{w}")
    elif vector_scan_to_origin[0]>0 and vector_scan_to_origin[1]<0:
        print(f"left {theta}")
        z,w = convert_theta_to_quaternion(theta)
        print(f"quaternion :"
              f"z :{z}"
              f"w :{w}")







