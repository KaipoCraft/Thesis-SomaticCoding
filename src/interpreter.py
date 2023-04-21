import inspect

class GestureInterpreter:
    def __init__(self):
        self.gesture_list = [ClockwiseCircleGesture(), CounterClockwiseCircleGesture(), UnderlineGesture()]

    def update(self, shape_name):
        for gesture in self.gesture_list:
            if gesture.get_shape_name() == shape_name:
                gesture.execute()
                break

    def interpret_gesture(self, movement_history_, cell_history_):
        #TODO rework this so that if a gesture is found, it is executed and the loop breaks

        for gesture in self.gesture_list:
            if gesture.found:
                gesture.execute()
                break

#------------------------------------------------------------#

class GestureCommand:
    def __init__(self):
        self.opposite_dictionary = {"←": "→", "→": "←", "↑": "↓", "↓": "↑"}
        self.tracked_movement = []
        self.shape = None
        self.shape_name = None
        self.needs_return_cell = True
        self.found = False
        self.observers = []

    def execute(self):
        pass

    def attach_observer(self, observer):
        self.observers.append(observer)
    def detach_observer(self, observer):
        self.observers.remove(observer)
    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.shape_name)

    def check_for_gesture(self, movement_history_, cell_history_):

        start_index = None

        # Run through every movement in the movement history
        for i in range(len(movement_history_)):
            # Check to see if we matched the shape
            if len(self.tracked_movement) == len(self.shape):
                # If we need to return to the start cell, we check to see if we are there
                if self.needs_return_cell:
                    if cell_history_[i] == start_index:
                        print(f"{self.shape_name} found")
                        self.tracked_movement = []
                        self.found = True
                        break
                    else:
                        self.tracked_movement = []
                        start_index = None
                # If we don't need to return to the start cell, we just return True
                else:
                    print(f"{self.shape_name} found")
                    self.tracked_movement = []
                    self.found = True
                    break
            # Else, we keep checking for the shape
            else:
                # The desired movement is the next movement in the shape
                desired_movement = self.shape[len(self.tracked_movement)]

                # If the movement in the history is the same as the desired movement, we add it to the tracked movement
                if movement_history_[i] == desired_movement:
                    self.tracked_movement.append(movement_history_[i])
                    if start_index is None:
                        start_index = cell_history_[i]
                # If the movement in the history is the opposite of the desired movement, we reset the tracked movement
                elif movement_history_[i] == self.opposite_dictionary[desired_movement]:
                    self.tracked_movement = []
                    start_index = None

    def get_shape_name(self):
        return self.shape_name

#------------------------------------------------------------#

class ClockwiseCircleGesture(GestureCommand):
    def __init__(self):
        super().__init__()
        self.shape = ["←", "↑", "→", "↓"]
        self.shape_name = "Clockwise Circle"
        self.needs_return_cell = True

    def execute(self):
        print("Clockwise Circle Gesture Command")
    
    def check_for_gesture(self, movement_history_, cell_history_):
        super().check_for_gesture(movement_history_, cell_history_)

    def get_shape_name(self):
        super().get_shape_name()

class CounterClockwiseCircleGesture(GestureCommand):
    def __init__(self):
        super().__init__()
        self.shape = ["←", "↓", "→", "↑"]
        self.shape_name = "Counter-Clockwise Circle"
        self.needs_return_cell = True

    def execute(self):
        print("Counter-Clockwise Circle Gesture Command")
    
    def check_for_gesture(self, movement_history_, cell_history_):
        super().check_for_gesture(movement_history_, cell_history_)

    def get_shape_name(self):
        super().get_shape_name()

class UnderlineGesture(GestureCommand):
    def __init__(self):
        super().__init__()
        self.shape = ["←", "←", "←", "→", "→", "→"]
        self.shape_name = "Underline"
        self.needs_return_cell = False

    def execute(self):
        print("Underline Gesture Command")
    
    def check_for_gesture(self, movement_history_, cell_history_):
        super().check_for_gesture(movement_history_, cell_history_)

    def get_shape_name(self):
        super().get_shape_name()