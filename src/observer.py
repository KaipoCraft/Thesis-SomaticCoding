from abc import ABC, abstractmethod
import command

# A push and a pull observer
class GestureObserver(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.gesture_observers = []
        self.center = None
        self.previous_centers = []
        self.gesture = None

    # Find out what each marker is doing
    def update(self, marker):
        self.center = marker.marker_center
        self.previous_centers.append(marker.marker_center)
    
    # Push the data from the data marker

    # Record the gesture from the cursor marker

# The all knowing object that will execute the function associated with a gesture, and notify the display
class Executioner(GestureObserver):
    def __init__(self) -> None:
        super().__init__()

    def update(self, marker):
        super.update(marker)

    def attach_observer(self, observer):
        self.gesture_observers.append(observer)

    def detach_observer(self, observer):
        self.gesture_observers.remove(observer)

    def notify_observers(self):
        for observer in self.gesture_observers:
            observer.update(self)

    def execute(self):
        self.gesture.execute()

    def checkGesture(self):
        # check the previous centers of each marker to see if it matches a gesture
        # if it does, set the gesture to that gesture
        # if it doesn't, set the gesture to None

        #TODO make a gesture library to hold all the gestures
        self.gesture = None

class GestureLibrary:
    def __init__(self) -> None:
        self.gestures = []