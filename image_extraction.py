import numpy as np
from scipy.misc import imread
import ffmpy
from ffmpy import FFmpeg

#def get_video -- let's just manually input urls for now when we want to extract a video

#change output image names according to each video
def parse_video(video):
	#In command line I used: "ffmpeg -r 30 -i video_1.mp4 -f image2 video_1-%d.jpg-s" (gave error about specifying size, so I removed it-- 640x480)
	

	#If we need to include this parsing in our code, here is how to do it in python:
	#ff = ffmpy.FFmpeg(inputs={"ffmpeg -r 30 -i video_1.mp4 -f image2 video_1-%d.jpg"}, outputs={})
