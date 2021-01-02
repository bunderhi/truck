import pyrealsense2 as rs
import numpy as np
import cv2
import os
from math import tan, pi
import datetime as dt
import time

"""
Returns a camera matrix K from librealsense intrinsics
"""
def camera_matrix(intrinsics):
    return np.array([[intrinsics.fx,             0, intrinsics.ppx],
                     [            0, intrinsics.fy, intrinsics.ppy],
                     [            0,             0,              1]])

"""
Returns the fisheye distortion from librealsense intrinsics
"""
def fisheye_distortion(intrinsics):
    return np.array(intrinsics.coeffs[:4])


pipe = rs.pipeline()

cfg = rs.config()
cfg.enable_stream(rs.stream.fisheye, 1)
cfg.enable_stream(rs.stream.fisheye, 2)

pipe.start(cfg)

# Retreive the stream and intrinsic properties for both cameras
profiles = pipe.get_active_profile()
streams = {"left"  : profiles.get_stream(rs.stream.fisheye, 1).as_video_stream_profile(),
           "right" : profiles.get_stream(rs.stream.fisheye, 2).as_video_stream_profile()}
intrinsics = {"left"  : streams["left"].get_intrinsics(),}

# Print information about both cameras
print("Left camera:",  intrinsics["left"])

# Translate the intrinsics from librealsense into OpenCV
K_left  = camera_matrix(intrinsics["left"])
D_left  = fisheye_distortion(intrinsics["left"])

print("camera_matrix:", K_left)
print("distortion:",D_left)


(width, height) = (intrinsics["left"].width, intrinsics["left"].height)

print("camera image size:",width, height)

pipe.stop()
