import numpy as np

class MarkerSubject:
    def __init__(self, marker_id):
        self.marker_id = marker_id
        self.observers = []
        self.previous_center = None
        self.center = None
        
    def attach_observer(self, observer):
        self.observers.append(observer)
        if len(self.observers) > 0:
            print("Observer attached to subject")

    def detach_observer(self, observer):
        self.observers.remove(observer)
        if len(self.observers) == 0:
            print("No observers attached to subject")
        
    def update_center(self, marker_corners):
        self.center = np.mean(marker_corners[0], axis=0).astype(int)
        if self.previous_center is not None and np.array_equal(self.center, self.previous_center):
            return
        self.previous_center = self.center

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.center)