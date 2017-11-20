from networktables import NetworkTables
from skvideo.io  import vread
import time
import cv2

NetworkTables.initialize('10.208.68.105')
sd = NetworkTables.getTable('MotionTracking')

offsetX = str(sd.getNumber('offsetX', 'N/A'))
offsetY = str(sd.getNumber('offsetY', 'N/A'))


while(True):
    newOffsetX = str(sd.getNumber('offsetX', 'N/A'))
    newOffsetY = str(sd.getNumber('offsetY', 'N/A'))
    if(offsetX != newOffsetX or offsetY != newOffsetY):
        print("\noffsetX: " + newOffsetX)
        print("offsetY: " + newOffsetY)
        offsetX = newOffsetX
        offsetY = newOffsetY
