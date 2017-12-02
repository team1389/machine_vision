import numpy as np
import cv2

def draw_contours(frame, cnts):
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
    return (frame, centerX, centerY)
