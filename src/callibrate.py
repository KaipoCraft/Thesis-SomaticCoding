# Use this file to create the camera matrix and distortion coefficients

import numpy as np
import cv2
import os
import time

class Callibrator:
    def __init__(self, camera, num_images=20, chessboard_size=(9, 6), image_sie=(640, 480)):
        """
        This class is used to callibrate the camera matrix and distortion coefficients
        :param camera: The camera to callibrate (which is usually 0)
        :param num_images: The number of images to take to callibrate the camera (default is 20)
        :param chessboard_size: The size of the chessboard (default is (9, 6))
        :param image_size: The size of the image (default is (640, 480))
        """
        self.folder_name = "calibration_images"
        self.folder_path = os.getcwd()
        self.destination_folder = self.folder_path + '\\' + self.folder_name
        self.camera = camera
        self.matrix = []
        self.dist_coeffs = []
        self.num_images = num_images
        self.chessboard_size = chessboard_size
    
    def gatherImages(self):
        """
        This function is used to gather images to callibrate the camera
        """
        # Create the destination folder if it does not exist
        if not os.path.exists(self.destination_folder):
            os.mkdir(self.destination_folder)

        # Create the video capture object
        cap = cv2.VideoCapture(self.camera)

        for i in range(self.num_images):
            # Wait for 5 seconds
            time.sleep(5)
            
            print("Taking image " + str(i))
            
            ret, frame = cap.read()

            cv2.imshow('frame', frame)
            cv2.imwrite(self.destination_folder + '\\' + 'calibration_image' + str(i) + '.jpg', frame)

            filename = self.destination_folder + '\\' + 'calibration_image' + str(i) + '.jpg'
            cv2.imwrite(filename, frame)

            print(f'Saved {filename}')

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def callibrate(self):
        """
        This function is used to callibrate the camera matrix and distortion coefficients and save them to a .npz file in the destination folder
        """
        objp = np.zeros((self.chessboard_size[0] * self.chessboard_size[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:self.chessboard_size[0], 0:self.chessboard_size[1]].T.reshape(-1, 2)

        object_points = []
        image_points = []
        gray_images = []

        for file in os.listdir(self.destination_folder):
            if file.endswith('.jpg'):
                img = cv2.imread(self.destination_folder + '\\' + file)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray_images.append(gray)

                ret, corners = cv2.findChessboardCorners(gray, self.chessboard_size, None)

                if ret:
                    object_points.append(objp)
                    image_points.append(corners)
                    gray_images.append(img)

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, gray_images[0].shape[::-1], None, None)
        
        # Save the camera matrix and distortion coefficients
        np.savez('calibration.npz', mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)