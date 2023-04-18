import cv2
from cv2 import aruco
import numpy as np

import markers
import gesture

class Main:
    def __init__(self, camera, marker_dict, aruco_dict, params, marker_size, camera_matrix, dist_coeffs):
        
        self.camera = camera
        self.marker_dict = marker_dict
        self.aruco_dict = aruco_dict
        self.params = params
        self.marker_size = marker_size
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs
        # Make a list for instantiated markers to be stored in
        self.my_markers = []
        # Instantiate the cursor marker upon initialization
        self.cursor = markers.CursorMarker(self.marker_dict[0][0], self.marker_dict[0][1])
        # Instantiate the data observers upon initialization
        self.gesture_observer = gesture.CursorObserver()
    
    def run_camera(self):
        cap = cv2.VideoCapture(self.camera)

        try:
            while True:
                ret, frame = cap.read()
                height, width, channels = frame.shape
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect the aruco markers
                corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.params)

                # Draw the markers
                image = aruco.drawDetectedMarkers(gray.copy(), corners, ids, borderColor=(255, 255, 255))

                # If we have detected a marker
                if ids is not None:
                    
                    # Process the markers
                    image = self.process_markers(corners, ids, image)

                cv2.imshow('frame', image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            cv2.destroyWindow('frame')
            cap.release()
        
    def process_markers(self, corners, ids, image):
        # Get the pose of the marker
        rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.camera_matrix, self.dist_coeffs)

        # print(int(self.my_markers[4].get_id()))
        # print(ids)

        # Go through visible ids and match them to the instantiated markers, updating them as visible
        # for id in ids:
            # print(self.my_markers[int(id)].get_id())
            # self.my_markers[int(id)].update(corners, True)

        for markers in self.my_markers:
            if markers.get_id() in ids:
                markers.update(corners, True)
                print(markers.get_id())
            else:
                markers.update(corners, False)

        # Iterate through the markers
        # for i in range(len(ids)):
            # print(self.my_markers[i].get_id())
            # print(self.my_markers[i].get_id())
            # image = cv2.drawFrameAxes(image, self.camera_matrix, self.dist_coeffs, rvecs[i], tvecs[i], 100)
            # image = cv2.drawFrameAxes(image, self.camera_matrix, self.dist_coeffs, rvecs[int(self.my_markers[i].get_id())], tvecs[int(self.my_markers[i].get_id())], 100)
        # Iterate through the markers
        # for m in range(len(self.my_markers)):
        #     image = cv2.drawFrameAxes(image, self.camera_matrix, self.dist_coeffs, rvecs[m], tvecs[m], 100)
        # for i in range(len(ids)):
        #     image = cv2.drawFrameAxes(image, self.camera_matrix, self.dist_coeffs, rvecs[i], tvecs[i], 100)

        # Use the observer pattern to update the markers

        return image
    
    def makeMarkers(self):
        # Create the marker factory
        marker_factory = markers.MarkerFactory(self.marker_dict)
        # Iterate through the marker dictionary
        for marker in self.marker_dict:
            # Create the marker
            marker = marker_factory.create_marker(marker, self.marker_dict[marker])
            # Add the marker to the list of instantiated markers
            self.my_markers.append(marker)
            print("Markers instantiated with following strings:")
            print(marker.get_data())