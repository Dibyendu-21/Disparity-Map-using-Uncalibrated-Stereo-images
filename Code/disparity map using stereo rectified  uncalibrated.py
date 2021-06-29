# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 11:20:55 2021

@author: Sonu
"""
import numpy as np 
import cv2 

#Reading the stereo image pair
imgLeft = cv2.imread('left1.jpg',  0) 
imgRight = cv2.imread('right1.jpg', 0) 
   
#Detecting the key points and compute the descriptors for the train and query images using SIFT descriptor object 
sift = cv2.xfeatures2d.SIFT_create() 
keyPointsLeft, descriptorsLeft = sift.detectAndCompute(imgLeft, None) 
keyPointsRight, descriptorsRight = sift.detectAndCompute(imgRight, None) 
   
#Creating FLANN matcher object 
FLANN_INDEX_KDTREE = 0
indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5) 
searchParams = dict(checks=50) 
flann = cv2.FlannBasedMatcher(indexParams, searchParams) 

#Finding the top two matches for each descriptor using KNN match
matches = flann.knnMatch(descriptorsLeft, descriptorsRight, k=2)
   
goodMatches = [] 
   
for m, n in matches: 
    #Applying Lowe's ratio test   
    if m.distance < 0.8 * n.distance:
        goodMatches.append(m) 

#Finding the keypoints for good matches only
ptsLeft = np.float32([ keyPointsLeft[m.queryIdx].pt for m in goodMatches])
ptsRight = np.float32([ keyPointsRight[m.trainIdx].pt for m in goodMatches])
        
#Finding the fundamental matrix
F, mask = cv2.findFundamentalMat(ptsLeft, ptsRight, cv2.FM_RANSAC, ransacReprojThreshold = 1.0, confidence = 0.99) 
  
#Selecting only inlier points 
ptsLeft = ptsLeft[mask.ravel() == 1] 
ptsRight = ptsRight[mask.ravel() == 1] 

#Finding rectified Homography matrix for both stereo images
retval, H1, H2	=	cv2.stereoRectifyUncalibrated(ptsLeft, ptsRight, F, imgLeft.shape)
height, width = imgLeft.shape

#Warping both the stereo images to align them along the same image plane
rectifiedLeft = cv2.warpPerspective(imgLeft, H1, (width, height))
rectifiedRight = cv2.warpPerspective(imgRight, H2, (width, height))

#Creating a stereoSGBM object
stereo = cv2.StereoSGBM_create(numDisparities=96, blockSize=5, disp12MaxDiff=20, preFilterCap=16, uniquenessRatio=1, speckleWindowSize=100, speckleRange=20)
#Finding the disparity map between the warped stereo image pair 
disp = stereo.compute(rectifiedLeft, rectifiedRight)
#Normalizing the dispaity map between the range of 0-255
norm_coeff = 255 / disp.max()
disp = disp * norm_coeff / 255
cv2.imshow("disparity", disp)
cv2.waitKey(10000)
cv2.destroyAllWindows()
