from networktables import NetworkTables
#from skvideo.io  import vread
import sysS
import cv2

NetworkTables.initialize(sys.argv[1])
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
