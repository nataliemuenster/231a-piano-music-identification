import numpy as np
from scipy.misc import imread
import ffmpy
from ffmpy import FFmpeg
import cv2
import os
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import argparse
#import pymouse #SARAH YOU NEED TO INSTALL THIS PROBABLY


#change output image names according to each video

def get_frames(video_name):
	#print "Parse_video:", video
    video_path = "./data/videos/" + video_name + ".mp4"
    images_dir = "./data/" + video_name + "_images"

    #if not yet parsed, parse. Else just return images
	
    if not os.path.exists(images_dir):
        #os.mkdir(images_dir)
        #process video and put all frames in this dir
        print "Please extract the frames from the video using ffmpeg, then try again."
        quit()
    
    #loops through all the images in the video directory
    image_list = os.listdir(images_dir)
    frames = []
    frameNum = 0
    for img_name in image_list:
        img = cv2.imread(os.path.join(images_dir,img_name))
        if img is not None and frameNum%5 == 0: #we gather only every 5 frames
                img = img.astype(np.uint8)
                #img = image_extraction.sobel(img)
                frames.append(img)
        frameNum += 1
    return frames


#Takes in an image of a piano, asks for the 4 corner points, and returns the rectified and cropped image, with consistent ratios of size of black to white keys
def rectify_first(img, pts_src): #original base_img (img2 example is of size: 1280x720)
    #how to make a GUI to show first image and let user click corners:
    size = img.shape
    #pts_src = np.array([[0,303],[0,599],[1243,315],[1243,618]]).astype(float) #in x,y
    pts_src = pts_src.astype(float)
    pts_dst = np.array([[0,0],[0,size[0]],[size[1],0],[size[1],size[0]]]).astype(float) #in x,y
    #print "pts_src, pts_dst", pts_src, pts_dst
    
    h, status = cv2.findHomography(pts_src, pts_dst)
    img_rectified = cv2.warpPerspective(img, h, (size[1], size[0]))
    """
    cv2.imshow('image', img_rectified)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    
    #cv2.imwrite("video_2-0001_rectified.jpg", img_rectified)
    params = np.array([pts_src, pts_dst])
    return img_rectified, params

#rectifies and converts to greyscale all images
def rectify_all(frames, params):
    size = frames[0].shape
    for f in xrange(len(frames)):
        frame = cv2.cvtColor(frames[f], cv2.COLOR_RGB2GRAY)
        h, status = cv2.findHomography(params[0], params[1])
        frames[f] = cv2.warpPerspective(frame, h, (size[1], size[0]))
    return frames


def getBinaryImages(base_img):
    img_grey = cv2.cvtColor(base_img, cv2.COLOR_RGB2GRAY)
    #cv2.imwrite("video_2-0001_grey.jpg", img_grey)
    thresh, img_binary = cv2.threshold(img_grey, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #cv2.imwrite("video_2-0001_binary_no_sobel.jpg", img_binary)
    
    #now try applying Sobel first
    img_sobel = sobel(base_img)
    #cv2.imwrite("video_2-0001_sobel.jpg", img_sobel)
    #apply thresholding to binarize image: http://docs.opencv.org/2.4/doc/tutorials/imgproc/threshold/threshold.html
    thresh, img_binary_sobel = cv2.threshold(img_sobel, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    '''
    cv2.imshow('image', img_binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    cv2.imshow('image', img_binary_sobel)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    return img_binary_sobel, img_binary


#from https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/sobel.py
def sobel(img):
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
	return dst
