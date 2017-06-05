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

threshold = 50

def allFrameDiffs(frames, black_key_width):
	x_coords = []
	height = frames[0].shape[0]
	width = frames[0].shape[1]
	crop_height = 2*height/3
	x_height = crop_height/2
	min_dist = black_key_width/2 #min distance between two valid different pressed keys (so same key not counted twice, but also so a black and neighboring white key can be detected)
	print "frame size:", frames[0][0:crop_height, :].shape
	for f1 in xrange(len(frames)-1): #loop over pairs of frames, already x frames apart
		crop_frame1 = frames[f1][0:crop_height, :]
		crop_frame2 = frames[f1+1][0:crop_height, :]
		#if f1 == 6:
		#	cv2.imwrite("video_2-cropped_indiff.jpg", crop_frame1)
		diff = cv2.subtract(crop_frame1,crop_frame2)
		#cv2.imwrite("video_2-cropped_diff" + str(f1) + ".jpg", diff)
		key_xs = []
		pixel = 0

		key_xs = [i for i,val in enumerate(diff[x_height, :]) if val > threshold]
		print "initial key_xs for ", f1, "=", key_xs
		#eliminate duplicates in list if they are too close to each other:
		if len(key_xs) > 1:
			for i in xrange(len(key_xs)-1, 0, -1): #iterate backwards
				if abs(key_xs[i] - key_xs[i-1]) < min_dist:
					key_xs.pop(i)#only keep first one found (is better way to average them??)

		#maybe take a sampling of two different y heights to see if it's just in black, or also white??
		print "filtered key_xs for ", f1, " = ", key_xs
		x_coords.append(key_xs)

	return np.asarray(x_coords) #list of lists -- each index is a frame difference, which may have 0 or more keys pressed
	
	
	##only rectify/preprocess every 5 frames to avoid extra work
	#NO!take top half of images, to get rid of hands
	#find the x coordinate wth the most white
	#look for where black turns to white, return that line to sarah (using threshold, get from range of intensity values)
	#Give Sarah the x (starting at 1/3 down from the top left side of image)