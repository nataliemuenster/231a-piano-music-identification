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


WB_key_len_ratio = 0.65
threshold = 0.8


def detect_keys(img_binary, img_binary_sobel, start_key):
        
    #get an array defining each key
    [whiteKeys, numWhiteKeys, offset, white_notes] = detect_white_keys(img_binary_sobel, start_key)
    
    [blackKeys, numBlackKeys, black_notes] = detect_black_keys(img_binary, offset)

    return whiteKeys, numWhiteKeys, blackKeys, numBlackKeys, white_notes, black_notes

def detect_white_keys(im_bw, startKey):
    imheight = im_bw.shape[0]
    
    im_bottom = im_bw[int(imheight * (2/3)):imheight, :]

    #gather a few sample keys to find the average width of a white key
    widths = []
    start = im_bottom.shape[1] / 3
    start_edge = start
    pixel = start
    firstKey = True
    numSampleKeys = 0
    while numSampleKeys < 5:
        if im_bottom[int(im_bottom.shape[0]/2), pixel] < threshold: #if in blackspace in the middle of a white #key (using binarized sobel image)
            pixel += 1
        
        else:
            if firstKey == True:
                firstKey = False
                start = pixel
                first_edge = pixel
            else:
                if (abs(start - pixel) > 12):
                    widths.append(abs(start - pixel))
                    numSampleKeys += 1
                    start = pixel

            #move past white space to get to next key
            while im_bottom[int(im_bottom.shape[0]/2), pixel] > threshold:
                pixel += 1
            start = pixel


    wk_width = sum(widths)/numSampleKeys
    # print "wk_width ", wk_width
    
    whiteKeys = np.zeros((52, 4))

    last_edge = start_edge
    numWhiteKeys = 0
    first_edge = start_edge

    while first_edge < (im_bottom.shape[1] - wk_width): #work across the photo towards the right
        if numWhiteKeys < 52:
            first_edge = last_edge
            
            #print "numWhiteKeys, whiteKeys.shape ", numWhiteKeys, whiteKeys.shape
            whiteKeys[numWhiteKeys-1][0] = 0
            whiteKeys[numWhiteKeys-1][1] = imheight
            whiteKeys[numWhiteKeys-1][2] = first_edge
            last_edge = first_edge + wk_width
            whiteKeys[numWhiteKeys-1][3] = last_edge
            #print "start and end of key ",first_edge, last_edge
            numWhiteKeys += 1
        else :
            break
                    
    last_edge = start_edge
    first_edge = start_edge
    while pixel > wk_width: #work across the photo towards the left
        if numWhiteKeys < 52:
            start_edge = last_edge
            #print "numWhiteKeys, whiteKeys.shape ", numWhiteKeys, whiteKeys.shape

            whiteKeys[numWhiteKeys-1][0] = 0
            whiteKeys[numWhiteKeys-1][1] = imheight
            whiteKeys[numWhiteKeys-1][3] = last_edge
            start_edge = last_edge - wk_width
            whiteKeys[numWhiteKeys-1][2] = first_edge
            numWhiteKeys += 1
        else :
            break

    nonzero_row_indices = []
    zeros = np.zeros((4, 1))
    #remove rows that are all 0's
    for i in range(0,whiteKeys.shape[0]):
        if not np.array_equal(whiteKeys[i,:].reshape(4,1), zeros):
            nonzero_row_indices.append(i)

    whiteKeys = whiteKeys[nonzero_row_indices,:]

    ind = np.argsort(whiteKeys[:, 2])

    sorted_white_keys = whiteKeys[ind]


    #correlate each key with its note based on the left-most-note passed in

    offset = 0 #default A

    if startKey == "B":
        offset = 1
    elif startKey == "C":
        offset = 2
    elif startKey == "D":
        offset = 3
    elif startKey == "E":
        offset = 4
    elif startKey == "F":
        offset = 5
    else: # if G
        offset = 6

    white_notes = []
    for i in range(0,whiteKeys.shape[0]):
        white_notes.append("ABCDEFG"[(i + offset) % 7])
    return sorted_white_keys, numWhiteKeys, offset, white_notes


def detect_black_keys(im_bw, offset):
    white_key_len = im_bw.shape[0]
    im_top = im_bw[0:int(white_key_len/2), :]
    [blackKeys, numBlackKeys] = get_black_key_boundaries(white_key_len, im_top)

    nonzero_row_indices = []
    zeros = np.zeros((4, 1))
    #remove rows that are all 0's
    for i in range(0, blackKeys.shape[0]):
        if not np.array_equal(blackKeys[i,:].reshape(4,1), zeros):
            nonzero_row_indices.append(i)

    blackKeys = blackKeys[nonzero_row_indices,:]

    #sort by x-axis min bound just in case something went wrong
    ind = np.argsort(blackKeys[:, 2])
    blackKeys = blackKeys[ind]

    black_notes = []

    if im_top[im_top.shape[0]-1, 0] > threshold: #if the edge doesn't start with a black key
        for i in range(0,blackKeys.shape[0]):
            black_notes.append("ACDFG"[(i + offset) % 5]) #first black key will be the sharp following first white key
    else : #if edge starts with black key
        for i in range(0,blackKeys.shape[0]):
            black_notes.append("GACDF"[(i + offset) % 5]) #first black key will be the sharp before first white key

    return blackKeys, numBlackKeys, black_notes


def get_black_key_boundaries(white_key_len, im_top):

    blackKeys = np.zeros((36, 4))
    numBlackKeys = 0
    
    start = True
    start_edge = 0
    pixel = start_edge
    while pixel < im_top.shape[1]:
        if start: #only do this for the first key
            if im_top[im_top.shape[0] - 1, 0] > threshold: #if the edge doesn't start with a black key
                while im_top[im_top.shape[0] - 1, pixel] > threshold: #move past white space
                    pixel += 1
                start_edge = pixel #set start edge of first black key
    
        #mark region of black key
        blackKeys[numBlackKeys-1][0] = 0
        blackKeys[numBlackKeys-1][1] = white_key_len * WB_key_len_ratio
        blackKeys[numBlackKeys-1][2] = start_edge
        
        #move through black region
        while im_top[im_top.shape[0]-1, pixel] < threshold:
            if pixel < im_top.shape[1] - 1:
                pixel += 1
            else:
                blackKeys[numBlackKeys-1][3] = pixel
                numBlackKeys += 1
                return blackKeys, numBlackKeys
        
        if abs(pixel - start_edge) > 15:
            #print "start_edge, pixel ", start_edge, pixel
            blackKeys[numBlackKeys-1][3] = pixel
            numBlackKeys += 1

        else: #if this isn't actually the end of the key but a blip of white pixels interrupting key,
            #move past blip
            while im_top[im_top.shape[0]-1, pixel] > threshold:
                if pixel < im_top.shape[1] - 1:
                    pixel += 1
                else:
                    return blackKeys, numBlackKeys

            #find the actual end of the key
            while im_top[im_top.shape[0]-1, pixel] < threshold:
                if pixel < im_top.shape[1] - 1:
                    pixel += 1
                else:
                    blackKeys[numBlackKeys-1][3] = pixel
                    numBlackKeys += 1
                    return blackKeys, numBlackKeys

            blackKeys[numBlackKeys-1][3] = pixel
            numBlackKeys += 1

#print "22222  start_edge, pixel ", start_edge, pixel


        #move past white space
        while im_top[im_top.shape[0]-1, pixel] > threshold:
            if pixel < im_top.shape[1] - 1:
                pixel += 1
                start_edge = pixel
            else:
                return blackKeys, numBlackKeys

    return blackKeys, numBlackKeys
