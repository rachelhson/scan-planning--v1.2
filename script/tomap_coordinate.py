import numpy as np
from module2 import pt_normal
from module9 import final_scanplan, final_scanplan_index
import matplotlib.pyplot as plt
#final_scanplan = [[1,1,0],[2,1,1]]
fig, ax = plt.subplots()
# -----> y
# down x

def cosine(theta): #theta degree
    cos = np.cos(np.deg2rad(theta))
    return cos

def sine(theta): #theta degree
    sin = np.sin(np.deg2rad(theta))
    return sin

""" change map => change origin"""
origin = [-2.265, -0.915]
matrix = [[cosine(90), -sine(90),origin[0]],
          [sine(90), cosine(90), origin[1]],
          [0,                0,         1]]

direction_matrix = [[cosine(180), -sine(180)],
                    [sine(180), cosine(180)]]
ax.scatter(origin[0], origin[1])
def get_theta(orientation): # between normal vector and ROBOT FRAME Y AXIS
    global_yaxis = [0,1] # map  x axis up
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
    ax.scatter(map_coord[0],map_coord[1])
    """ compute the angle between yaxis to scantoorigin"""
    vector_scan_to_origin = origin - map_coord[:2]
    theta = get_theta(vector_scan_to_origin) # with respect to robot y axis frame
    print(f"theta: {theta}")

plt.show()








