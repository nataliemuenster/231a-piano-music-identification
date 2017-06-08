
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

threshold = 40
pixel_buffer = 5

def allFrameDiffs(video_name, size, black_key_width):
	images_dir = "./data/" + video_name + "_rectified"
	image_list = os.listdir(images_dir)
	
	x_coords = [None]*len(image_list)
	height = size[0]
	width = size[1]
	crop_height = 2*height/3
	x_height = crop_height/2
	min_dist = black_key_width/2 #min distance between two valid different pressed keys (so same key not counted twice, but also so a black and neighboring white key can be detected)
	
	frameNum = 0
	prev_frame = cv2.imread(os.path.join(images_dir,image_list[0]), cv2.IMREAD_GRAYSCALE) #first image
	prev_crop = prev_frame[0:crop_height, :]
    
    #loop over pairs of frames, already x frames apart
	for f1 in xrange(1, len(image_list)):
		curr_frame = cv2.imread(os.path.join(images_dir,image_list[f1]), cv2.IMREAD_GRAYSCALE)
		curr_crop = curr_frame[0:crop_height, :]
		
		diff = cv2.subtract(prev_crop, curr_crop)
		key_xs = []
		pixel = 0

		key_xs = [i for i,val in enumerate(diff[x_height, :]) if val > threshold]
		#eliminate duplicates in list if they are too close to each other:
		if len(key_xs) > 1:
			for i in xrange(len(key_xs)-1, 0, -1): #iterate backwards
				if abs(key_xs[i] - key_xs[i-1]) < min_dist:
					key_xs.pop(i) #only keep first one found (current method for averaging)

		prev_crop = curr_crop
		x_coords[f1-1] = key_xs
	x_coords = list(filter(None, x_coords))
	return x_coords #list of lists -- each index is a frame difference, which may have 0 or more keys pressed


def map_to_key(x_coords, whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes):

    notes = []
    for i in range(0, len(x_coords)):
        frame_x_coords = x_coords[i]
        simultaneous_notes = []
        for j in range(0, len(frame_x_coords)):
            x = frame_x_coords[j] + pixel_buffer
            index = np.intersect1d(np.where(blackKeys[:, 2] < x)[0], np.where(blackKeys[:, 3] > x)[0])

            if len(index) != 0: #if there is a black key region that matches
                note = black_notes[index[0]]
                simultaneous_notes.append(note)
                break
            else:
                #if it matches no black key it must be a white key
                index = np.intersect1d(np.where(whiteKeys[:, 2] < x)[0], np.where(whiteKeys[:, 3] > x)[0])
                
                if len(index) == 0: #if there is no region that matches (falls in a gap region)
                    simultaneous_notes.append("x")
                
                else: #if there is a white key region that matches
                    note = white_notes[index[0]]
                    simultaneous_notes.append(note)
        notes.append(simultaneous_notes)

    #print notes, len(notes)
    return notes
