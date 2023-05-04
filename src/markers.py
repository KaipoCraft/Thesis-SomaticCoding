from abc import ABC, abstractmethod
import numpy as np
import cv2
import calculations

class Marker(ABC):
    @abstractmethod
    def __init__(self, marker_id, data) -> None:
        '''
        Params:
            marker_id: The id of the marker
            data: The data that the marker will send
        '''
        self.marker_id = marker_id
        self.data = data
        self.marker_observers = []
        self.marker_center = None
        self.is_visible = False
        self.is_cursor = False
        self.current_cell = None

    def attach_observer(self, observer):
        self.marker_observers.append(observer)
    def detach_observer(self, observer):
        self.marker_observers.remove(observer)

    def calculate_center(self, corners):
        # Get the center of the marker
        # corners = corners[0]
        # print(corners)
        self.marker_center = np.mean(corners, axis=0)

    def draw_marker(self, image, color):
        # Draw the center
        radius = 10
        cv2.circle(image, (int(self.marker_center[0]), int(self.marker_center[1])), radius, color, -1)
        # cv2.putText(image, str(self.data), (int(self.marker_center[0]) + radius, int(self.marker_center[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        return image

    def get_center(self):
        return self.marker_center
    
    def get_id(self):
        return self.marker_id
    
    def get_data(self):
        return self.data
    
    def set_current_cell(self, cell_id):
        # self.current_cell = (cell_id)
        if cell_id == None:
            self.current_cell = None
        else:
            self.current_cell = [int(x) for x in cell_id.split(",")]

    def update_visibility(self):
        for observer in self.marker_observers:
            observer.update_visibility(self)

#------------------------------------------------------------#

class CursorMarker(Marker):
    def __init__(self, marker_id, data, history_length) -> None:
        super().__init__(marker_id, data)
        self.current_cell = None
        self.previous_cell = None
        self.cell_history = []
        self.direction_history = []
        self.data = None
        self.has_data = False
        self.history_length = history_length
        self.is_cursor = True
        self.direction_dict = {
            (1, 0): "←",
            (-1, 0): "→",
            (0, 1): "↓",
            (0, -1): "↑",
            # (1, 1): "↘",
            # (-1, 1): "↙",
            # (1, -1): "↗",
            # (-1, -1): "↖"
        }
    
    # When something the Executioner wants to know about the cursor changes, notify the Executioner
    def notify_observers(self):
        #TODO change so that the marker only notifies the Executioner when the history gets full
        for observer in self.marker_observers:
            observer.update(self.direction_history, self.cell_history)
    
    def update_marker(self, ids):
        # if self.current_cell is not None:
        self.build_history()
        if len(self.direction_history) >= self.history_length:
            self.notify_observers()
            self.direction_history = []
            self.cell_history = []

    def build_history(self):
        # print("Building history")
        # If this is the first cell, set the previous cell to the current cell and return
        if self.previous_cell is None:
            self.previous_cell = self.current_cell
            return
        # If the current cell is the same as the previous cell, return
        if self.current_cell == self.previous_cell:
            return
        # print("adding to history")
        # Calculate the direction of movement
        dir_x, dir_y = self.current_cell[0] - self.previous_cell[0], self.current_cell[1] - self.previous_cell[1]
        if abs(dir_x) == abs(dir_y):
            print("Matching x and y")
            self.previous_cell = self.current_cell
            return
        elif abs(dir_x) > abs(dir_y):
            dir_y = 0
        elif abs(dir_x) < abs(dir_y):
            dir_x = 0
        dx, dy = calculations.get_sign(dir_x), calculations.get_sign(dir_y)
        # If the direction of movement is not a valid key in the direction dictionary, return
        if (dx, dy) not in self.direction_dict.keys():
            print("Still not found" + dx + ", " + dy)
            self.previous_cell = self.current_cell
            return
        # Get the direction corresponding to the direction of movement
        direction = self.direction_dict[(dx, dy)]
        # If the length of the direction history is greater than or equal to the maximum length, remove the oldest direction and cell
        if len(self.direction_history) >= self.history_length:
            self.direction_history.pop(0)
            self.cell_history.pop(0)
        # Add the current direction and cell to the end of the direction history and cell history, respectively
        self.direction_history.append(direction)
        self.cell_history.append(self.current_cell)
        # Set the previous cell to the current cell
        self.previous_cell = self.current_cell

    def set_movement_history(self, direction_history, cell_history):
        self.direction_history = direction_history
        self.cell_history = cell_history
            
class DataMarker(Marker):
    def __init__(self, marker_id, data, data_type):
        super().__init__(marker_id, data)
        self.og_data = data
        self.data = data
        self.has_data = True
        # Holds the changes made to the data
        # A dictionary of the function and the result
        # self.memory = {"data": self.data}
        self.data_type = data_type

    def update_marker(self, ids):
        self.notify_observers()
    
    def notify_observers(self):
        for observer in self.marker_observers:
            observer.update_visibility(self)

    def write_data(self, result):
        self.data = result

    def get_memory(self):
        return self.memory
    
    def get_data_type(self):
        return self.data_type
    
    def set_data(self, data):
        self.data = data