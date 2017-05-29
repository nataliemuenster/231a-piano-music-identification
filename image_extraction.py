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
	#In command line I used: "ffmpeg  -r 30 -i ./videos/video_2.mp4 -qscale:v 2 -f image2 video_2-%04d.jpg"

    #not quite the same: ffmpeg  -r 30 -i ../video_2.mp4 -qscale:v 2 -f image2 video_2-%04d.jpg

    #We should definitely look into this to crop https://video.stackexchange.com/questions/4563/how-can-i-crop-a-video-with-ffmpeg

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
