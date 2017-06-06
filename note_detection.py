
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
pixel_buffer = 5

def allFrameDiffs(video_name, size, black_key_width):
	images_dir = "./data/" + video_name + "_rectified" #using the rectified images
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
		#print "initial key_xs for ", f1, "=", key_xs
		#eliminate duplicates in list if they are too close to each other:
		if len(key_xs) > 1:
			for i in xrange(len(key_xs)-1, 0, -1): #iterate backwards
				if abs(key_xs[i] - key_xs[i-1]) < min_dist:
					key_xs.pop(i)#only keep first one found (is better way to average them??)

        #maybe take a sampling of two different y heights to see if it's just in black, or also white??
		#print "filtered key_xs for ", f1-1, " = ", key_xs
		prev_crop = curr_crop
		x_coords[f1-1] = key_xs
	#print "x_coords:", x_coords
	x_coords = list(filter(None, x_coords))
	return x_coords #list of lists -- each index is a frame difference, which may have 0 or more keys pressed


def map_to_key(x_coords, whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes):

    #notes = []
    for i in range(0, x_coords.shape[0]):
        frame_x_coords = x_coords[i]
        
        for j in range(0, frame_x_coords.shape[0]):
            x = frame_x_coords[j] + pixel_buffer

            #check if there is  black key that covers this region
            #black_key = blackKeys[np.where(blackKeys[2, :] < x and blackKeys[3, :] > x)]
            print "x ", x
            #print "blackKeys[2, :] ", blackKeys[:, 2]
            
            # print "blackKeys[3, :] ", blackKeys[:, 3]
            """
            print "np.where(blackKeys[2, :] < x)[0] ", np.where(blackKeys[:, 2] < x)[0]
            print "np.where(blackKeys[3, :] > x)[0] ", np.where(blackKeys[:, 3] > x)[0]
            print "blackKeys[3, :] ", blackKeys[3, :]
            print "blackKeys[4, :] ", blackKeys[4, :]
            """

            index = np.intersect1d(np.where(blackKeys[:, 2] < x)[0], np.where(blackKeys[:, 3] > x)[0])

            if len(index) != 0:
                note = black_notes[index[0]] + " sharp"
                print note
                break
            else:
                
                print "np.where(whiteKeys[2, :] < x)[0] ", np.where(whiteKeys[19, 2] < x)[0]
                print "np.where(whiteKeys[3, :] > x)[0] ", np.where(whiteKeys[19, 3] > x)[0]
                print "whiteKeys[19, :] ", whiteKeys[19, :]
                print "whiteKeys[20, :] ", whiteKeys[20, :]
                #print "whiteKeys ", whiteKeys
                

                #if it matches no black key it must be a white key
                index = np.intersect1d(np.where(whiteKeys[:, 2] < x)[0], np.where(whiteKeys[:, 3] > x)[0])
                print "index ", index

                if len(index) == 0:
                    print "could not detect note"
                
                else:
                    note = white_notes[index[0]]
                    #notes.append(note)
                    print note

	##only rectify/preprocess every 5 frames to avoid extra work
	#NO!take top half of images, to get rid of hands
	#find the x coordinate wth the most white
	#look for where black turns to white, return that line to sarah (using threshold, get from range of intensity values)
	#Give Sarah the x (starting at 1/3 down from the top left side of image)
