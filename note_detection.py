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

def allFrameDiffs(frames, key_width):
	print "okay"
	print "frame type", type(frames[0])
	x_coords = [] #np.empty((len(frames)-1, 1))
	height = frames[0].shape[0]
	width = frames[0].shape[1]
	crop_height = 2*height/3
	x_height = crop_height/2
	print "frame size:", frames[0][0:crop_height, :].shape
	for f1 in xrange(len(frames)-1): #loop over pairs of frames, already x frames apart
		crop_frame1 = frames[f1][0:crop_height, :]
		crop_frame2 = frames[f1+1][0:crop_height, :]
		#if f1 == 6:
		#	cv2.imwrite("video_2-cropped_indiff.jpg", crop_frame1)
		diff = cv2.subtract(crop_frame1,crop_frame2)
		#cv2.imwrite("video_2-cropped_diff" + str(f1) + ".jpg", diff)
		#x_coords
		key_xs = []
		pixel = 0
		#Simple/lazy version in which it may miss some keys pressed if black included, because incrementing by width of white (possibly too big)
		'''while pixel < width:
			while diff[int(x_height), pixel] > threshold:
				pixel += 1
			if pixel < width: #if reached end of image, don't simply append last pixel as a key
				key_xs.append(pixel)
		'''
		for x in xrange(len(diff[x_height,:])):
			if diff[x_height,x] >= threshold:

				print "diff image ", f1, "found at ", x, " : ", diff[x_height,x]
		#key_xs = [x for x in diff[x_height, :] if x > threshold]
		key_xs = np.where(diff[x_height, :] >= threshold)[0]#.nonzero()
		#eliminate duplicates? in list if they are too close to each other??
		#maybe take a sampling of two different y heights to see if it's just in black, or also white??
		print "keys x's for ", f1, " = ", key_xs
		x_coords.append(key_xs)
	return np.asarray(x_coords) #list of lists -- each index is a frame difference, which may have 0 or more keys pressed
	
	
	##only rectify/preprocess every 5 frames to avoid extra work
	#NO!take top half of images, to get rid of hands
	#find the x coordinate wth the most white
	#look for where black turns to white, return that line to sarah (using threshold, get from range of intensity values)
	#Give Sarah the x (starting at 1/3 down from the top left side of image)