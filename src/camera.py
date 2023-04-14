import cv2
from cv2 import aruco
import numpy as np

import markers

class Camera:
    def __init__(self, camera, marker_dict, aruco_dict, params, marker_size, camera_matrix, dist_coeffs):
        self.camera = camera
        self.marker_dict = marker_dict
        self.aruco_dict = aruco_dict
        self.params = params
        self.marker_size = marker_size
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs
        # Instantiate the cursor marker upon initialization
        self.cursor = markers.CursorMarker(self.marker_dict[0][0])
    
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
                frame_markers = aruco.drawDetectedMarkers(gray.copy(), corners, ids, borderColor=(0, 0, 255))

                # If we have detected a marker
                if ids is not None:
                    for id in ids:
                        # Check if we've already instantiated the cursor marker in the dictionary
                        # If not, instantiate it
                        if self.marker_dict[id.item()][0] in self.marker_dict:
                            self.marker_dict[self.marker_dict[id.item()][0]].update_state(id)
                        else:
                            self.marker_dict[self.marker_dict[id.item()][0]] = markers.Marker(id)

                        #TODO define the cursor marker ijn a variable
                        if id == 0:
                            self.cursor_marker.update_state(id)
                        else:
                            data_marker = markers.DataMarker(id)
                            self.cursor_marker.add_observer(data_marker)
                    # Process the markers
                    self.process_markers(corners, ids)

                    # for i in range(len(ids)):
    #                 if ids[i] == 4:
    #                     print(marker_dict[ids[i].item()][0])
    #                     _subject.update_center(corners[i])
    #                 # Draw the axis
    #                 frame_markers = cv2.drawFrameAxes(frame_markers, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 100)

    #                 rotationMatrix, _ = cv2.Rodrigues(rvecs[i])

                cv2.imshow('frame', frame_markers)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            cv2.destroyWindow('frame')
            cap.release()
        
    def process_markers(self, corners, ids):
        # Get the pose of the marker
        rvecs, tvecs, _objPoints = aruco.estimatePoseSingleMarkers(corners, self.marker_size, self.camera_matrix, self.dist_coeffs)

        # Use the observer pattern to update the markers