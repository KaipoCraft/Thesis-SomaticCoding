from abc import ABC, abstractmethod

@abstractmethod
class GestureCommand(ABC):
    def __init__(self, gestureBehavior) -> None:
        self.gestureBehavior = gestureBehavior

    def process(self):
        self.gestureBehavior.execute()

#------------------------------------------------------------#

class CircleCommand(GestureCommand):
    def __init__(self, gestureBehavior) -> None:
        super().__init__(gestureBehavior)
    
    def process(self):
        super().process()

class RightLeftLineCommand(GestureCommand):
    def __init__(self, gestureBehavior) -> None:
        super().__init__(gestureBehavior)
    
    def process(self):
        super().process()

class LeftRightLineCommand(GestureCommand):
    def __init__(self, gestureBehavior) -> None:
        super().__init__(gestureBehavior)
    
    def process(self):
        super().process()

class UpDownLineCommand(GestureCommand):
    def __init__(self, gestureBehavior) -> None:
        super().__init__(gestureBehavior)
    
    def process(self):
        super().process()

class DownUpLineCommand(GestureCommand):
    def __init__(self, gestureBehavior) -> None:
        super().__init__(gestureBehavior)
    
    def process(self):
        super().process()

class TapCommand(GestureCommand):
    def __init__(self, gestureBehavior) -> None:
        super().__init__(gestureBehavior)
    
    def process(self):
        super().process()