# This script is in charge of running the camera

import cv2
import numpy as np
import time
import os

class Camera:
    def __init__(self, matrix_path):
        self.matrix = []
        self.matrix_path = matrix_path
        self.dist_coeffs = []

    def get_matrix(self):
        if not os.path.exists(self.matrix_path + '\\' + 'camera_calibration.npz'):
            print("File does not yet exist, go to callibrate.py to create it")
        else:
            print("Loading camera matrix")
            data = np.load(self.matrix_path + '\\' + 'camera_calibration.npz')
            self.matrix = data['mtx']
            self.dist_coeffs = data['dist']
        return self.camera_matrix, self.dist_coeffs