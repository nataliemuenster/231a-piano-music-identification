import numpy as np
from scipy.misc import imread
import ffmpy
from ffmpy import FFmpeg
import cv2
import os
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage.segmentation import clear_border
from skimage.morphology import label


def allFrameDiffs(images_dir):
	#loops through all the images in the video directory
    '''image_list = os.listdir(images_dir)
    images = []
    for img_name in image_list:
        img = cv2.imread(os.path.join(images_dir,img_name))
        name = ""
        if img is not None:
                img = img.astype(np.uint8)
                img = image_extraction.sobel(img)
                #print "img.shape", img.shape
                images.append(img)
    '''