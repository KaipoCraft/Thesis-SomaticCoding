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
        self.board = board.Board(self.camera_dims[0], self.camera_dims[1])
    
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
                for cell in self.board.get_cells():
                    for i in cell:
                        image = i.draw_cell(image, (255, 255, 255))

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

# class BoardFactory:
#     def __init__(self, frame_size, board_size=(5, 5)) -> None:
#         self.frame_size = frame_size
#         self.board_size = board_size
#         self.cell_height = self.frame_size[1] / self.board_size[1]
#         self.cell_width = self.frame_size[0] / self.board_size[0]

#     def make_board(self, image):
#         for i in range(self.board_size[0]):
#             y = i * self.cell_height
#             cv2.line(image, (0, int(y)), (self.frame_size[0], int(y)), (255, 255, 255), 1)
#         for j in range(self.board_size[1]):
#             x = j * self.cell_width
#             cv2.line(image, (int(x), 0), (int(x), self.frame_size[1]), (255, 255, 255), 1)
#         return image