from networktables import NetworkTables
import sys
import cv2
import base64

NetworkTables.initialize(sys.argv[1])
sd = NetworkTables.getTable('pid_offset_values')


while(True):
	frame_raw = sd.getString('frame_raw', 'na')
	cv2.imshow('image', base64.b64decode(frame_raw))
