import os, sys
import numpy as np
from image_extraction import *
from scipy.misc import imread
import cv2 #or cv2??

#url = "https://www.youtube.com/watch?v=9Pk0R8OWg0k"
video_path = "./data/video_1.mp4"
images_dir = "./data/video_1_images"

if __name__ == '__main__':
	frames = image_extraction.parse_video(video_path)
	images = []
	#cv2.glob(images_dir, images, false)
	#for (i,image_file) in enumerate(glob.iglob('')
	for img_name in os.listdir(images_dir):
        img = cv2.imread(os.path.join(images_dir,img_name))
        if img is not None:
        	img = image_extraction.sobel(img)
            images.append(img)
    
	images = np.array(images)	
	cv2.imshow("sobel", images[333])
	cv2.waitKey(0)
	print "done with main"
