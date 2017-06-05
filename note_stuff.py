import numpy as np
from scipy.misc import imread
import ffmpy
from ffmpy import FFmpeg
import cv2
import os
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from skimage.segmentation import clear_border
from skimage.morphology import label


pixel_buffer = 10

def map_to_key(key_x, whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes):
    x = key_x + pixel_buffer
    
    #check if there is  black key that covers this region
    black_key = blackKeys[np.where(blackKeys[2, :] < x and blackKeys[3, :] > x)]
    index = np.where(blackKeys[2, :] < x and blackKeys[3, :] > x)[0]
    note = black_notes[index]
    
    print index
    print black_key
    
    if black_key : #something something
        return

    #if it matches no black key it must be a white key
    white_key = whiteKeys[np.where(whiteKeys[2, :] < x and whiteKeys[3, :] > x)]
    index = np.where(whiteKeys[2, :] < x and whiteKeys[3, :] > x)[0]
    note = white_notes[index] + " sharp"

    return note





