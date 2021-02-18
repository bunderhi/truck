import matplotlib.pyplot as plt
import math
import numpy as np
import sys
from datastore import TubReader


# Vehicle parameters
LENGTH = 4.5  # [cm]
WIDTH =  1.0  # [cm]
BACKTOWHEEL = 1.0  # [cm]

show_animation = True

def plot_car(x, y, yaw, steer=0.0, truckcolor="-g"): 

    outline = np.array([[-BACKTOWHEEL, (LENGTH - BACKTOWHEEL), (LENGTH - BACKTOWHEEL), -BACKTOWHEEL, -BACKTOWHEEL],
                        [WIDTH / 2, WIDTH / 2, - WIDTH / 2, -WIDTH / 2, WIDTH / 2]])

    Rot1 = np.array([[math.cos(yaw), math.sin(yaw)],
                     [-math.sin(yaw), math.cos(yaw)]])
    Rot2 = np.array([[math.cos(steer), math.sin(steer)],
                     [-math.sin(steer), math.cos(steer)]])

    outline = (outline.T.dot(Rot1)).T
    outline[0, :] += x
    outline[1, :] += y

    print(np.array(outline[0, :]).flatten(),np.array(outline[1, :]).flatten())
    plt.plot(np.array(outline[0, :]).flatten(),
             np.array(outline[1, :]).flatten(), truckcolor)

    plt.plot(x, y, "*")

def smooth_yaw(yaw):

    for i in range(len(yaw) - 1):
        dyaw = yaw[i + 1] - yaw[i]

        while dyaw >= math.pi / 2.0:
            yaw[i + 1] -= math.pi * 2.0
            dyaw = yaw[i + 1] - yaw[i]

        while dyaw <= -math.pi / 2.0:
            yaw[i + 1] += math.pi * 2.0
            dyaw = yaw[i + 1] - yaw[i]

    return yaw

current_idx = 1
last_idx = 600
reader=TubReader(path="/home/brian/Downloads/tub48")
#reader=TubReader(path="/users/brian/Downloads/tub48")  
#img_array = None
posx = None
posy = None
posz = None
velx = None
vely = None
velz = None
roll = None
pitch = None
yawrad = None
x = []
y = []
vx = []
vz = []
yaw = []

while last_idx > current_idx:
    record = reader.run('pos/x','pos/y','pos/z','vel/x','vel/y','vel/z','rpy/roll','rpy/pitch','rpy/yaw')
    if record is not None:
        posx = record[0] * 100.0
        posz = -record[2] * 100.0
        velx = record[3] * 100.0
        velz = -record[5] * 100.0
        yawd = record[8]
        yawrad = math.radians(yawd)
    # print (posx,posz,yawrad,velx,velz)
    current_idx += 1
    x.append(posz)
    y.append(posx)
    vz.append(velz)
    vx.append(velx)
    yaw.append(yawrad)

cyaw = smooth_yaw(yaw)


if show_animation: 
    xo = []
    yo = []
    yawo = []
    length = len(x)
    for i in range(length):
        xstate = x[i]
        ystate = y[i]
        yawstate = yaw[i]
        xo.append(xstate)
        yo.append(ystate)
        yawo.append(yawstate)
        if i > 5:
            plt.cla()
            # for stopping simulation with the esc key.
            plt.gcf().canvas.mpl_connect('key_release_event',
                lambda event: [exit(0) if event.key == 'escape' else None])
            plt.plot(xo[-5:], yo[-5:], "ob", label="trajectory")
            plot_car(xstate, ystate, yawstate)
            plt.axis("equal")
            plt.grid(True)
            plt.title("Sample:" + str(i)
                        + ", speed[m/s]:" + str(yawstate))
            #plt.pause(0.0001)
            plt.pause(0.1)