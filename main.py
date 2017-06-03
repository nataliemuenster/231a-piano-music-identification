import os, sys
import numpy as np
import preprocess
import key_detection
from scipy.misc import imread
import cv2
import urllib



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


#the [x, y] for each right-click event will be stored here
right_clicks = list()

#this function will be called whenever the mouse is right-clicked
def mouse_callback(event, x, y, flags, params):
    #right-click event value is 2
    if event == 2:
        global right_clicks
        
        #store the coordinates of the right-click event
        right_clicks.append([x, y])

def get_corners(img):
    print
    print "Please click on the four corners that define the keyboard in first image."
    print "Use two fingers when clicking to select points"
    print "Select in this order: top right, bottom right, top left, bottom left"
    
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




if __name__ == '__main__':
    
    #get User's input
    start_key = input("Please enter the note corresponding to the left most white key in the format (A, B, C, D, E, F, or G) with quotes around the capital letter: ")
    first_frame = cv2.imread(os.path.join(images_dir,base_img_name)) #a static variable above main
    get_corners(first_frame)
    
    """
    video_path = "./data/videos/" + video_name + ".mp4"
    images_dir = "./data/" + video_name + "_images"
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)
    """
    
    #extract images from frames. Doesn't actually do anything rn...
    #frames = image_extraction.parse_video(video_path)
    
    
    #kernel = np.ones((5,5),np.uint8) #for dilation/erosion to fill in gaps, used for masking
    base_img = base_img = cv2.imread(os.path.join(images_dir,base_img_name)) #a static variable above main
    base_img = base_img.astype(np.uint8)
    
    pts_src = np.asarray(right_clicks)
    
    base_img_rectified = preprocess.rectify(base_img, pts_src)
    cv2.imshow('image', base_img_rectified)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    [binary_rectified_sobel, binary_rectified] = preprocess.getBinaryImages(base_img_rectified)
    #quit()

    [whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes] = key_detection.detect_keys(binary_rectified, binary_rectified_sobel, start_key)
    
    print whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes


    print "done with main"

