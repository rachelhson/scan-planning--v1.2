""" module 10 only for robotics operation """
import numpy as np

with open('final_scanplan.txt') as f:
    final_scanplan = f.readlines()

""" change to robot's available height """
height = np.vstack(final_scanplan)[:,2]
actuator_h = []
for h in height:
    if h<1.0:
        actuator_extend_time = 0 #25+62.3cm = 87.3 cm
        actuator_h.append([actuator_extend_time])
    elif h > 1.0 and h < 1.2:
        actuator_extend_time = 5 # 77.25+25 cm = 102.25 cm
        actuator_h.append([actuator_extend_time])
    else:
        actuator_extend_time = 10 # 92.5+25 cm = 117.5 cm
        actuator_h.append([actuator_extend_time])

