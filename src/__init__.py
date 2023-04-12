# This is the main script that will run the program.

import cv2
from cv2 import aruco
import numpy as np
import time
import os

import callibrate

# Set the variables for the aruco markers
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters()
marker_size = 100
# import the camera matrix and distortion coefficients
Callibrator = callibrate.Callibrator(0)
camera_matrix, dist_coeffs = Callibrator.get_matrix()

cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        height, width, channels = frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect the aruco markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        # Draw the markers
        frame_markers = aruco.drawDetectedMarkers(gray.copy(), corners, ids, borderColor=(0, 0, 255))

        # If we have detected a marker
        if ids is not None:
            # Get the pose of the marker
            rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, dist_coeffs)

        cv2.imshow('frame', frame_markers)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    cv2.destroyWindow('frame')
    cap.release()