from abc import ABC, abstractmethod

# An abstract class that all gestures forms will inherit from
class GestureCommand(ABC):
    @abstractmethod
    def __init__(self, center_points) -> None:
        self.center_points = center_points

    def processString():
        pass

# An abstract class that all gesture-related functions will inherit from
class GestureBehavior(ABC):
    @abstractmethod
    def __init__(self, marker) -> None:
        self.marker = marker

    def execute(self):
        pass

#------------------------------------------------------------#

class Circle(GestureCommand):
    def __init__(self, center_points) -> None:
        super().__init__(center_points)

    def processString(self):
        # concatenate the visible strings of the present markers (leaving info that on each marker as "secondary data")
        return "Circle"
    
#------------------------------------------------------------#

class PrintBehavior(GestureBehavior):
    def __init__(self, center_points) -> None:
        super().__init__(center_points)

    def execute(self):
        print(self.marker.get_data())

#------------------------------------------------------------#

class OperationsReceiver:
    def __init__(self) -> None:
        self.gesture = None

    def update(self, gesture):
        self.gesture = gesture

    def execute(self):
        self.gesture.execute()

