import numpy as np
from scipy.misc import imread
import ffmpy
from ffmpy import FFmpeg
import cv2
import os
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def region_labeling(im):
    n = 12
    l = 256
    np.random.seed(1)
    im = np.zeros((l, l))
    points = l * np.random.random((2, n ** 2))
    im[(points[0]).astype(np.int), (points[1]).astype(np.int)] = 1
    im = filters.gaussian_filter(im, sigma= l / (4. * n))
    blobs = im > 0.7 * im.mean()

    all_labels = measure.label(blobs)
    blobs_labels = measure.label(blobs, background=0)

    plt.figure(figsize=(9, 3.5))
    plt.subplot(131)

