import os, sys
import numpy as np
import image_extraction
from scipy.misc import imread
import cv2 #or cv2??
print cv2.__version__

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

    video_path = "./data/videos/" + video_name + ".mp4"
    images_dir = "./data/" + video_name + "_images"
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)

    #videos = os.listdir(videos_dir)
    #video = video_name + ".mp4" #do we need to "open" this video at all?
    
    #extract images from frames. Doesn't actually do anything rn...
    frames = image_extraction.parse_video(video_path)
    

    #kernel = np.ones((5,5),np.uint8) #for dilation/erosion to fill in gaps, used for masking

    #get the sobel of just the baseline image (no hands) to get lines using Sobel then Hough transform
    '''base_img_name = "video_1-0122.jpg"
    base_img = cv2.imread(os.path.join(images_dir,base_img_name))
    base_img = base_img.astype(np.uint8)
    sobel_img = image_extraction.sobel(base_img)
    sobel_img = cv2.cvtColor(sobel_img, cv2.COLOR_RGB2GRAY) #convert to greyscale to applythresholding to binarize image

    cv2.imshow("sobel", sobel_img)
 	cv2.waitKey(0)
 	'''

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
