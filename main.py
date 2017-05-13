import sys
import numpy as np
from image_extraction import *
from scipy.misc import imread

#url = "https://www.youtube.com/watch?v=9Pk0R8OWg0k"
video_path = "./data/video_1.mp4"

if __name__ == '__main__':
	frames = image_extraction.parse_video(video_path)