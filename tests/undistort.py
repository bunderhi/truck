"""
Script to perfrom a fisheye correction 

Usage:
    undistort.py  [--in=<image_pth>] [--out=<image_pth>] 

Options:
    -i --in=<image_pth>   Path to find the raw image [default: /home/brian/Downloads/labels]
    -o --out=<image_pth>  Path to put the processed image [default: /home/brian/Downloads/train_data/Masks]

"""
from docopt import docopt
import numpy as np
import cv2
import os

"""
Returns a camera matrix K from librealsense intrinsics
"""
def camera_matrix(intrinsics):
    return np.array([[intrinsics["fx"],             0, intrinsics["ppx"]],
                     [            0, intrinsics["fy"], intrinsics["ppy"]],
                     [            0,             0,              1]])

"""
Returns the fisheye distortion from librealsense intrinsics
"""
def fisheye_distortion(intrinsics):
    return np.array(intrinsics["coeffs"][:4])

def undistort(img):    
    
    leftcam = {
    "width": 848,
    "height": 800, 
    "ppx": 432.782, "ppy": 406.656, 
    "fx": 285.247, "fy": 286.178, 
    "model": 5, 
    "coeffs": [-0.00460218, 0.0404374, -0.0388418, 0.00706689, 0]
    }

    # Translate the intrinsics from librealsense into OpenCV
    K  = camera_matrix(leftcam)
    D  = fisheye_distortion(leftcam)
    DIM = (leftcam["width"], leftcam["height"])
    print("camera_matrix:", K)
    print("distortion:",D)
    print("camera:", DIM)
   
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_32FC1)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)    
    return undistorted_img 

def main(img_path,out_path):
    
    #img_path = '/home/brian/cam1/605_cam-image1_.jpg'
    #out_path = '/home/brian/sample01mask.jpg'

    img = cv2.imread(img_path)
    assert img is not None,"File:"+img_path+" not loaded"

    undistorted_img = undistort(img)
    cv2.imwrite(out_path,undistorted_img) 

if __name__ == '__main__':

    args = docopt(__doc__,version='undistort version 1.0')
    # print(args)
    main(args['--in'],args['--out'])