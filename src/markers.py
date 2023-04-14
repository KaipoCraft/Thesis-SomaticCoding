import numpy as np

class Marker:
    def __init__(self, marker_id) -> None:
        self.marker_id = marker_id
        self.marker_detected = True
        self.marker_observers = []

    def update(self, marker):
        self.marker_id = marker.marker_id
        self.marker_corners = marker.marker_corners
        self.marker_center = marker.marker_center
        self.marker_detected = marker.marker_detected
        self.notify_observers()

    def __str__(self) -> str:
        return f"Marker ID: {self.marker_id}, Marker Center: {self.marker_center}, Marker Corners: {self.marker_corners}"

#------------------------------------------------------------#

class CursorMarker(Marker):
    def __init__(self, marker_id) -> None:
        super().__init__(marker_id)
        self.marker_observers = []
        self.radius_threshold = 10

    def update(self, marker):
        super().update(marker)

    def add_observer(self, observer):
        self.marker_observers.append(observer)
    
    def notify_observers(self):
        for observer in self.marker_observers:
            observer.update(self)

    def check_shape(self):
        # Check what the shape of the cursor movement is
        pass
            
class DataMarker(Marker):
    def __init__(self, marker_id) -> None:
        super().__init__(marker_id)
        self.previous_centers = []
        self.isVisible = False

    def update(self, marker):
        super().update(marker)
        self.previous_centers.append(self.marker_center)