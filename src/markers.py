from abc import ABC, abstractmethod
import numpy as np

class Marker(ABC):
    @abstractmethod
    def __init__(self, marker_id, data) -> None:
        self.marker_id = marker_id
        self.data = data
        self.marker_observers = []
        self.previous_centers = []
        self.marker_corners = None
        self.marker_center = None
        self.is_visible = False

    def attach_observer(self, observer):
        self.marker_observers.append(observer)

    def detach_observer(self, observer):
        self.marker_observers.remove(observer)
    
    def notify_observers(self):
        for observer in self.marker_observers:
            observer.update(self)

    def update_marker(self, corners, center, ids):
        self.marker_corners = corners
        self.marker_center = center
        self.previous_centers.append(center)
        if self.get_id in ids:
            self.is_visible = True
        else:
            self.is_visible = False

    def points_changed(self):
        self.notify_observers()

    def __str__(self) -> str:
        return f"Marker ID: {self.marker_id}, Marker Center: {self.marker_center}, Marker Corners: {self.marker_corners}"
    
    def get_id(self):
        return self.marker_id
    
    def get_data(self):
        return self.data

#------------------------------------------------------------#

class MarkerFactory:
    def __init__(self, marker_dict) -> None:
        self.marker_dict = marker_dict
    
    def make_markers(self):
        markers = []
        for marker_id, data in self.marker_dict.items():
            # print(str(marker_id) + ", " + str(data))
            markers.append(DataMarker(marker_id, data))
        return markers

#------------------------------------------------------------#

class CursorMarker(Marker):
    def __init__(self, marker_id, data) -> None:
        super().__init__(marker_id, data)
        self.cursor_observers = []

    def attach_observer(self, observer):
        super().attach_observer(observer)
    def detach_observer(self, observer):
        super().detach_observer(observer)
    def notify_observers(self):
        super().notify_observers()
    def get_data(self):
        return super().get_data()

    #TODO - Check for the cursor gesture
    def check_gesture():
        pass
    
    #TODO - Add the cursor gesture detection
    def gesture_detected():
        pass
            
class DataMarker(Marker):
    def __init__(self, marker_id, data):
        super().__init__(marker_id, data)
        self.data = data

    def attach_observer(self, observer):
        super().attach_observer(observer)
    def detach_observer(self, observer):
        super().detach_observer(observer)
    def notify_observers(self):
        super().notify_observers()
    def get_data(self):
        return super().get_data()