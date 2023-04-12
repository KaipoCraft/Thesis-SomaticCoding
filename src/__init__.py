# This is the main script that will run the program.

import cv2
from cv2 import aruco
import numpy as np
import time
import os

import calibrate
import observer
import subject

# Set the variables for the aruco markers
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters()
marker_size = 100

# import the camera matrix and distortion coefficients
camera_matrix, dist_coeffs = calibrate.Calibrator(0, file_name='camera_calibration_desktop').get_matrix()

_observer = observer.GestureObserver()
_subject = subject.MarkerSubject(4)

_subject.attach_observer(_observer)

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

            for i in range(len(ids)):
                if ids[i] == 4:
                    _subject.update_center(corners[i])
                # Draw the axis
                frame_markers = cv2.drawFrameAxes(frame_markers, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 100)

                rotationMatrix, _ = cv2.Rodrigues(rvecs[i])

        cv2.imshow('frame', frame_markers)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    cv2.destroyWindow('frame')
    cap.release()