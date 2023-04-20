from abc import ABC, abstractmethod
import numpy as np
import cv2

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

    def update_marker(self, corners, ids):
        self.marker_center = self.calculate_center(corners)
        for id in ids:
            # print(int(id))
            if self.get_id() == int(id):
                self.is_visible = True
            else:
                self.is_visible = False

    def calculate_center(self, corners):
        # Get the center of the marker
        center = np.mean(corners, axis=0)
        return center

    def draw_marker(self, image, color):
        # Draw the center
        radius = 10
        cv2.circle(image, (int(self.marker_center[0]), int(self.marker_center[1])), radius, color, -1)
        cv2.putText(image, str(self.data), (int(self.marker_center[0]) + radius, int(self.marker_center[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
        return image

    def get_center(self):
        return self.marker_center
    
    def get_id(self):
        return self.marker_id
    
    def get_data(self):
        return self.data
    
    def set_current_cell(self, cell):
        self.current_cell = cell

#------------------------------------------------------------#

class MarkerFactory:    
    @staticmethod
    def make_markers(markers):
        marker_list = []
        for marker_id, data in markers.items():
            if data == 'cursor':
                marker_list.append(CursorMarker(marker_id, data))
            else:
                marker_list.append(DataMarker(marker_id, data))
        return marker_list

#------------------------------------------------------------#

class CursorMarker(Marker):
    def __init__(self, marker_id, data) -> None:
        super().__init__(marker_id, data)
        self.current_cell = None
        self.previous_cell = None
        self.cell_history = []
        self.history_length = 10
        self.is_cursor = True

    def attach_observer(self, observer):
        super().attach_observer(observer)
    def detach_observer(self, observer):
        super().detach_observer(observer)
    def get_data(self):
        return super().get_data()
    def calculate_center(self, corners):
        return super().calculate_center(corners)
    def __str__(self) -> str:
        return super().__str__()
    def get_center(self):
        return super().get_center()
    def get_id(self):
        return super().get_id()
    def draw_marker(self, image, color):
        return super().draw_marker(image, color)
    def set_current_cell(self, cell):
        super().set_current_cell(cell)
    
    # When something the Executioner wants to know about the cursor changes, notify the Executioner
    def notify_observers(self):
        for observer in self.marker_observers:
            observer.check_gesture(self.cell_history)
    
    def update_marker(self, corners, ids):
        super().update_marker(corners, ids)
        self.build_history()
        self.notify_observers()
        return super().update_marker(corners, ids)
    
    # def build_history(self):
    #     if self.current_cell is None:
    #         return
    #     elif self.current_cell != self.previous_cell:
    #         # Take the current cell coordinates and the previous cell coordinates

    #         # subtract
    #         # figure out which direction
    
    def build_history(self):
        #TODO rebuild this to work to build the history as a series of moves (i.e. up, down, left, right)
        if self.current_cell is None:
            return
        elif self.current_cell != self.previous_cell:
            if len(self.cell_history) <= self.history_length:
                self.cell_history.append(self.current_cell)
            else:
                self.cell_history.pop(0)
                self.cell_history.append(self.current_cell)
            self.previous_cell = self.current_cell
            
class DataMarker(Marker):
    def __init__(self, marker_id, data):
        super().__init__(marker_id, data)
        self.data = data
        self.secondary_data = None

    def attach_observer(self, observer):
        super().attach_observer(observer)
    def detach_observer(self, observer):
        super().detach_observer(observer)
    # def notify_observers(self):
    #     super().notify_observers()
    def get_data(self):
        return super().get_data()
    def update_marker(self, corners, ids):
        return super().update_marker(corners, ids)
    def calculate_center(self, corners):
        return super().calculate_center(corners)
    def __str__(self) -> str:
        return super().__str__()
    def get_center(self):
        return super().get_center()
    def get_id(self):
        return super().get_id()
    def draw_marker(self, image, color):
        return super().draw_marker(image, color)
    def set_current_cell(self, cell):
        super().set_current_cell(cell)