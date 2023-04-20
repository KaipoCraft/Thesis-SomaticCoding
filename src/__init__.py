# This is the main script that will run the program.

# Import the external depencdecies
import cv2
from cv2 import aruco

# Import the necessary local scripts
import calibrate
import main

# Create the marker dictionary, which defines the string each marker corresponds to
marker_dict = {
    0: ("Hello"),
    1: ("Goodbye"),
    2: ("How are you?"),
    3: ("I'm fine, thank you"),
    4: ("What's your name?"),
    5: ("My name is"),
    6: ("Nice to meet you"),
    7: ("cursor"),
    8: ("click"),
    9: ("scroll"),
    10: ("zoom"),
    11: ("drag"),
    12: ("drop"),
    13: ("select"),
    14: ("deselect"),
    15: ("undo")
}

# Create the marker dictionary, which will be used to store the markers once they're visible
# marker_dict = {}

# Set the variables for the aruco markers
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters()
marker_size = 100
grid_size = 5 # size of the grid
primary_color = (245, 200, 25) # BGR

# import the camera matrix and distortion coefficients
camera_matrix, dist_coeffs = calibrate.Calibrator(0, file_name='camera_calibration_desktop').get_matrix()

# Create the main object and generate the markers
_main = main.Main(0, primary_color, grid_size, marker_dict, aruco_dict, parameters, marker_size, camera_matrix, dist_coeffs)
_main.make_board()
_main.make_markers()

# Main loop
_main.run_camera()