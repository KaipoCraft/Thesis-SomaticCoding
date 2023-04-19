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

    def update_marker(self, corners, ids):
        self.marker_corners = corners
        center = self.calculate_center(corners)
        self.marker_center = center
        
        if self.get_id in ids:
            self.is_visible = True
        else:
            self.is_visible = False

    def calculate_center(self, corners):
        # Get the center of the marker
        center = np.mean(corners, axis=0)
        return center

    def points_changed(self):
        self.notify_observers()

    def __str__(self) -> str:
        return f"Marker ID: {self.marker_id}, Marker Center: {self.marker_center}, Marker Corners: {self.marker_corners}"
    
    def get_center(self):
        return self.marker_center
    
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
            if data == 'cursor':
                markers.append(CursorMarker(marker_id, data))
            else:
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
    def update_marker(self, corners, ids):
        return super().update_marker(corners, ids)
    def calculate_center(self, corners):
        return super().calculate_center(corners)
    def points_changed(self):
        return super().points_changed()
    def __str__(self) -> str:
        return super().__str__()
    def get_center(self):
        return super().get_center()

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
        self.secondary_data = None

    def attach_observer(self, observer):
        super().attach_observer(observer)
    def detach_observer(self, observer):
        super().detach_observer(observer)
    def notify_observers(self):
        super().notify_observers()
    def get_data(self):
        return super().get_data()
    def update_marker(self, corners, ids):
        return super().update_marker(corners, ids)
    def calculate_center(self, corners):
        return super().calculate_center(corners)
    def points_changed(self):
        return super().points_changed()
    def __str__(self) -> str:
        return super().__str__()
    def get_center(self):
        return super().get_center()