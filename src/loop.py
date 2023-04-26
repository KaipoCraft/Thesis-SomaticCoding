import tkinter as tk

import observer
import board
import singleton
import factory
import display

class Loop(metaclass=singleton.SingletonMeta):
    def __init__(self, primary_color: list, grid_size: tuple, marker_dict: dict, aruco_dict: object, params: object, marker_size: int, camera_matrix: object, dist_coeffs: object, gesture_history_length: int, background_color=(255,255,255), video_ratio: float=2/3):
        self.primary_color = primary_color
        self.grid_size = grid_size
        self.marker_dict = marker_dict
        self.aruco_dict = aruco_dict
        self.params = params
        self.marker_size = marker_size
        self.camera_matrix = camera_matrix
        self.dist_coeffs = dist_coeffs
        self.history_length = gesture_history_length
        self.video_ratio = video_ratio
        self.video_widget_size = (0, 0)
        self.gesture_observer = None
        self.my_markers = []
        
        self.board = board.Board()
        self.display = display.Display(self.aruco_dict, self.params, self.board, self.primary_color, background_color)

    def setup(self):
        self.set_size()

        self.board.generate_board(self.video_widget_size, self.grid_size)

        # Iterate through the marker dictionary and make each marker object based on the dictionary
        self.my_markers = factory.MarkerFactory.make_markers(self.marker_dict, self.history_length)
        self.gesture_observer = observer.Executioner(self.my_markers)
        self.gesture_observer.display_observer = self.display
        # Attach our observer to the markers
        for marker in self.my_markers:
            marker.attach_observer(self.gesture_observer)

        print(str(len(self.my_markers)) + " markers instantiated")

        self.display.set_marker_list(self.my_markers)
        self.display.setup()
    
    def run(self):
        self.display.run()

    def set_size(self):
        # Create a Tkinter window
        root = tk.Tk()
        root.title("OpenCV Video Feed")
        # Get the screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.screen_size = (screen_width, screen_height)

        video_widget_width = int(screen_width*self.video_ratio)
        video_widget_height = int(video_widget_width * 480/640)
        self.video_widget_size = (video_widget_width, video_widget_height)