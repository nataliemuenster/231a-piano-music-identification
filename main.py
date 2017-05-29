import os, sys
import numpy as np
import image_extraction
from scipy.misc import imread
import cv2 #or cv2??
print cv2.__version__

#url = "https://www.youtube.com/watch?v=9Pk0R8OWg0k"
video_path = "./data/video_1.mp4"
images_dir = "./data/video_1_images"
sobel_img_dir = "./data/sobel_images/"

if __name__ == '__main__':
    block_size = 2
    cell_size = 6
    nbins = 9
    window_size = np.array([36, 36])

    frames = image_extraction.parse_video(video_path)
    images = []
    hog_features_all = []
	#cv2.glob(images_dir, images, false)
    image_list = os.listdir(images_dir)
    for img_name in image_list:
        img = cv2.imread(os.path.join(images_dir,img_name))

        if img is not None:
                img = image_extraction.sobel(img)
                images.append(img)

#hog_features = image_extraction.compute_hog_features(img, cell_size, block_size, nbins)
#hog_features_all.append(hog_features)

                name = img_name.split(".")[0]
			#cv2.imshow("image:", img)
			#cv2.imshow("sobel", images[333])

                
                cv2.imwrite(os.path.join(sobel_img_dir, name + "_sobel.jpg"), img)

			#cv2.waitKey(0)

#os.rename("./data/" + name + "_sobel.jpg", sobel_img_dir + name + "_sobel.jpg")
                #if img_name == "video_1-0122_sobel.jpg":
                # cv2.imwrite

		
        #images = np.array(images)
	#cv2.imshow("sobel", images[333])
	#cv2.waitKey(0)

    print "done with main"
