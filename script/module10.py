""" module 10 only for robotics operation """
import numpy as np

with open('final_scanplan.csv','r') as f:
    final_scanplan = csv.reader(f)
print(final_scanplan)
""" change to robot's available height """
height = np.vstack(final_scanplan)[:,2]
actuator_h = []
for count,h in enumerate(height):
    if h<1.0:
        # actuator height
        actuator_height = 0.873#m
    elif h > 1.0 and h < 1.2:
        #actuator height
        actuator_height = 1.0225#m
    else:
        actuator_height = 1.175#m
    final_scanplan[count][2] = actuator_height

print(f"changed final_scanplan:")
print(final_scanplan)
