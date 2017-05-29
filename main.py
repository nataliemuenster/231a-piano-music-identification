import os, sys
import numpy as np
import image_extraction
from scipy.misc import imread
import cv2 #or cv2??
print cv2.__version__

videos_dir = "./data/videos"

#url1 = "https://www.youtube.com/watch?v=9Pk0R8OWg0k"
video_path = "./data/videos/video_1.mp4"
images_dir = "./data/video_1_images"
sobel_img_dir = "./data/sobel_images_1"

#url2 = "https://www.youtube.com/watch?v=CQTim0KdILE"
video_path = "./data/videos/video_2.mp4"
images_dir = "./data/video_2_images"
sobel_img_dir = "./data/sobel_images_2"


if __name__ == '__main__':
    block_size = 2
    cell_size = 6
    nbins = 9

    videos = os.listdir(videos_dir)
    for video in videos:
        video_path = "./data/videos/" + video
        video_name = video.split(".")[0]
        
        images_dir = "./data/" + video_name + "_images"
        if not os.path.exists(images_dir):
            os.mkdir(images_dir)


        
        vid_num = video.split("_")[1]
        print vid_num[0]
        sobel_img_dir = "./data/sobel_images_" + vid_num[0]
        
        if not os.path.exists(sobel_img_dir):
            os.mkdir(sobel_img_dir)
        
        frames = image_extraction.parse_video(video_path)
        images = []
        hog_features_all = []
        #cv2.glob(images_dir, images, false)

        kernel = np.ones((5,5),np.uint8)

        image_list = os.listdir(images_dir)
        
        for img_name in image_list:
            img = cv2.imread(os.path.join(images_dir,img_name))
            name = ""
            if img is not None:
                    img = img.astype(np.uint8)
                    img = image_extraction.sobel(img)
                    #print "img.shape", img.shape
                    images.append(img)


    #Hey Natalie! The following code is my attempts to try to crop along the lines but I'm getting really stuck because honestly figuring how to crop seems like a project in itself. Idk if we should just manually pick a region of the image as a subset of the image matrix
                    """
                    for gray in cv2.split(img):
                        print "gray", gray
                            
                            
                    #dilated = cv2.dilate(src = gray, kernel = kernel, anchor = (-1,-1))
            
                    #blured = cv2.medianBlur(dilated, 7)
                
                    # Shrinking followed by expanding can be used for removing isolated noise pixels
                    # another way to think of it is "enlarging the background"
                    # http://www.cs.umb.edu/~marc/cs675/cvs09-12.pdf
                    #small = cv2.pyrDown(blured, dstsize = (width / 2, height / 2))
                    # oversized = cv2.pyrUp(small, dstsize = (width, height))
                    """
                    name = img_name.split(".")[0]
                #cv2.imshow("image:", img)
                #cv2.imshow("sobel", images[333])
                
                #THIS IS ME TRYING TO MANUALLY CROP but I think we can also do this to the entire video when we're parsing (see image_extraction)

                    img = img[80:16+(img.shape[0]/2), :]
                    
                    cv2.imwrite(os.path.join(sobel_img_dir, name + "_sobel.jpg"), img)
                    
                    
            
            #The following code is me playinga round with the effect of dilating and eroding the sobel image to see if I can get the lines to be more crip in order to crop
            """
            if img_name == "video_1-0122.jpg":
                im = imread(os.path.join(sobel_img_dir, name + "_sobel.jpg"), 'L').astype(np.uint8)

    #http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
                im_eroded = cv2.erode(im,kernel,iterations = 1)
                #im_dilated = cv2.dilate(im_eroded,kernel,iterations = 1)
                cv2.imwrite(os.path.join(sobel_img_dir, name + "_E_AND_D.jpg"), img)



                #cv2.waitKey(0)
                break
        """

    #Here I'm trying to collect hog features for every sobel image but like I texted you the image's shape here is (2, 640, 3) unlike the (480, 640, 3) shape of the image we put inte the sobel directory when we print in the method for loop above... super confused by this
        """
        image_list_sobel = os.listdir(sobel_img_dir)
        for img_name in image_list_sobel:
            img = imread(os.path.join(sobel_img_dir,img_name))
            if img is not None:

                #if img_name == "video_1-0122_sobel.jpg":
                print "img.shape", img.shape

                img = img[:2].astype(np.uint8)
                print "img.shape", img.shape
                hog_features = image_extraction.compute_hog_features(img[:2], cell_size, block_size, nbins)
                hog_features_all.append(hog_features)
                print hog_features_all
                break
        """

    #  cv2.imwrite(os.path.join(sobel_img_dir, name + "_sobel.jpg"), img)



                    # cv2.imwrite

            
            #images = np.array(images)
        #cv2.imshow("sobel", images[333])
        #cv2.waitKey(0)

    print "done with main"
