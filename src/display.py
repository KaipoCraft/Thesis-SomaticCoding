import tkinter as tk
import cv2
from PIL import Image, ImageTk
from cv2 import aruco

import singleton

# Abstract class that all displays will inherit from
class Display(metaclass=singleton.SingletonMeta):
    def __init__(self, aruco_dict_, params_, board_ : object, primary_color_):
        self.aruco_dict = aruco_dict_
        self.params = params_
        self.board = board_
        self.primary_color = primary_color_

        # Create a Tkinter window
        self.root = tk.Tk()
        self.root.title("OpenCV Video Feed")

        # Get the screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Set the canvas size to maintain aspect ratio
        self.video_feed_width = int(self.screen_width*2/3)
        self.video_feed_height = int(self.video_feed_width * 480/640)

        # Create a canvas to hold the video feed
        self.canvas = None
        
        # Initialize the OpenCV capture object
        self.cap = cv2.VideoCapture(0)

    def setup(self):
        # Create a canvas to hold the video feed
        self.canvas = tk.Canvas(self.root, width=self.screen_width * 2/3 + 3, height=self.screen_height)
        self.canvas["bg"]="#%02x%02x%02x" % self.primary_color
        # self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.pack(side=tk.LEFT)
    
        # Create a label widget to display additional information
        self.label = tk.Label(self.root, text="Some additional information")
        self.label["bg"]="#%02x%02x%02x" % self.primary_color
        self.label.pack(side=tk.LEFT, padx=10, pady=10)


    # Define the video capture loop
    def video_loop(self):

        ret, frame = self.cap.read()
        if ret:
            # Convert the frame to RGB color space and resize it
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.resize(frame, (self.video_feed_width, self.video_feed_height))

            # Detect the aruco markers
            corners, ids, _ = aruco.detectMarkers(frame, self.aruco_dict, parameters=self.params)

            # Draw the markers
            frame = aruco.drawDetectedMarkers(frame.copy(), corners, ids, borderColor=(0, 0, 0))

            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            
            # Draw the grid
            frame = self.board.draw_board(frame, self.primary_color, (self.video_feed_width, self.video_feed_height))
            # If we have detected a marker
            if ids is not None:
                # Process the markers
                self.process_markers(corners, ids, frame)
                for id in ids:
                    for cell in self.board.cells:
                        cell.draw_active_cell(frame, self.primary_color)
                        cell.check_for_markers(self.my_markers[id[0]])
            
            frame = cv2.flip(frame, 1)
            
            # Create a PIL image from the OpenCV frame
            img = Image.fromarray(frame)

            # Accounts for the border width and the thickness of the grid lines
            x = 4
            y = (self.screen_height - self.video_feed_height) / 2

            imgtk = ImageTk.PhotoImage(image=img)
            
            try:
                # Update the canvas with the new image
                self.canvas.imgtk = imgtk

                self.canvas.create_image(x, y, anchor=tk.NW, image=imgtk)
                
            except tk.TclError as e:
                print(f"Error: {e}")
            
        # Call this function again after 10ms
        self.root.after(1, self.video_loop)
    
    # Define a function to exit the program when the user presses the "q" key
    def exit_program(self, event):
        if event.keysym == 'q':
            print("Exiting program...")
            self.root.quit()

    def run(self):
        # Bind the escape key event to the root window
        self.root.bind('<Key>', self.exit_program)
        
        # Make the window fullscreen
        self.root.attributes('-fullscreen', True)

        # Call the video loop function
        self.video_loop()

        # Start the Tkinter main loop
        self.root.mainloop()

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
    
    def set_marker_list(self, my_markers_):
        self.my_markers = my_markers_