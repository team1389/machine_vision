from networktables import NetworkTables as nt
import numpy as np
import cv2
import sys
from utils import draw_contours

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


    (frame, centerX, centerY) = draw_contours(frame, cnts)
    center = (centerX, centerY)
    
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

cv2.destroyAllWindows()
