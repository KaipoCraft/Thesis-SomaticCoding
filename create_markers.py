# Use this to generate the markers for detection:

import cv2
from cv2 import aruco
import numpy as np
import os

# Set the variables for the aruco markers
dictionary_id = aruco.DICT_6X6_250
marker_size = 100
markers_num = 37
folder_name = "markers"
folder_path = os.getcwd()

# Create a dictionary with 5 markers and 250 bits
dictionary = aruco.getPredefinedDictionary(dictionary_id)

# Create the marker images
marker_image = aruco.generateImageMarker(dictionary, 0, marker_size)

# Create the folder if it doesn't exist
if not os.path.exists(folder_path + "\\" + folder_name):
    os.mkdir(folder_path + "\\" + folder_name)

# Generate the markers
for i in range(markers_num):
    marker_id = i
    marker_image = np. zeros((marker_size, marker_size), dtype=np.uint8)
    marker = aruco.generateImageMarker(dictionary, marker_id, marker_size, marker_image, 1)

    # Define the border size and color
    inner_border_size = 2
    inner_border_color = [0, 0, 0]
    outer_border_size = 20
    outer_border_color = [255, 255, 255]

    # Add the borders to the marker
    bordered_marker = cv2.copyMakeBorder(marker, outer_border_size, outer_border_size, outer_border_size, outer_border_size, cv2.BORDER_CONSTANT, value=outer_border_color)
    bordered_marker = cv2.copyMakeBorder(bordered_marker, inner_border_size, inner_border_size, inner_border_size, inner_border_size, cv2.BORDER_CONSTANT, value=inner_border_color)

    # Save the marker
    cv2.imwrite(folder_path + "\\" + folder_name + "\\" + str(dictionary_id) + "_" + str(marker_id) + ".png", bordered_marker)