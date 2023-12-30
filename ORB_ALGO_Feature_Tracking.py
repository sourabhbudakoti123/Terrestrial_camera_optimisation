#  ORB ALGORITHM
import numpy as np
import cv2 as cv
import pandas as pd
import matplotlib.pyplot as plt
i1 = cv.imread('IMG_4037.JPG')          # queryImage
i2 = cv.imread('IMG_4456.JPG') # trainImage
r1 = cv.selectROI("select the area", i1) 
r2 = cv.selectROI("select the area", i2)
img1 = i1[int(r1[1]):int(r1[1]+r1[3]),  
                      int(r1[0]):int(r1[0]+r1[2])] 
img2 = i2[int(r2[1]):int(r2[1]+r2[3]),  
                      int(r2[0]):int(r2[0]+r2[2])] 
gray_image1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY) 
gray_image2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY) 
orb = cv.ORB_create()
width = 6000
height = 4000
channels = 3  # 3 channels for color (BGR)
# Create a blank black image
blank_image = np.zeros((height, width, channels), dtype=np.uint8)
color = (255,0,0)
thickness = 2
threshold_length = 30
# Find keypoints and descriptors
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2, None)

# Create a Brute Force Matcher object
bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)

# Match descriptors
matches = bf.knnMatch(des1, des2, k=2)
matchesMask = [[0,0] for i in range(len(matches))]
good_matches = []
for (m,n) in matches: 
 if m.distance < 0.3*n.distance:
  good_matches.append(m)
matches_img = cv.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)        
# Print coordinates of matching points
for match in good_matches:
    # Get the coordinates of keypoints in both images
  img1_idx = match.queryIdx
  img2_idx = match.trainIdx
    # Get the coordinates
  (x1, y1) = kp1[img1_idx].pt
  (x2, y2) = kp2[img2_idx].pt
  print(f"Image 1 - X: {x1}, Y: {y1} | Image 2 - X: {x2}, Y: {y2}")
  pt1 = (int(x1), int(y1))
  pt2 = (int(x2), int(y2))
  image_with_arrow = cv.arrowedLine(img1, pt1, pt2, color, thickness,line_type=8, shift=0, tipLength=0.1)
  cv.imshow('Arrowed Line', image_with_arrow)
plt.imshow(matches_img,),plt.show()
cv.waitKey(0)
cv.destroyAllWindows()
