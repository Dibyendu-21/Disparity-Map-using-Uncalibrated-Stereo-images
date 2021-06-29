# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 19:39:05 2021

@author: Sonu
"""
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('left2.jpg',0)
cv2.imshow('img_left', imgL)
cv2.waitKey(10000)
cv2.destroyAllWindows()
        
imgR = cv2.imread('right2.jpg',0)
cv2.imshow('img_right', imgR)
cv2.waitKey(10000)
cv2.destroyAllWindows()

#Creating a stereoSGBM object
stereo = cv2.StereoSGBM_create(numDisparities=96, blockSize=5, disp12MaxDiff=20, preFilterCap=16, uniquenessRatio=1, speckleWindowSize=100, speckleRange=20)
#Finding the disparity map between the pair of raw uncalibrated stereo images 
disp = stereo.compute(imgL, imgR)

#Normalizing the dispaity map between the range of 0-255
norm_coeff = 255 / disp.max()
disp = disp * norm_coeff / 255
cv2.imshow("disparity", disp)
cv2.waitKey(10000)
cv2.destroyAllWindows()

plt.imshow(disp,'gray')
plt.show()

