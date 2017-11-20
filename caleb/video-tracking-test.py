import numpy as np
import cv2
import time
from skvideo.io import vread
from networktables import NetworkTables

#stable determines if you want to stabilize the image or not
stable = True;

#set HSV vars for later use
lower = np.array([85,50,50])
upper = np.array([93,255,255])

#initialize capture device
#using skvideo.io.vread as workaround because cv2 wasn't working
#sudo pip install sk-video
cap = vread('../tape-vid.mp4')

NetworkTables.initialize()
sd = NetworkTables.getTable("MotionTracking")

for frame in cap:

    # Convert the image from RGB to HSV color space.  This is required for the next operation.
    tape_hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

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
    cv2.drawContours(frame, [rect1], -1, (255, 0, 0), 2)
    cv2.drawContours(frame, [rect2], -1, (255, 0, 0), 2)

    # Get the moment of the contour: https://docs.opencv.org/3.3.0/dd/d49/tutorial_py_contour_features.html
    # it's like the center
    M1 = cv2.moments(cnt1)
    cx1 = int(M1['m10']/M1['m00'])
    cy1 = int(M1['m01']/M1['m00'])
    cv2.circle(frame,(cx1,cy1), 5, (0,0,255), -1)
    M2 = cv2.moments(cnt2)
    cx2 = int(M2['m10']/M2['m00'])
    cy2 = int(M2['m01']/M2['m00'])
    cv2.circle(frame,(cx2,cy2), 5, (0,0,255), -1)

    # Next steps: find the center point between the two pieces of tape
    centerX = round((cx1 + cx2)/2)
    centerY = round((cy1 + cy2)/2)
    center = (centerX, centerY)
    cv2.circle(frame, center, 5, (255,0,0), -1)
    height, width, channels = frame.shape
    frame_center = (width, height)

    #find height and width of the actual frame
    height, width = frame.shape[:2]
    trueCenterX = int(width/2)
    trueCenterY = int(height/2)

    if(stable):
        M = np.float32([[1,0,(trueCenterX-centerX)],[0,1,(trueCenterY-centerY)]])
        dst = cv2.warpAffine(frame,M,(width,height))

        cv2.circle(dst, (trueCenterX, trueCenterY), 2, (255,255,255), -1)

        cv2.imshow("frame", dst)
        time.sleep(.05)
        cv2.waitKey(1)
    else:
        #mark center of actual frame
        cv2.circle(frame, (trueCenterX, trueCenterY), 2, (0,0,0), -1)

        #draw triangle from the center of the image to the center of the tape pieces
        cv2.line(frame, (trueCenterX, trueCenterY), center, (255,0,0), 2)
        cv2.line(frame, (trueCenterX, centerY), center, (0,255,0), 2)
        cv2.line(frame, (trueCenterX, trueCenterY), (trueCenterX, centerY), (0,0,255), 2)

        cv2.imshow("frame", frame)
        time.sleep(.05)
        cv2.waitKey(1)

    #write offsets to the network table 'MotionTracking'
    sd.putNumber('offsetX', trueCenterX-centerX)
    sd.putNumber('offsetY', trueCenterY-centerY)


cv2.destroyAllWindows()
