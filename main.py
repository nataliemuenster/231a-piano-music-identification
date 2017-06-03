import os, sys
import numpy as np
import preprocess
import key_detection
from scipy.misc import imread
import cv2
import urllib
from win32api import GetSystemMetrics



videos_dir = "./data/videos"
max_RGB_value = 255

#url1 = "https://www.youtube.com/watch?v=9Pk0R8OWg0k"
'''video_path = "./data/videos/video_1.mp4"
images_dir = "./data/video_1_images"
sobel_img_dir = "./data/sobel_images_1"
base_img_name = "video_1-0122.jpg"
'''

#url2 = "https://www.youtube.com/watch?v=CQTim0KdILE"
video_name = "video_2" #User can change this for whichever video they want
video_path = "./data/videos/video_2.mp4"
images_dir = "./data/video_2_images"
sobel_img_dir = "./data/sobel_images_2"
base_img_name = "video_2-0001.jpg"


if __name__ == '__main__':
    
    corners, start_key = getUserInput()
    """
    video_path = "./data/videos/" + video_name + ".mp4"
    images_dir = "./data/" + video_name + "_images"
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)
    """
    
    #extract images from frames. Doesn't actually do anything rn...
    #frames = image_extraction.parse_video(video_path)
    
    """
    #kernel = np.ones((5,5),np.uint8) #for dilation/erosion to fill in gaps, used for masking
    base_img = base_img = cv2.imread(os.path.join(images_dir,base_img_name)) #a static variable above main
    base_img = base_img.astype(np.uint8)
    base_img_rectified = preprocess.rectify(base_img)
    quit()
    #get the sobel of just the baseline image (no hands) to get lines between keys from Hough transform (Right now, key_lines is all lines returned by Hough)
    key_lines = preprocess.getLines(base_img_rectified) #will use base_img_rectified once i finish rectify
    """
    
    get_corners(img)
    
    """
    start_key = "B"

    binary_rectified = cv2.imread("./video_2-0001_binary_no_sobel.jpg") #a static variable above main
    
    binary_rectified_sobel = cv2.imread("./video_2-0001_binary.jpg") #a static variable above main
    
    [whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes] = key_detection.detect_keys(binary_rectified, binary_rectified_sobel, start_key)
    
    print whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes
    """

    #loops through all the images in the video directory
    '''image_list = os.listdir(images_dir)
    images = []
    for img_name in image_list:
        img = cv2.imread(os.path.join(images_dir,img_name))
        name = ""
        if img is not None:
                img = img.astype(np.uint8)
                img = image_extraction.sobel(img)
                #print "img.shape", img.shape
                images.append(img)
    '''



    print "done with main"



"""
def getUserInput
    print Hello! In order to process your video, we require a couple pieces of information about your video.
    top_right = input('Pixel coordinates of the top right corner (in the format [x,y] with no spaces): ')
    top_right = input('Pixel coordinates of the top right corner (in the format [x,y] with no spaces): ')
    top_right = input('Pixel coordinates of the top right corner (in the format [x,y] with no spaces): ')
    top_right = input('Pixel coordinates of the top right corner (in the format [x,y] with no spaces): ')

"""



#the [x, y] for each right-click event will be stored here
right_clicks = list()

#this function will be called whenever the mouse is right-clicked
def mouse_callback(event, x, y, flags, params):
    
    #right-click event value is 2
    if event == 2:
        global right_clicks
        
        #store the coordinates of the right-click event
        right_clicks.append([x, y])
        
        #this just verifies that the mouse data is being collected
        #you probably want to remove this later
        print right_clicks

def get_corners(img):
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    scale_width = 640 / img.shape[1]
    scale_height = 480 / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('image', window_width, window_height)
    
    #set mouse callback function for window
    cv2.setMouseCallback('image', mouse_callback)
    
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




