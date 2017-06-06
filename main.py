import os, sys
import numpy as np
import preprocess
import note_detection
import key_detection
from scipy.misc import imread
import cv2
import urllib


videos_dir = "./data/videos"
max_RGB_value = 255

#url1 = "https://www.youtube.com/watch?v=9Pk0R8OWg0k"
#video_path = "./data/videos/video_1.mp4"

#url2 = "https://www.youtube.com/watch?v=CQTim0KdILE"
video_name = "video_2" #User can change this for whichever video they want



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
    
    """
    global right_clicks
    right_clicks.extend([[0,303],[0,599],[1243,315],[1243,618]])
    """

if __name__ == '__main__':
    images_dir = "./data/" + video_name + "_images"
    base_img_name = video_name + "-0001.jpg" #this might vary based on when the piano is visible w/o hands

    #get User's input
    start_key = input("Please enter the note corresponding to the left most white key with the number corresponding to its octive in the format (ex: 'A3') with quotes around the two characters: ")
    
    #error check input
    letters = "ABCDEFG"
    numbers = "01234567"
    while (len(start_key) != 2 or letters.find(start_key[0]) == -1 or numbers.find(start_key[1]) == -1):
        print "ERROR: The key you entered was invalid!"
        print
        start_key = input("Please enter the note corresponding to the left most white key with the number corresponding to its octive in the format (ex: 'A3') with quotes around the two characters: ")

    base_img = cv2.imread(os.path.join(images_dir,base_img_name)) #a static variable above main
    base_img = base_img.astype(np.uint8) #need this??
    get_corners(base_img)

    #error check input
    while len(right_clicks) != 4:
        print "before right_clicks ", right_clicks
        right_clicks = list()
        print "after right_clicks ", right_clicks
        print "Please reselect corners taking care to choose only 4 points"
        get_corners(base_img)

    pts_src = np.asarray(right_clicks)
    print "found corners:", right_clicks
    
    base_img_rectified, homography = preprocess.rectify_first(base_img, pts_src)
    #get the sobel of just the baseline image (no hands) to get lines between keys from Hough transform (Right now, key_lines is all lines returned by Hough)
    
    cv2.imshow('image', base_img_rectified)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


    #extract images from frames and rectifies them acording to params of first image
    #frames = preprocess.get_frames(video_name)
    preprocess.get_and_rectify_frames(video_name, homography)
    print "preprocessed and rectified frames"

    [binary_rectified_sobel, binary_rectified] = preprocess.getBinaryImages(base_img_rectified)
    #print "got binary"

    [whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes] = key_detection.detect_keys(binary_rectified, binary_rectified_sobel, start_key)
    
    #print whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes
    black_key_width = np.average(blackKeys[:,3] - blackKeys[:,2])

    #Mask off hands from each frame first? Then make it black and white?
    #Rectify all the frames we need #DONE IN GET_AND_RECTIFY_FRAMES!!!
    #frames = preprocess.rectify_all(frames, params) #ALSO TURNS TO GREYSCALE!! mask out hands first?
    #preprocess.rectify_all(video_name, params)
    print "all frames rectified"
    #Now detectNotesPressed
    #find light source based on shape of shadows?? then decide how shadows determine right or left key
    key_x_coords = note_detection.allFrameDiffs(video_name, base_img_rectified.shape, black_key_width)
    #print "x_coords:", key_x_coords

    note_detection.map_to_key(key_x_coords, whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes)
    
    

    print "done with main"

