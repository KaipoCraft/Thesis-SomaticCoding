import numpy as np

class Marker:
    def __init__(self, marker_id, data) -> None:
        self.marker_id = marker_id
        self.data = data
        self.marker_observers = []
        self.previous_centers = []
        self.marker_corners = None
        self.marker_center = None
        self.is_visible = False

    def update(self, corners, is_visible):
        self.marker_corners = corners
        self.is_visible = is_visible
        self.notify_observers()

    def add_observer(self, observer):
        self.marker_observers.append(observer)

    def remove_observer(self, observer):
        self.marker_observers.remove(observer)
    
    def notify_observers(self):
        for observer in self.marker_observers:
            observer.update(self)

    def __str__(self) -> str:
        return f"Marker ID: {self.marker_id}, Marker Center: {self.marker_center}, Marker Corners: {self.marker_corners}"
    
    def get_data(self):
        return self.data
    
    def get_id(self):
        return self.marker_id

#------------------------------------------------------------#

class MarkerFactory:
    def __init__(self, marker_dict) -> None:
        self.marker_dict = marker_dict

    def create_marker(self, marker_id, data):
        if marker_id in self.marker_dict:
            return DataMarker(marker_id, data)
        else:
            return Marker(marker_id, data)

#------------------------------------------------------------#

class CursorMarker(Marker):
    def __init__(self, marker_id, data) -> None:
        super().__init__(marker_id, data)
        self.cursor_observers = []

    def update(self, corners, is_visible):
        super().update(corners, is_visible)

    def add_observer(self, observer):
        super().add_observer(observer)

    def remove_observer(self, observer):
        super().remove_observer(observer)

    def notify_observers(self):
        super().notify_observers()

    def check_shape(self):
        # Check what the shape of the cursor movement is
        pass
            
class DataMarker(Marker):
    def __init__(self, marker_id, data) -> None:
        super().__init__(marker_id, data)

    def update(self, corners, is_visible):
        super().update(corners, is_visible)
        self.previous_centers.append(self.marker_center)

    def add_observer(self, observer):
        super().add_observer(observer)

    def remove_observer(self, observer):
        super().remove_observer(observer)

    def notify_observers(self):
        super().notify_observers()