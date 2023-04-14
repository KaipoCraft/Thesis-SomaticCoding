# This is the main script that will run the program.

import cv2
from cv2 import aruco

import calibrate
import main

marker_dict = {
    0: ("Hello", "string"),
    1: ("Goodbye", "string"),
    2: ("1", "int"),
    3: ("2", "int"),
    4: ("print", "function"),
    5: ("concat", "function"),
    6: ("add", "function"),
}

# Create the marker dictionary, which will be used to store the markers once they're visible
# marker_dict = {}

# Set the variables for the aruco markers
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters()
marker_size = 100

# import the camera matrix and distortion coefficients
camera_matrix, dist_coeffs = calibrate.Calibrator(0, file_name='camera_calibration_desktop').get_matrix()

_main = main.Main(0, marker_dict, aruco_dict, parameters, marker_size, camera_matrix, dist_coeffs)
_main.run_camera()