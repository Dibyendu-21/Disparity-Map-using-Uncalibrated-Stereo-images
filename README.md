# Disparity Map using Uncalibrated stereo images

This repo does and experimental and qualitative analysis of disparity map produced from three different methods using unclaibrated images.

## Uncalibrated Stereo Image Pair
![Stereo Image Left](Stereo%20Image/left2.jpg?raw=true)

![Stereo Image Right](Stereo%20Image/right2.jpg?raw=true)

## Method-1: Disparity map using Homography
This method finds homography between keypoints of matching pair sets from uncalibrated stereo images and warps one of the image to align along the same plane as that of the other image before finding the disparity map between the rectified warped image and the other stereo image.

### Design Pipeline
The Design Pipeline is as follows:
* Read the pair of raw uncalibrated stereo images.
* Initiate a keypoint detector. Here SIFT is used.
* Find the keypoints and descriptors with SIFT.
* Match object using FLANN based matcher.
* Retrieve the top two matches for each descriptor using KNN match with N=2.
* Store all the good matches as per Lowe's ratio test.
* Detect the keypoints for good matches only.
* Compute the homography between keypoints of matching pair sets using RANSAC.
* Warp the query image to align that image along the same plane as the train image.
* Create a stereo object.
* Find the disparity map between the warped query and target image using the stereo obejct.
* Normalize the dispaity map between the range of 0-255.
* Display the disparity map.

### Output
![Disparity Map](Disparity%20Map/disparity_map_using_homography_uncalibrated_image.png?raw=true)

## Method-2: Disparity map using raw Uncalibrated image
This method directly finds the disparity map between a pair of uncalibrated stereo images without performing any preprocessing.

### Design Pipeline
The Design Pipeline is as follows:
* Read the pair of raw uncalibrated stereo images.
* Create a stereo object.
* Find the disparity map between the pair of raw uncalibrated stereo images. 
* Normalize the dispaity map between the range of 0-255.
* Display the disparity map.

### Output
![Disparity Map](Disparity%20Map/disparity_map_using_raw_uncalibrated_image.png?raw=true)

## Method-3: Disparity map using rectified forms of stereo Uncalibrated images.
This method directly finds the disparity map using a rectified Homography matrix for both stereo images and rectifies both the stereo images to align them along the same image plane before finding the disparity map between both the rectified stereo image pair.

### Design Pipeline
The Design Pipeline is as follows:
* Read the pair of raw uncalibrated stereo images.
* Initiate a keypoint detector. Here SIFT is used.
* Find the keypoints and descriptors with SIFT.
* Match object using FLANN based matcher.
* Retrieve the top two matches for each descriptor using KNN match with N=2.
* Store all the good matches as per Lowe's ratio test.
* Detect the keypoints for good matches only.
* Compute the fundamental matrix between keypoints of matching pair sets using RANSAC..
* Select only inlier points. 
* Find the rectified Homography matrix for both stereo images using stereoRectifyUncalibrated() on the matchings set of inlier points.
* Rectify both the stereo images to align them along the same image plane.
* Create a stereo object.
* Finding the disparity map between the rectified stereo image pair. 
* Normalize the dispaity map between the range of 0-255.
* Display the disparity map.

### Output
![Disparity Map](Disparity%20Map/disparity_map_using_stereo_rectified_uncalibrated_image.png?raw=true)

 








