from networktables import NetworkTables
import sys
import cv2
import base64

NetworkTables.initialize(sys.argv[1])
sd = NetworkTables.getTable('pid_offset_values')


while(True):
	frame_raw = sd.getRaw('frame_raw', 'na')
	try:
		cv2.imshow('image', bytearray(frame_raw))
	except Exception:
		print("error decoding")
