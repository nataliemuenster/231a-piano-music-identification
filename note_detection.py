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
	diff = cv2.subtract(frames[44],frames[49])
	cv2.imwrite("video_2-diff_ex.jpg", diff)