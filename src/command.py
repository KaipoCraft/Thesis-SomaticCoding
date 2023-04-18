from abc import ABC, abstractmethod

# An abstract class that all gestures forms will inherit from
class GestureCommand(ABC):
    @abstractmethod
    def __init__(self, gesture) -> None:
        self.gesture = gesture

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
    def __init__(self, gesture) -> None:
        super().__init__(gesture)

    def processString(self):
        return "Circle"
    
#------------------------------------------------------------#

class PrintBehavior(GestureBehavior):
    def __init__(self, marker) -> None:
        super().__init__(marker)

    def execute(self):
        print(self.marker.get_data())

#------------------------------------------------------------#

class OperationsReciever:
    def __init__(self) -> None:
        self.gesture = None

    def update(self, gesture):
        self.gesture = gesture

    def execute(self):
        self.gesture.execute()

