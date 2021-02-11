import matplotlib.pyplot as plt
import math
import numpy as np
import sys
from datastore import TubReader

current_idx = 1
last_idx = 400
reader=TubReader(path="/home/brian/Downloads/tub48")
    
img_array = None
posx = None
posy = None
posz = None
velx = None
vely = None
velz = None
roll = None
pitch = None
yaw = None

while last_idx > current_idx:
    record = reader.run('cam/image1','pos/x','pos/y','pos/z','vel/x','vel/y','vel/z','rpy/roll','rpy/pitch','rpy/yaw')
    if record is not None:
        img_array = record[0]
        posx = record[1]
        posy = record[2]
        posz = record[3]
        velx = record[4]
        vely = record[5]
        velz = record[6]
        roll = record[7]
        pitch = record[8]
        yaw = record[9]

    print (posx,posy,posz,yaw,roll,pitch)
    current_idx += 1

    