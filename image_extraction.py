import numpy as np
from scipy.misc import imread
import ffmpy
from ffmpy import FFmpeg
import cv2
import os
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#def get_video -- let's just manually input urls for now when we want to extract a video

#change output image names according to each video
def parse_video(video):
	print "Parse_video:", video
	return
	#In command line I used: "ffmpeg  -r 30 -i ../video_1.mp4 -qscale:v 2 -f image2 video_1-%04d.jpg"

	#If we need to include this parsing in our code, here is how to do it in python:
	#ff = ffmpy.FFmpeg(inputs={"ffmpeg -r 30 -i video_1.mp4 -f image2 video_1-%d.jpg"}, outputs={})


#from https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/sobel.py
def sobel(img): #one at a time? or do all at once?
	scale = 1
	delta = 0
	ddepth = cv2.CV_16S

	#img = cv2.imread(img)
	img = cv2.GaussianBlur(img,(3,3),0) #idk what these numbers mean
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	# Gradient-X
	grad_x = cv2.Sobel(gray,ddepth,1,0, ksize = 3, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)
	#grad_x = cv2.Scharr(gray,ddepth,1,0)

	# Gradient-Y
	grad_y = cv2.Sobel(gray,ddepth,0,1, ksize = 3, scale = scale, delta = delta, borderType = cv2.BORDER_DEFAULT)
	#grad_y = cv2.Scharr(gray,ddepth,0,1)

	abs_grad_x = cv2.convertScaleAbs(grad_x)   # converting back to uint8
	abs_grad_y = cv2.convertScaleAbs(grad_y)

	dst = cv2.addWeighted(abs_grad_x,0.5,abs_grad_y,0.5,0)

	#cv2.imshow("cropped", crop_img)
	#cv2.waitKey(0)
	return dst


def compute_gradient(im):
    H, W = im.shape
    xgrad = np.zeros((H-2, W-2))
    ygrad = np.zeros((H-2, W-2))
    
    xgrad = im[1:-1, :-2] - im[1:-1, 2:]
    ygrad = im[:-2, 1:-1] - im[2:, 1:-1]
    
    angles = np.arctan2(ygrad, xgrad)
    angles[angles < 0] += math.pi
    angles = np.degrees(angles)
    magnitudes = np.sqrt(xgrad ** 2 + ygrad ** 2)
    return angles, magnitudes


def generate_histogram(angles, magnitudes, nbins = 9):
    histogram = np.zeros(nbins)
    
    bin_size = float(180 / nbins)
    
    # iterate over the pixels
    for h in xrange(angles.shape[0]):
        for w in xrange(angles.shape[1]):
            ang = angles[h,w]
            mag = magnitudes[h,w]
            
            if ang >= 180:
                ang = ang - 180
            
            # interpolate the votes
            lower_idx = int(ang / bin_size) - 1
            upper_idx = lower_idx + 1
            
            lower_ang = lower_idx * bin_size + 90/nbins
            upper_ang = upper_idx * bin_size + 90/nbins
            
            # Account for edge case
            if upper_idx >= nbins:
                upper_idx = 0
            if lower_idx < 0:
                lower_idx = nbins - 1
            
            lower_diff= abs(ang - lower_ang)
            upper_diff = abs(ang - upper_ang)
            lower_percent = upper_diff/ bin_size
            upper_percent = lower_diff/ bin_size
            histogram[lower_idx] += lower_percent * mag
            histogram[upper_idx] += upper_percent * mag
    
    return histogram



def compute_hog_features(im, pixels_in_cell, cells_in_block, nbins):
    height = im.shape[0] - 2
    width = im.shape[1] - 2
    
    angles, magnitudes = compute_gradient(im)
    
    total_cells_in_block = cells_in_block * pixels_in_cell
    stride = total_cells_in_block / 2
    features = np.zeros((int(math.floor(height / stride)) - 1,
                         int(math.floor(width / stride)) - 1,
                         nbins * cells_in_block * cells_in_block))
        
                         # iterate over the blocks, 50% overlap
    for w in xrange(0, width - total_cells_in_block, stride):
        for h in xrange(0, height - total_cells_in_block, stride):
            block_features = np.zeros((cells_in_block, cells_in_block,  nbins))
            block_magnitude = magnitudes[h:h+total_cells_in_block, w:w+total_cells_in_block]
            block_angle = angles[h:h+total_cells_in_block, w:w+total_cells_in_block]
            #  iterate over the cells
            for i in xrange(cells_in_block):
                for j in xrange(cells_in_block):
                    cell_magnitudes = block_magnitude[i * pixels_in_cell:(i+1)
                                        * pixels_in_cell,
                                        j*pixels_in_cell:(j+1)*pixels_in_cell]
                    cell_angles = block_angle[i * pixels_in_cell:(i+1) * pixels_in_cell,
                                        j*pixels_in_cell:(j+1)*pixels_in_cell]
                    block_features[i,j,:] = generate_histogram(cell_angles, cell_magnitudes, nbins)
                                                                 
            block_features = block_features.flatten()
            block_features = block_features \
                / np.sqrt(np.linalg.norm(block_features) ** 2 + .01)
            features[int(math.ceil(h/(stride))),
            int(math.ceil(w/(stride))),:] = block_features
                                                                         
    return features

# Displays the HoG features next to the original image
def plot_img_with_bbox(im, bbox, title_text = None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for i in range(bbox.shape[0]):
        ax.add_patch(
            patches.Rectangle(
                (bbox[i,0], bbox[i,1]),
                bbox[i,2],
                bbox[i,3],
                fill=False,
                edgecolor='red'
            )
        )
    plt.imshow(im, 'gray')
    if title_text is not None:
        plt.title(title_text)

