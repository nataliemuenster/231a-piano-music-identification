import os, sys
import numpy as np
import preprocess
import note_detection
import key_detection
from scipy.misc import imread
import cv2
import urllib
import evaluation


videos_dir = "./data/videos"
max_RGB_value = 255

#User can change this for whichever video they want
video_name = "video_2" #url2 = "https://www.youtube.com/watch?v=CQTim0KdILE"
#First white key is D2

#the [x, y] for each right-click event will be stored here
right_clicks = list()

#this function will be called whenever the mouse is right-clicked
'''def mouse_callback(event, x, y, flags, params):
    #right-click event value is 2
    if event == 2:
        global right_clicks
        
        #store the coordinates of the right-click event
        right_clicks.append([x, y])

'''

def get_corners(img):
    print
    print "Please click on the four corners that define the keyboard in first image."
    print "Use two fingers when clicking to select points"
    print "Select in this order: top right, bottom right, top left, bottom left"

    
    '''scale_width = 640 / img.shape[1]
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
    '''
    
    global right_clicks
    right_clicks.extend([[0,303],[0,599],[1243,315],[1243,618]])


if __name__ == '__main__':
    images_dir = "./data/" + video_name + "_images"
    base_img_name = video_name + "-0001.jpg" #this might vary based on when the piano is visible w/o hands

    #get User's input
    start_key = input("Please enter the note corresponding to the left most white key with the number corresponding to its octave in the format (ex: 'A3') with quotes around the two characters: ")
    
    #error check input
    letters = "ABCDEFG"
    numbers = "01234567"
    while (len(start_key) != 2 or letters.find(start_key[0]) == -1 or numbers.find(start_key[1]) == -1):
        print "ERROR: The key you entered was invalid!"
        print
        start_key = input("Please enter the note corresponding to the left most white key with the number corresponding to its octave in the format (ex: 'A3') with quotes around the two characters: ")

    #Step 1: Preprocess
    base_img = cv2.imread(os.path.join(images_dir,base_img_name))
    get_corners(base_img)

    #error check input
    while len(right_clicks) != 4:
        right_clicks = list()
        print "Please reselect corners taking care to choose only 4 points"
        get_corners(base_img)

    pts_src = np.asarray(right_clicks)
    print "found corners:", right_clicks
    
    #Get the homography matrix for just the base image (w/o hands), which we can later use to rectify the rest of the images
    base_img_rectified, homography = preprocess.rectify_first(base_img, pts_src)
    
    #extract images from frames and rectifies them according to params of first image
    preprocess.get_and_rectify_frames(video_name, homography)

    #Step 2: locate keys and map to image coordinates
    [binary_rectified_sobel, binary_rectified] = preprocess.getBinaryImages(base_img_rectified)
    [whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes] = key_detection.detect_keys(binary_rectified, binary_rectified_sobel, start_key)

    black_key_width = np.average(blackKeys[:,3] - blackKeys[:,2])

    #Step 3: detect keys pressed and identify keys by mapping coordinates of differences
    key_x_coords = note_detection.allFrameDiffs(video_name, base_img_rectified.shape, black_key_width)
    notes = note_detection.map_to_key(key_x_coords, whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes)

    #Evaluation
    detected, true = evaluation.totalError(video_name, notes)
    editDist = evaluation.calculateDistance(detected, true)
    print "Edit distance:", editDist
    
    #print notes

    print "done with main"

