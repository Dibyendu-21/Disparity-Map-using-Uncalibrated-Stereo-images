# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 12:59:21 2021

@author: Sonu
"""
import numpy as np
import cv2

MIN_MATCH_COUNT = 4

img1 = cv2.imread('left2.jpg',0)  #QueryImage
img2 = cv2.imread('right2.jpg',0) #TrainImage

#Initiating SIFT descriptor
sift = cv2.xfeatures2d.SIFT_create()

#Finding the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

#Match object using FLANN based matcher
flann = cv2.FlannBasedMatcher(index_params, search_params)
#Finding the top two matches for each descriptor using KNN match
matches = flann.knnMatch(des1,des2,k=2)

#Storing all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)
        
#Homography is possible if atleast 4 sets of match are found                
if len(good)>MIN_MATCH_COUNT:
    print('yeah!!')
    #Finding the keypoints for good matches only
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    
    #Finding the homography between keypoints of matching pair sets using RANSAC
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    h,w = img1.shape
    #Warping the query image to align that image along the same plane as the train image.
    #Bringing both the images in the same perspective view.
    rectifiedimg1 = cv2.warpPerspective(img1, M, (w,h))

#Creating a stereoSGBM object
stereo = cv2.StereoSGBM_create(numDisparities=96, blockSize=5, disp12MaxDiff=20, preFilterCap=16, uniquenessRatio=1, speckleWindowSize=100, speckleRange=20)

#Finding the disparity map between the warped query and target image 
disp = stereo.compute(rectifiedimg1, img2)

#Normalizing the dispaity map between the range of 0-255
norm_coeff = 255 / disp.max()
disp = disp * norm_coeff / 255
cv2.imshow("disparity", disp)
cv2.waitKey(10000)
cv2.destroyAllWindows()

