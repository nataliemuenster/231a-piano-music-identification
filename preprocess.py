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
    for img_name in image_list:
        img = cv2.imread(os.path.join(images_dir,img_name))
        if img is not None:
                img = img.astype(np.uint8)
                #img = image_extraction.sobel(img)
                frames.append(img)
    return frames

#https://stackoverflow.com/questions/25521120/store-mouse-click-event-coordinates-with-matplotlib
#display image and record where user clicks to get corners of keyboard
def get_corners(img_loc, size): #img_loc is the path to get the image
    #display image so user will be able to click
    img = imread(img_loc)
    fig = plt.figure()
    
    #img = mpimg.imread(img_loc)
    #plt.imshow(img)
    plt.imshow(img)
    print "gets here"

    coords = []

    def onclick(event):
        print "in event function"
        global ix, iy
        ix, iy = event.xdata, event.ydata
        print 'x = %d, y = %d'%(
            ix, iy)

        global coords
        coords.append([ix, iy])

        if len(coords) == 4: #we want 4 coordinates
            
            fig.canvas.mpl_disconnect(cid)

        
    #this connects mouse event to onclick function
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    print cid
    #can access coords now through global
    #Later postprocess points so we know which corner is which and return in correct order


#FAILED ATTEMPT TO WORK WITH OPENCV -- some problem with the version, I can't seem to fix it.
#GUI to let the user pick the corners of the keyboard from the initial image
'''def get_coord(event,x,y,flags,param):
    global refPt
    corners = np.array([[0,0],[0,0],[0,0],[0,0]]) #in x,y
    if event ==  cv2.EVENT_LBUTTONCLK: #cv2.EVENT_LBUTTONDOWN:
        refPt = [x,y]
'''

#https://stackoverflow.com/questions/23596511/how-to-save-mouse-position-in-variable-using-opencv-and-python
'''def get_corners(img, size):
    corners = []
    #Create a window and bind the function to window
    

    #cv2.namedWindow('image')
    cv2.setMouseCallback('Choose keyboard corners', get_coord)#, img)

    while(len(corners) < 4): #get the 4 corners
        cv2.imshow('Choose keyboard corners',img)
        
        #self.pressedkey=cv2.waitKey(0)
        # Wait for ESC key to exit
        #if self.pressedkey==27:
        #    cv2.destroyAllWindows()
        if self.pressedkey == 13: #if enter pressed
            corners.append(refPt)

    cv2.destroyAllWindows()
    print "corners:", corners
'''


#Takes in an image of a piano, asks for the 4 corner points, and returns the rectified and cropped image, with consistent ratios of size of black to white keys
def rectify_first(img): #original base_img (img2 example is of size: 1280x720)
    #how to make a GUI to show first image and let user click corners:
    #size = img.shape
    
    corners = get_corners("./data/video_2_images/video_2-0001.jpg", size)
    pts_src = np.array([[0,303],[0,599],[1243,315],[1243,618]]).astype(float) #in x,y
    pts_dst = np.array([[0,0],[0,size[0]],[size[1],0],[size[1],size[0]]]).astype(float) #in x,y
    #print "pts_src, pts_dst", pts_src, pts_dst
    
    h, status = cv2.findHomography(pts_src, pts_dst)
    img_rectified = cv2.warpPerspective(img, h, (size[1], size[0]))
    #cv2.imwrite("video_2-0001_rectified.jpg", img_rectified)
    params = np.array([pts_src, pts_dst])
    return img_rectified, params

#rectifies and converts to greyscale all images
def rectify_all(frames, params):
    for frame in frames:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        h, status = cv2.findHomography(params[0], params[1])
        frame = cv2.warpPerspective(frame, h, (size[1], size[0]))
    return frames


def getLines(base_img): #img is the base_image without hands in it
    img_grey = cv2.cvtColor(base_img, cv2.COLOR_RGB2GRAY)
    #cv2.imwrite("video_2-0001_grey.jpg", img_grey)
    thresh, img_binary = cv2.threshold(img_grey, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #cv2.imwrite("video_2-0001_binary_no_sobel.jpg", img_binary)

    #now try applying Sobel first
    img_sobel = sobel(base_img)
    #cv2.imwrite("video_2-0001_sobel.jpg", img_sobel)
    #apply thresholding to binarize image: http://docs.opencv.org/2.4/doc/tutorials/imgproc/threshold/threshold.html
    thresh, img_binary_sobel = cv2.threshold(img_sobel, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    #cv2.imwrite("video_2-0001_binary.jpg", img_binary_sobel)
    key_lines = hough(img_binary_sobel)
    #right now, best lines is all lines returned by Hough
    return key_lines


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


#http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
def hough(img): #img is a binarized image
    #First parameter, Input image should be a binary image, so apply threshold or use canny edge detection before finding applying hough transform. Second and third parameters are \rho and \theta accuracies respectively. Fourth argument is the threshold, which means minimum vote it should get for it to be considered as a line. Remember, number of votes depend upon number of points on the line. So it represents the minimum length of line that should be detected.
    quit()
    params = cv2.HoughLines(img, 1,np.pi/180, 100) #params 2 and 3 i got somewhere, 4 we should tune
    #arr is array of (rho, theta) for each line above voting threshold
    for i in xrange(len(params)):
        degrees = 180 * params[i][0][1] / math.pi
        params[i][0][1] = degrees #all angles are positive degree values
    return params #returns all params (rho, theta)

