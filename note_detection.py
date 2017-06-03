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


def allFrameDiffs(frames):
	print "okay"
	print "frame type", type(frames[0])
	diff = cv2.subtract(frames[1],frames[0])
	cv2.imwrite("video_2-diff_ex.jpg", diff)
	##only rectify/preprocess every 5 frames to avoid extra work
	#NO!take top half of images, to get rid of hands
	#find the x coordinate wth the most white
	#look for where black turns to white, return that line to sarah (using threshold, get from range of intensity values)
	#Give Sarah the x (starting at 1/3 down from the top left side of image)