from networktables import NetworkTables as nt
import numpy as np
import cv2
import sys

lower = np.array([85,50,50])
upper = np.array([93,255,255])

capture = cv2.VideoCapture(0)

nt.initialize()
pid_table = nt.getTable('pid_offset_values')

while True:

    success, frame = capture.read()
    tape_hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    res = cv2.inRange(tape_hsv, lower, upper)
    kernel = np.ones((4,4),np.uint8)
    opened = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)
    blur = cv2.blur(opened, (3,3))
    (_, cnts, _) = cv2.findContours(blur.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    try:
        
        cnt1 = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        cnt2 = sorted(cnts, key = cv2.contourArea, reverse = True)[1]

        rect1 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt1)))
        rect2 = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt2)))

        cv2.drawContours(frame, [rect1], -1, (255,0,0), 2)
        cv2.drawContours(frame, [rect2], -1, (255,0,0), 2)

        M1 = cv2.moments(cnt1)
        cx1 = int(M1['m10']/M1['m00'])
        cy1 = int(M1['m01']/M1['m00'])
        cv2.circle(frame,(cx1,cy1), 5, (0,0,255), -1)
        M2 = cv2.moments(cnt2)
        cx2 = int(M2['m10']/M2['m00'])
        cy2 = int(M2['m01']/M2['m00'])
        cv2.circle(frame,(cx2,cy2), 5, (0,0,255), -1)

        centerX = round((cx1 + cx2)/2)
        centerY = round((cy1 + cy2)/2)
        center = (centerX, centerY)
        cv2.circle(frame, center, 5, (255,0,0), -1)
        height, width, channels = frame.shape
        frame_center = (width, height)

        height, width = frame.shape[:2]
        trueCenterX = int(width/2)
        trueCenterY = int(height/2)

        pid_table.putNumber('offset_x', (trueCenterX-centerX)*-1)
        pid_table.putNumber('offset_y', (trueCenterY-centerY))

        cv2.circle(frame, (trueCenterX, trueCenterY), 2, (0,0,0), -1)
        cv2.line(frame, (trueCenterX, trueCenterY), center, (255,0,0), 2)
        cv2.line(frame, (trueCenterX, centerY), center, (0,255,0), 2)
        cv2.line(frame, (trueCenterX, trueCenterY), (trueCenterX, centerY), (0,0,255), 2)

        cv2.imshow("frame", frame)
        cv2.waitKey(1)
    except Exception:
	print("Error")

cv2.destroyAllWindows()
