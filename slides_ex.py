#write diff rectified
import numpy as np
import cv2
import preprocess

if __name__ == '__main__':
	pts_src = np.asarray([[0,303],[0,599],[1243,315],[1243,618]])
	base_img = img1 = cv2.imread("./data/video_2_images_full/video_2-0001.jpg")
	base_img_rectified, homography = preprocess.rectify_first(base_img, pts_src)

	img1 = cv2.imread("./data/video_2_images_full/video_2-0049.jpg")
	img2 = cv2.imread("./data/video_2_images_full/video_2-0053.jpg")
	img1_rect = preprocess.rectify_other(img1, homography)
	cv2.imwrite("./slides_img1_rect.jpg", img1_rect)
	img2_rect = preprocess.rectify_other(img2, homography)
	cv2.imwrite("./slides_img2_rect.jpg", img2_rect)

	crop_height = 2*base_img.shape[0]/3
	x_height = crop_height/2
	gray1 = cv2.imread("./slides_img1_rect.jpg", cv2.IMREAD_GRAYSCALE)
	gray2 = cv2.imread("./slides_img2_rect.jpg", cv2.IMREAD_GRAYSCALE)
	crop1 = gray1[0:crop_height, :]
	crop2 = gray2[0:crop_height, :]
	diff = cv2.subtract(crop1, crop2)
	cv2.imwrite("./slides_diff.jpg", diff)