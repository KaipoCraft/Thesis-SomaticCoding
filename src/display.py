from abc import ABC, abstractmethod
import cv2

# Abstract class that all displays will inherit from
class Display(ABC):
    @abstractmethod
    def __init__(self):
        self.display = None

    def update(self, marker):
        pass

# A display that will print what is happening with the markers to the console
class CodeDisplay(Display):
    def __init__(self) -> None:
        self.display = None

    def update(self, marker):
        pass