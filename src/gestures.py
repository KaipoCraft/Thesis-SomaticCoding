import gestureBehavior

class Gesture:
    def __init__(self, shape_multiplier_=1):
        self.opposite_dictionary = {"←": "→", "→": "←", "↑": "↓", "↓": "↑"}
        self.tracked_movement = []
        self.shape = None
        self.shape_multiplier = shape_multiplier_
        self.shape_name = None
        self.needs_return_cell = True
        self.found = False
        self.observers = []
        self.execute_behavior = None

    def execute(self, active_data_markers_, display_):
        self.execute_behavior.execute(active_data_markers_, display_)
    def attach_observer(self, observer):
        self.observers.append(observer)
    def notify_observers(self):
        for observer in self.observers:
            observer.update(self.shape_name)
    # Adds the ability to increase the size of the gesture (could be useful for increased cell counts)
    def extend_shape(self):
        self.shape = ''.join([char * self.shape_multiplier for char in self.shape])

    def check_for_gesture(self, movement_history_, cell_history_):
        start_index = None

        # Run through every movement in the movement history
        for i in range(len(movement_history_)):
            
            # Check to see if we matched the shape
            if len(self.tracked_movement) == len(self.shape):
                # If we need to return to the start cell, we check to see if we are there
                # if self.needs_return_cell:
                #     if cell_history_[i] == start_index:
                #         print(f"{self.shape_name} found")
                #         self.tracked_movement = []
                #         self.found = True
                #         break
                #     else:
                #         self.tracked_movement = []
                #         start_index = None
                # If we don't need to return to the start cell, we just return True
                # else:
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
    
    def set_found(self, found_):
        self.found = found_

    def update_display(self, display_):
        display_.update(self.shape_name)

#------------------------------------------------------------#

class ClockwiseCircleGesture(Gesture):
    def __init__(self, shape_multiplier_=1):
        super().__init__(shape_multiplier_)
        self.shape = ["←", "↑", "→", "↓"]
        self.shape_name = "Clockwise Circle"
        self.needs_return_cell = True
        self.execute_behavior = gestureBehavior.GrammarTransformationBehavior()

class CounterClockwiseCircleGesture(Gesture):
    def __init__(self, shape_multiplier_=1):
        super().__init__(shape_multiplier_)
        self.shape = ["→", "↑", "←", "↓"]
        self.shape_name = "Counter-Clockwise Circle"
        self.needs_return_cell = True
        self.execute_behavior = gestureBehavior.ResetBehavior()

class UnderlineGesture(Gesture):
    def __init__(self, shape_multiplier_=1):
        super().__init__(shape_multiplier_)
        self.shape = ["←", "←", "←", "→", "→", "→"]
        self.shape_name = "Underline"
        self.needs_return_cell = False
        self.execute_behavior = gestureBehavior.AddToOutputBehavior()

class VerticalLineGesture(Gesture):
    def __init__(self, shape_multiplier_=1):
        super().__init__(shape_multiplier_)
        self.shape = ["↑", "↑", "↑", "↓", "↓", "↓"]
        self.shape_name = "Vertical Line"
        self.needs_return_cell = False
        self.execute_behavior = gestureBehavior.RunOutputBehavior()

# class BottomLineGesture(Gesture):
#     def __init__(self, shape_multiplier_=1):
#         super().__init__(shape_multiplier_)
#         self.shape = ["→", "→", "→"]
#         self.shape_name = "Bottom Line"
#         self.needs_return_cell = False
#         self.execute_behavior = gestureBehavior.CallChatGPTBehavior()

#     def check_for_gesture(self, movement_history_, cell_history_):
#         start_index = None

#         # Run through every movement in the movement history
#         for i in range(len(movement_history_)):
#             current_cell = cell_history_[i]
            
#             # Check to see if we matched the shape
#             if len(self.tracked_movement) == len(self.shape):
#                 print(f"{self.shape_name} found")
#                 self.tracked_movement = []
#                 self.found = True
#                 break
#             # Else, we keep checking for the shape
#             else:
#                 # The desired movement is the next movement in the shape
#                 desired_movement = self.shape[len(self.tracked_movement)]

#                 # If the movement in the history is the same as the desired movement and is in the bottom row, we add it to the tracked movement
#                 if movement_history_[i] == desired_movement and current_cell[1] == 5:
#                     self.tracked_movement.append(movement_history_[i])
#                     if start_index is None:
#                         start_index = current_cell
#                 # If the movement in the history is the opposite of the desired movement or is not in the bottom row, we reset the tracked movement
#                 elif movement_history_[i] == self.opposite_dictionary[desired_movement] or current_cell[1] != 5:
#                     self.tracked_movement = []
#                     start_index = None