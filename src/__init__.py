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
    0: ("cursor"),
    # Prefix
    1: ("Pre"),
    2: ("Re"),
    3: ("Anti"),
    4: ("De"),
    5: ("Pro"),
    6: ("Intra"),
    # Root
    7: ("state"),
    8: ("click"),
    9: ("scroll"),
    10: ("zoom"),
    11: ("drag"),
    12: ("drop"),
    # Suffix
    13: ("select"),
    14: ("deselect"),
    15: ("undo"),
    16: ("redo"),
    17: ("copy"),
    18: ("paste"),
}

# Create the marker dictionary, which will be used to store the markers once they're visible
# marker_dict = {}

# Set the variables for the aruco markers
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_50)
parameters = aruco.DetectorParameters()
marker_size = 100
primary_color = (140, 125, 110)
background_color = (230, 230, 230)
gesture_history_length = 10

# import the camera matrix and distortion coefficients
camera_matrix, dist_coeffs = calibration.calibrate.Calibrator(args.camera, args.file_name).get_matrix()

# Create the main object and generate the markers
loop_ = loop.Loop(args.camera, primary_color, args.grid_size, marker_dict, aruco_dict, parameters, marker_size, camera_matrix, dist_coeffs, gesture_history_length=gesture_history_length, background_color=background_color)
loop_.setup()
loop_.run()