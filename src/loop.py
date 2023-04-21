import cv2
from cv2 import aruco
import numpy as np
import screeninfo

import markers
import observer
import board
import singleton

class Loop(metaclass=singleton.SingletonMeta):
    def __init__(self, camera: int, primary_color: list, grid_size: tuple, marker_dict: dict, aruco_dict: object, params: object, marker_size: int, camera_matrix: object, dist_coeffs: object, gesture_history_length: int):
        '''
        Params:
            camera: the camera to use
            primary_color: the color of the board
            grid_size: the size of the board
            marker_dict: the dictionary of markers
            aruco_dict: the aruco dictionary
            params: the aruco parameters
            marker_size: the size of the markers
            camera_matrix: the camera matrix
            dist_coeffs: the distortion coefficients
        '''
        self.camera = camera
        self.primary_color = primary_color
        self.grid_size = grid_size
        self.marker_dict = marker_dict
        self.aruco_dict = aruco_dict
        self.params = params
        self.marker_size = marker_size
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs
        self.history_length = gesture_history_length
        # Will be set dynamically, but defaults to 1920x1080
        self.window_size = (1920, 1080)
        # Make a list for instantiated markers to be stored in
        self.my_markers = []
        # Instantiate the cursor marker upon initialization
        # self.cursor = markers.CursorMarker(self.marker_dict[0][0], self.marker_dict[0][1], gesture_history_length)
        # Instantiate the data observers upon initialization
        self.gesture_observer = observer.Executioner()
        # Instantiate the board upon initialization
        self.board = None
    
    def run_camera(self):
        '''
        Runs the camera
        '''
        cap = cv2.VideoCapture(self.camera)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.window_size[0])
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.window_size[1])
        
        # Create a window
        cv2.namedWindow("My Window", cv2.WINDOW_NORMAL)

        # Set the window to a normal state
        cv2.setWindowProperty("My Window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)        

        try:
            while True:
                ret, frame = cap.read()
                height, width, channels = frame.shape
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect the aruco markers
                corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.aruco_dict, parameters=self.params)

                # Draw the markers
                image = aruco.drawDetectedMarkers(gray.copy(), corners, ids, borderColor=(255, 255, 255))

                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

                # If we have detected a marker
                if ids is not None:
                    
                    # Process the markers
                    self.process_markers(corners, ids, image)
                    
                    for id in ids:
                        for cell in self.board.cells:
                            cell.check_for_markers(self.my_markers[id[0]])

                # Draw the grid
                image_final = self.board.draw_board(image, self.primary_color, self.window_size)

                cv2.imshow('frame', image_final)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except KeyboardInterrupt:
            cv2.destroyWindow('frame')
            cap.release()
        
    def process_markers(self, corners, ids, image):
        '''
        Run the update function in each marker that has been detected and update each cell
        Params:
            corners: the corners of the detected markers
            ids: the ids of the detected markers
            image: the image to draw on
        Returns:
            image: the image with the markers drawn on it
        '''
        detected_ids = [id[0] for id in ids]

        for id in detected_ids:
            self.my_markers[id].update_marker(corners[detected_ids.index(id)][0], ids[detected_ids.index(id)])
            # if self.my_markers[id].is_visible:
            self.my_markers[id].draw_marker(image, self.primary_color)

        return image
    
    def make_markers(self):
        '''
        Make the markers via the MarkerFactory and attach the observer to them
        '''
        # Iterate through the marker dictionary and make each marker object based on the dictionary
        self.my_markers = markers.MarkerFactory.make_markers(self.marker_dict, self.history_length)
        # Attach our observer to the markers
        for marker in self.my_markers:
            marker.attach_observer(self.gesture_observer)

        print(str(len(self.my_markers)) + " markers instantiated")

    def make_board(self):
        '''
        Make the board via the BoardFactory
        '''
        self.board = board.BoardFactory.make_board(self.window_size, self.grid_size)
        # self.board.attach_cell_observers(self.gesture_observer)

    def set_feed_dims(self):
        '''
        Get the window dimensions
        '''
        screen_size = (screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height)
        
        if self.window_size[0] > 1280 or self.window_size[1] > 720:
            self.window_size = (1280, 720)
        else:
            self.window_size = screen_size

        return self.window_size