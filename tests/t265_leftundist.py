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
#cfg.enable_stream(rs.stream.fisheye, 2)

pipe.start(cfg)

# Retreive the stream and intrinsic properties for both cameras
profiles = pipe.get_active_profile()
streams = {"left"  : profiles.get_stream(rs.stream.fisheye, 1).as_video_stream_profile(),}
 #           "right" : profiles.get_stream(rs.stream.fisheye, 2).as_video_stream_profile()}
intrinsics = {"left"  : streams["left"].get_intrinsics(),}

# Print information about both cameras
print("Left camera:",  intrinsics["left"])
print("Right camera:", intrinsics["right"])

# Translate the intrinsics from librealsense into OpenCV
K_left  = camera_matrix(intrinsics["left"])
D_left  = fisheye_distortion(intrinsics["left"])

(width, height) = (intrinsics["left"].width, intrinsics["left"].height)

R_left = np.eye(3)

P_left = np.array([[stereo_focal_px, 0, stereo_cx, 0],
                    [0, stereo_focal_px, stereo_cy, 0],
                    [0,               0,         1, 0]])



m1type = cv2.CV_32FC1
(lm1, lm2) = cv2.fisheye.initUndistortRectifyMap(K_left, D_left, R_left, P_left, stereo_size, m1type)

undistort_rectify = {"left"  : (lm1, lm2),}


try:
    for i in range(200):
        frames = pipe.wait_for_frames()

        left = frames.get_fisheye_frame(1)
        left_data = np.asanyarray(left.get_data())
        
        #right = frames.get_fisheye_frame(2)


        left_undistorted = cv2.remap(src = left_data,
                                       map1 = undistort_rectify["left"][0],
                                       map2 = undistort_rectify["left"][1],
                                       interpolation = cv2.INTER_LINEAR)

        color_image = cv2.cvtColor(left_undistorted[:,max_disp:], cv2.COLOR_GRAY2RGB)

        #cv2.imshow(WINDOW_TITLE, np.hstack((color_image, disp_color)))
        #if mode == "overlay":
        #    ind = disparity >= min_disp
        #    color_image[ind, 0] = disp_color[ind, 0]
        #    color_image[ind, 1] = disp_color[ind, 1]
        #    color_image[ind, 2] = disp_color[ind, 2]
        #    cv2.imshow(WINDOW_TITLE, color_image)
        #cv2.waitKey(500)

finally:
    pipe.stop()
    f.close()
    print('end')