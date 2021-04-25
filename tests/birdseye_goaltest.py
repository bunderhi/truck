"""
Script to test goal setting
Usage:
    goaltest.py  [--in=<image_pth>] [--out=<image_pth>] 

Options:
    -i --in=<image_pth>   Path to find the raw image [default: /home/brian/Downloads/labels]
    -o --out=<image_pth>  Path to put the processed image [default: /home/brian/Downloads/train_data/Masks]

"""
from docopt import docopt
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt  

def camera_matrix(intrinsics):
    """
    Returns a camera matrix K from librealsense intrinsics
    """
    return np.array([[intrinsics["fx"],             0, intrinsics["ppx"]],
                     [            0, intrinsics["fy"], intrinsics["ppy"]],
                     [            0,             0,              1]])

def fisheye_distortion(intrinsics):
    """
    Returns the fisheye distortion from librealsense intrinsics
    """
    return np.array(intrinsics["coeffs"][:4])

def reverse(self,img):
    """
    Reverse the preprocessing performed on an image 
    """
    original = np.zeros((800,848,3),dtype=np.uint8)
    img = cv2.resize(img,None,fx=2.0,fy=2.0,interpolation=cv2.INTER_AREA)
    original[230:550, 130:770] = img
    return original

def undistort(img):    
    """
    Perform a fisheye undistort  
    """
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

def reverse(img):
    """
    Reverse the preprocessing performed on an image 
    """
    print(img.shape)
    original = np.zeros((800,848,3),dtype=np.uint8)
    img = cv2.resize(img,None,fx=2.0,fy=2.0,interpolation=cv2.INTER_AREA)
    print(img.shape)
    original[230:550, 130:770] = img
    return original

def markup(img):
    cv2.rectangle(img,(130,230),(770,550),(0,255,0),2)
    return img

def imgpolygon(img):    
    
    pts = np.array([[371,455],[337,550],[472,472],[538,548]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(img,[pts],True,(255,255,0))
    return img

def realpolygon(img):    
    pts = np.array([[27,65],[73,314],[133,194],[133,314]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(img,[pts],True,(0,255,255))
    return img

def warpperspective(img):
    """
    Create a birdseye view from image 
    """
    #srcpts = np.float32([[394,473],[337,550],[472,472],[540,548]]) # mat pts
    #dstpts = np.float32([[73,194],[73,314],[133,194],[133,314]])
    srcpts = np.float32([[371,455],[337,550],[472,472],[538,548]])  # mat + banister pts
    dstpts = np.float32([[27,65],[73,314],[133,194],[133,314]])
    M = cv2.getPerspectiveTransform(srcpts,dstpts)
    dst = cv2.warpPerspective(img,M,(200,400))

    red = [0,255,0]

    return dst

def draw_text(
        img,
        *,
        text,
        uv_top_left,
        color=(255, 255, 255),
        fontScale=0.5,
        thickness=1,
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        outline_color=(0, 0, 0),
        line_spacing=1.5,
    ):
        """
        Draws multiline with an outline.
        """
        assert isinstance(text, str)

        uv_top_left = np.array(uv_top_left, dtype=float)
        assert uv_top_left.shape == (2,)

        for line in text.splitlines():
            (w, h), _ = cv2.getTextSize(
                text=line,
                fontFace=fontFace,
                fontScale=fontScale,
                thickness=thickness,
            )
            uv_bottom_left_i = uv_top_left + [0, h]
            org = tuple(uv_bottom_left_i.astype(int))

            if outline_color is not None:
                cv2.putText(
                    img,
                    text=line,
                    org=org,
                    fontFace=fontFace,
                    fontScale=fontScale,
                    color=outline_color,
                    thickness=thickness * 3,
                    lineType=cv2.LINE_AA,
                )
            cv2.putText(
                img,
                text=line,
                org=org,
                fontFace=fontFace,
                fontScale=fontScale,
                color=color,
                thickness=thickness,
                lineType=cv2.LINE_AA,
            )

            uv_top_left += [0, h * line_spacing]


def main(filename,out_path):
    
    fill = np.zeros((2,800,848),dtype=np.uint8)

    mask_folder = '/home/brian/projects/truck/tests'
    mask = cv2.imread(os.path.join(mask_folder,filename))
    
    assert mask is not None

    red = reverse(mask)
    print(red.shape)

    redm = cv2.cvtColor(red,cv2.COLOR_RGB2GRAY).reshape(1,800,848)*255
    redmask = np.vstack((fill,redm)).transpose(1,2,0)
    undistorted = undistort(redmask)
    birdseye_img = warpperspective(undistorted)


    plt.subplot(131),plt.imshow(birdseye_img),plt.title('Original')
    #plt.subplot(132),plt.imshow(undistorted),plt.title('Undistorted')
    #plt.subplot(133),plt.imshow(markup_img),plt.title('Birdseye')
    plt.show()
    cv2.imwrite(out_path,birdseye_img) 

if __name__ == '__main__':

    args = docopt(__doc__,version='goaltest version 1.0')
    # print(args)
    main(args['--in'],args['--out'])