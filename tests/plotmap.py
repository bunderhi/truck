import matplotlib.pyplot as plt
import math
import numpy as np
import sys
from datastore import TubReader


# Vehicle parameters
LENGTH = 1.0 # 4.5  # [cm]
WIDTH =  0.1 #0.5  # [cm]
BACKTOWHEEL = 0.001 # 1.0  # [cm]
WHEEL_LEN =  0.3  # [cm]
WHEEL_WIDTH =  0.2  # [cm]
TREAD = 0.7  # [cm]
WB = 2.5  # [cm]

show_animation = True

def plot_car(x, y, yaw, steer=0.0, cabcolor="-r", truckcolor="-g"): 

    outline = np.array([[-BACKTOWHEEL, (LENGTH - BACKTOWHEEL), (LENGTH - BACKTOWHEEL), -BACKTOWHEEL, -BACKTOWHEEL],
                        [WIDTH / 2, WIDTH / 2, - WIDTH / 2, -WIDTH / 2, WIDTH / 2]])

    fr_wheel = np.array([[WHEEL_LEN, -WHEEL_LEN, -WHEEL_LEN, WHEEL_LEN, WHEEL_LEN],
                         [-WHEEL_WIDTH - TREAD, -WHEEL_WIDTH - TREAD, WHEEL_WIDTH - TREAD, WHEEL_WIDTH - TREAD, -WHEEL_WIDTH - TREAD]])

    rr_wheel = np.copy(fr_wheel)

    fl_wheel = np.copy(fr_wheel)
    fl_wheel[1, :] *= -1
    rl_wheel = np.copy(rr_wheel)
    rl_wheel[1, :] *= -1

    Rot1 = np.array([[math.cos(yaw), math.sin(yaw)],
                     [-math.sin(yaw), math.cos(yaw)]])
    Rot2 = np.array([[math.cos(steer), math.sin(steer)],
                     [-math.sin(steer), math.cos(steer)]])

    fr_wheel = (fr_wheel.T.dot(Rot2)).T
    fl_wheel = (fl_wheel.T.dot(Rot2)).T
    fr_wheel[0, :] += WB
    fl_wheel[0, :] += WB

    fr_wheel = (fr_wheel.T.dot(Rot1)).T
    fl_wheel = (fl_wheel.T.dot(Rot1)).T

    outline = (outline.T.dot(Rot1)).T
    rr_wheel = (rr_wheel.T.dot(Rot1)).T
    rl_wheel = (rl_wheel.T.dot(Rot1)).T

    outline[0, :] += x
    outline[1, :] += y
    fr_wheel[0, :] += x
    fr_wheel[1, :] += y
    rr_wheel[0, :] += x
    rr_wheel[1, :] += y
    fl_wheel[0, :] += x
    fl_wheel[1, :] += y
    rl_wheel[0, :] += x
    rl_wheel[1, :] += y
    print(np.array(outline[0, :]).flatten(),np.array(outline[1, :]).flatten())
    plt.plot(np.array(outline[0, :]).flatten(),
             np.array(outline[1, :]).flatten(), truckcolor)
    #plt.plot(np.array(fr_wheel[0, :]).flatten(),
    #         np.array(fr_wheel[1, :]).flatten(), truckcolor)
    #plt.plot(np.array(rr_wheel[0, :]).flatten(),
    #         np.array(rr_wheel[1, :]).flatten(), truckcolor)
    #plt.plot(np.array(fl_wheel[0, :]).flatten(),
    #         np.array(fl_wheel[1, :]).flatten(), truckcolor)
    #plt.plot(np.array(rl_wheel[0, :]).flatten(),
    #         np.array(rl_wheel[1, :]).flatten(), truckcolor)
    plt.plot(x, y, "*")


current_idx = 1
last_idx = 600
#reader=TubReader(path="/home/brian/Downloads/tub48")
reader=TubReader(path="/users/brian/Downloads/tub48")  
#img_array = None
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
    record = reader.run('pos/x','pos/y','pos/z','vel/x','vel/y','vel/z','rpy/roll','rpy/pitch','rpy/yaw')
    if record is not None:
        posx = record[0]
        posy = record[1]
        posz = record[2]
        velx = record[3]
        vely = record[4]
        velz = record[5]
        roll = record[6]
        pitch = record[7]
        yawstate = record[8]
        posx = posx * 100.0
        posz = posz * 100.0
        velx = velx * 100.0
        velz = velz * 100.0
    if current_idx == 1:
        x = [posz]
        y = [posx]
        yaw = [yawstate]
    # print (posx,posz,yawstate,velx,velz)
    current_idx += 1
    x.append(posz)
    y.append(posx)
    yaw.append(yawstate)

    if show_animation: 
        plt.cla()
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',
            lambda event: [exit(0) if event.key == 'escape' else None])
        plt.plot(x, y, "ob", label="trajectory")
        #plot_car(posz, posx, yawstate)
        plt.axis("equal")
        plt.grid(True)
        plt.title("Sample:" + str(current_idx)
                    + ", speed[m/s]:" + str(velx))
        #plt.pause(0.0001)
        plt.pause(0.1)