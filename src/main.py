import cv2
from cv2 import aruco
import numpy as np

import markers
import observer
import board

class Main:
    def __init__(self, camera, camera_dims, grid_size, marker_dict, aruco_dict, params, marker_size, camera_matrix, dist_coeffs):
        
        self.camera = camera
        self.camera_dims = camera_dims
        self.grid_size = grid_size
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
        self.gesture_observer = observer.Executioner()
        # Instantiate the board upon initialization
        self.board = None
    
    def run_camera(self):
        cap = cv2.VideoCapture(self.camera)
        # Create a named window
        cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
        # Set the window size
        cv2.resizeWindow("frame", self.camera_dims[0], self.camera_dims[1])

        try:
            while True:
                ret, frame = cap.read()
                height, width, channels = frame.shape
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect the aruco markers
                corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.params)

                # Draw the markers
                image = aruco.drawDetectedMarkers(gray.copy(), corners, ids, borderColor=(255, 255, 255))

                # Draw the grid
                image = self.board.draw_board(image)

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

        # Iterate through the detected markers
        for i in range(len(ids)):
            # Get the id of the marker
            id = ids[i][0]

            # Update the marker's points and whether or not it has been detected
            self.my_markers[id].update_marker(corners[i][0], ids)

            # Checks each of the cells for the marker
            for cell in self.board.get_cells():
                cell.marker_check(self.my_markers[id])

        return image
    
    def make_markers(self):
        # Create the marker factory
        marker_factory = markers.MarkerFactory(self.marker_dict)
        # Iterate through the marker dictionary
        self.my_markers = marker_factory.make_markers()
        # Attach our observer to the markers
        for marker in self.my_markers:
            marker.attach_observer(self.gesture_observer)
        
        # Print the instantiated markers
        print("Following markers instantiated:")
        for marker in self.my_markers:
            print(str(marker.get_id()) + ": " + str(type(marker).__name__), end=" ")
            if type(marker).__name__ == "DataMarker":
                  print(marker.get_data() + " || ", end="")
            else:
                print(" || ", end="")
            if marker.marker_observers is not None:
                print(str(len(marker.marker_observers)) + " observer(s) attached")
            else:
                print("No observer attached")

    def make_board(self):
        board_factory = board.BoardFactory(self.camera_dims[0], self.camera_dims[1], self.grid_size)
        self.board = board_factory.make_board()