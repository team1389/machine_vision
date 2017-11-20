# Reads a .mov video file from an iPhone
# Optionally write out the frames to jpg files but 
# we don't need that except maybe for testing

import cv2
vidcap = cv2.VideoCapture('./5-second-video.mov')
success,image = vidcap.read()
count = 0
success = True
while success:
  success,image = vidcap.read()
  print('Read a new frame: ', success)
  # cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  count += 1
