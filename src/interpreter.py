class GestureInterpreter:
    def __init__(self):
        self.states = []
        self.observers = []

    def attach_observer(self, observer):
        self.observers.append(observer)
    def detach_observer(self, observer):
        self.observers.remove(observer)
    def notify_observers(self, gesture):
        for observer in self.observers:
            observer.process_movement(gesture)

    def request_gesture(self, cell_history, movement_history):
        for state in self.states:
            gesture = state.process_movement(cell_history, movement_history)
            

#------------------------------------------------------------#
from abc import ABC, abstractmethod

@abstractmethod
class GestureSubject(ABC):
    def __init__(self):
        self.opposite_dictionary = {"←": "→", "→": "←", "↑": "↓", "↓": "↑"}
        self.tracked_movement = []

    def process_movement(self, cell_history_, movement_history_):
        # Check the length of the self.tracked_movement against the incoming directions
        # If the direction is the opposite of the expected direction, break out of this state
        # If the direction is the expected direction
        
        #TODO make this update in the cycle for loop
        desired_movement = self.shape[len(self.tracked_movement)]

        for i in range(len(movement_history_)):
            if movement_history_[i] == desired_movement:
                self.tracked_movement.append(movement_history_)
                print(self.tracked_movement)
                if len(self.tracked_movement) == len(self.shape):
                    # we've found the shape, so run function
                    self.notify_observers(self.shape)
            #TODO make a dictionary of opposites of movements to reference
            elif movement_history_[i] == self.opposite_dictionary[desired_movement]:
                # We've detected the opposite movement of the expected movement, so we break out of this state
                self.tracked_movement = []
                self.notify_observers(None)

#------------------------------------------------------------#
        
# A clockwise circle in this program is defined as:
# 1. A path has exited a starting cell
# 2. A path exhibits left, up, right, down
# 3. A path has re-entered the starting cell
# This circle then finds the furthest left, right, up, and down points
# and checks to see which markers are inside these the circle (yes, I know thats a square, but it works)
class ClockwiseCirle(GestureSubject):
    def __init__(self, cell_history_, movement_history_):
        super().__init__()
        self.cell_history = cell_history_
        self.movement_history = movement_history_
        self.shape = ["←", "↑", "→", "↓"]
        self.tracked_movement = []

    def process_movement(self):
        super().process_movement()

class CounterClockwiseCirle(GestureSubject):
    def __init__(self):
        super().__init__()
        self.shape = ["→", "↑", "←", "↓"]

    def process_movement(self, cell_history, movement_history):
        for i in range(len(movement_history)):
            if movement_history[i] == "→":
                starting_cell = cell_history[i]
                print(starting_cell)

class Underline(GestureSubject):
    def __init__(self):
        super().__init__()
        self.shape = ["→", "→", "←", "←"]

    def process_movement(self, cell_history, movement_history):
        for i in range(len(movement_history)):
            if movement_history[i] == "→":
                starting_cell = cell_history[i]
                print(starting_cell)