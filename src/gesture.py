from abc import ABC, abstractmethod
import command

# A push and a pull observer
class GestureObserver(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self.gesture_observers = []
        self.gesture = None

    # Find out what each marker is
    def update(self, marker):
        if marker.get_id() == self.marker_id:
            if self.gesture_type == 'cursor':
                self.gesture = marker.CursorGesture(marker)
            elif self.gesture_type == 'record':
                self.gesture = marker.RecordGesture(marker)
            self.notify_observers()
    
    # Push the data from the data marker

    # Record the gesture from the cursor marker

# Command object to 
class Executioner(GestureObserver):
    def __init__(self) -> None:
        super().__init__()
        self.gesture = None

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