# This is the main script that will run the program.

# Import the external depencdecies
from cv2 import aruco
import sys
import argparse

# Import the necessary local scripts
import loop
sys.path.insert(0, '..\calibration')
import calibration.calibrate

# Set up the command-line argument parser
parser = argparse.ArgumentParser(description='Run the ARUCO marker detection program.')
parser.add_argument('--camera', type=int, default=0, help='the index of the camera to use (default: 1)')
parser.add_argument('--grid_size', type=int, default=6, help='the size of the grid (default: 6)')
parser.add_argument('--file_name', type=str, default='camera_calibration_nexigo', help='the name of the file containing the camera calibration data (default: camera_calibration_nexigo)')

# Parse the command-line arguments
args = parser.parse_args()

# Create the marker dictionary, which defines the string each marker corresponds to
marker_dict = {
    0: ["cursor", "cursor"],
    # Nouns
    1: ["bicycle", "noun"],
    2: ["elephant", "noun"],
    3: ["car", "noun"],
    4: ["dog", "noun"],
    5: ["cat", "noun"],
    6: ["house", "noun"],
    # Verbs
    7: ["run", "verb"],
    8: ["jump", "verb"],
    9: ["walk", "verb"],
    10: ["talk", "verb"],
    11: ["eat", "verb"],
    12: ["drink", "verb"],
    # Adjectives
    13: ["big", "adjective"],
    14: ["small", "adjective"],
    15: ["tall", "adjective"],
    16: ["short", "adjective"],
    17: ["fast", "adjective"],
    18: ["slow", "adjective"],
    # Noun-Professtions
    19: ["doctor", "noun"],
    20: ["teacher", "noun"],
    21: ["lawyer", "noun"],
    22: ["engineer", "noun"],
    23: ["scientist", "noun"],
    24: ["programmer", "noun"],
    # Colors
    25: ["red", "adjective"],
    26: ["orange", "adjective"],
    27: ["yellow", "adjective"],
    28: ["green", "adjective"],
    29: ["blue", "adjective"],
    30: ["purple", "adjective"],
    # Action verbs
    31: ["play", "verb"],
    32: ["sleep", "verb"],
    33: ["study", "verb"],
    34: ["work", "verb"],
    35: ["read", "verb"],
    36: ["write", "verb"],
}

# Create the marker dictionary, which will be used to store the markers once they're visible
# marker_dict = {}

# Set the variables for the aruco markers
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters()
marker_size = 100
primary_color = (145, 196, 153)
background_color = (230, 230, 230)
gesture_history_length = 7

# import the camera matrix and distortion coefficients
camera_matrix, dist_coeffs = calibration.calibrate.Calibrator(args.camera, args.file_name).get_matrix()

# Create the main object and generate the markers
loop_ = loop.Loop(args.camera, primary_color, args.grid_size, marker_dict, aruco_dict, parameters, marker_size, camera_matrix, dist_coeffs, gesture_history_length=gesture_history_length, background_color=background_color)
loop_.setup()
loop_.run()