#test commit
# get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import cv2
import numpy as np

# Get still image from disk
vidcap = cv2.VideoCapture(0)

while True:
	success, img = vidcap.read()

# Define the lower and upper boundaries of the color we need
# This is not easy to do, I'll try to explain some techniques in another document
	lower = np.array([85,50,50])  # HSV
	upper = np.array([93,255,255])

# Convert the image from RGB to HSV color space.  This is required for the next operation.
	tape_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

# Create a new image that contains yellow where the color was detected, otherwise purple
	res = cv2.inRange(tape_hsv, lower, upper)

# A kernal is like a matrix that is used in the morphology operation
# See https://en.wikipedia.org/wiki/Kernel_(image_processing) if interested
	kernel = np.ones((4,4),np.uint8)

# The morphological 'open' operation is described here:
# https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html
# It helps remove noise and jagged edges, note how the stray speckles are removed!
	opened = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
# Blurring operation helps forthcoming findContours operation work better
	blur = cv2.blur(opened, (3,3))
# cv2.waitKey(0)

# Find contours
	(_, cnts, _) = cv2.findContours(blur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sometimes the contours operation will find more than two contours
# But if we did all our preliminary operations properly, then the two contours we need will be
# the *largest* contours in the set of contours.  The sorted operation below sorts
# the cnts array of contours by area, so the first two contours will be the largest

	cnt1 = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
	cnt2 = sorted(cnts, key = cv2.contourArea, reverse = True)[1]

# Draw a minimum area rectangle around each contour
	rect1 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt1)))
	rect2 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt2)))

# Draw the contours in red (255, 0, 0) on top of our original image
	cv2.drawContours(img, [rect1], -1, (255, 0, 0), 2)
	cv2.drawContours(img, [rect2], -1, (255, 0, 0), 2)

# Get the moment of the contour: https://docs.opencv.org/3.3.0/dd/d49/tutorial_py_contour_features.html
# it's like the center
	M1 = cv2.moments(cnt1)
	cx1 = int(M1['m10']/M1['m00'])
	cy1 = int(M1['m01']/M1['m00'])
	cv2.circle(img,(cx1,cy1), 5, (0,0,255), -1)
	M2 = cv2.moments(cnt2)
	cx2 = int(M2['m10']/M2['m00'])
	cy2 = int(M2['m01']/M2['m00'])
	cv2.circle(img,(cx2,cy2), 5, (0,0,255), -1)

# Next steps: find the center point between the two pieces of tape
	centerX = round((cx1 + cx2)/2)
	centerY = round((cy1 + cy2)/2)

	center = (centerX, centerY)

	cv2.circle(img, center, 5, (255,0,0), -1)
	height, width, channels = img.shape
	img_center = (width, height)
# cv2.circle(img, img_center, 5)

#Get center of image
	height, width = img.shape[:2]

	trueCenterX = int(width / 2)
	trueCenterY = int(height / 2)

	cv2.circle(img, (trueCenterX, trueCenterY), 5, (0, 0, 0), -1)

#Draw line between center of image and center of tape
	cv2.line(img, (trueCenterX, trueCenterY), center, (0,255,0),2)
#Draw Horizontal line
	cv2.line(img,(trueCenterX, centerY), center,(255,0,0),2)
#Draw Vertical line
	cv2.line(img,(trueCenterX, trueCenterY), (trueCenterX, centerY),(0,0,255),2)


	lengthOffset = trueCenterX - centerX
	heightOffset = trueCenterY - centerY

	print("Length Offset: " + str(abs(lengthOffset)) + "\n", "Height Offset: " + str(abs(heightOffset)))

	cv2.imshow("image", img)
	cv2.waitKey(1)
