# SIFT ALGORITHM
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
img1 = cv.imread('IMG_4061.JPG')          # queryImage
img2 = cv.imread('IMG_4156.JPG') # trainImage
gray_image1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY) 
gray_image2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY) 
# Initiate SIFT detector
sift = cv.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)
# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)
width = 1500
height = 1500
channels = 3  # 3 channels for color (BGR)
# Create a blank black image
blank_image = np.zeros((height, width, channels), dtype=np.uint8)
# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]
color = (255,0,0)
thickness = 2
# ratio test as per Lowe's paper
good_matches = []
threshold_length = 30 
for i,(m,n) in enumerate(matches):
 if m.distance < 0.1*n.distance:
  matchesMask[i]=[1,0]
  good_matches.append(m)
for match in good_matches :
   img1_idx = match.queryIdx
   img2_idx = match.trainIdx

    # Get the coordinates
   (x1, y1) = kp1[img1_idx].pt
   (x2, y2) = kp2[img2_idx].pt
   query_keypoint = kp1[match.queryIdx]
   train_keypoint = kp2[match.trainIdx]
   query_x, query_y = map(int, query_keypoint.pt)
   train_x, train_y = map(int, train_keypoint.pt)
   arrow_length = np.sqrt((train_x - query_x)**2 + (train_y - query_y)**2)

    # # Draw an arrow only if the length is below the threshold
    # if arrow_length < threshold_length:
    #     cv.arrowedLine(img1, (query_x, query_y), (train_x, train_y), (0, 255, 0), 1)
   print(f"Image 1 - X: {x1}, Y: {y1} | Image 2 - X: {x2}, Y: {y2}")
   pt1 = (int(x1), int(y1))
   pt2 = (int(x2), int(y2))
   image_with_arrow = cv.arrowedLine(blank_image,pt1, pt2, color, thickness,line_type=8, shift=0, tipLength=0.1)
draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   matchesMask = matchesMask,
                   flags = cv.DrawMatchesFlags_DEFAULT)
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
cv.imshow('Arrowed Line', image_with_arrow)
plt.imshow(img3,),plt.show()
# cv.imshow("Matches and Arrows", img1)
cv.waitKey(0)
cv.destroyAllWindows()
