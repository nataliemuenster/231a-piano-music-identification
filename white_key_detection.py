import numpy as np
from scipy.misc import imread
import ffmpy
from ffmpy import FFmpeg
import cv2
import os
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def apply_Canny(im):

#   edges = cv2.Canny(im,100,200)
#somehow need to determine where the larger gaps are in order to detect where to split white gaps into two different white keys

def locate_key(key):

    #For each white key, determine which black key is closest to it

    #scale and translate region to fit the white key size, then remove the areas that overlap with black keys

    #dilate whte region by a structure element of 3x3 to cover more area as detecting changes in next section will need to detect changes around the keys as well
    d_kernel = np.ones((3,3),np.uint8)
    im_dilated = cv2.dilate(im_eroded,kernel,iterations = 1)

    #erode previously found black regions by a structured element of 5x5 to leave room between black and white keys
    im_eroded = cv2.erode(im,d_kernel,iterations = 1)
    e_kernel = np.ones((5,5),np.uint8)
