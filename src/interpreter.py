class GestureInterpreter:
    def __init__(self):
        self.gestureState = GestureState
        self.gestures = []
    
    def add_gesture(self, gesture):
        self.gestures.append(gesture)
    
    def check_for_gesture(self, cell_history, movement_history):
        for i in range(len(self.movement_history)):
            if self.movement_history[i] == "←":
                # We've detected the first step of a clockwise circle, so we enter that state to check for it
                self.gestureState.add_state(ClockwiseCirleState())
            elif self.movement_history[i] == "→":
                self.gestureState.add_state(CounterClockwiseCirleState())
        self.gestureState.process_movement(cell_history, movement_history)

#------------------------------------------------------------#

class GestureState():
    def __init__(self):
        self.states = []

    def process_movement(self, cell_history, movement_history):
        for state in self.states:
            state.process_movement(cell_history, movement_history)
    
    def add_state(self, state):
        self.states.append(state)
    
    def remove_state(self, state):
        self.states.remove(state)

#------------------------------------------------------------#
        
# A clockwise circle in this program is defined as:
# 1. A path has exited a starting cell
# 2. A path exhibits left, up, right, down
# 3. A path has re-entered the starting cell
# This circle then finds the furthest left, right, up, and down points
# and checks to see which markers are inside these the circle (yes, I know thats a square, but it works)
class ClockwiseCirleState(GestureState):
    def __init__(self, cell_history_, movement_history_):
        super().__init__()
        self.cell_history = cell_history_
        self.movement_history = movement_history_
        self.shape = ["←", "↑", "→", "↓"]
        self.tracked_movement = []

    # If the opposite movement of the expected movement is detected, break out of this state

    # def process_movement(self):
    #     for i in range(len(self.movement_history)):
    #         if self.movement_history[i] == "←":
    #             starting_cell = self.cell_history[i]
    #             print(starting_cell)

    def track_movement(self):
        # Check the length of the self.tracked_movement against the incoming directions
        # If the direction is the opposite of the expected direction, break out of this state
        # If the direction is the expected direction
        
        #TODO make this update in the cycle for loop
        desired_movement = self.shape[len(self.tracked_movement)]

        for i in range(len(self.movement_history)):
            if self.movement_history[i] == desired_movement:
                self.tracked_movement.append(self.movement_history[i])
                print(self.tracked_movement)
                if len(self.tracked_movement) == len(self.shape):
                    # we've found the shape, so run function
                    break
            #TODO make a dictionary of opposites of movements to reference
            elif self.movement_history[i] == "←":
                # We've detected the opposite movement of the expected movement, so we break out of this state
                self.tracked_movement = []
                break

        # if self.movement_history[i] == self.shape[i]:
        #     print("We've found the movement we wanted!!")
        #     self.tracked_movement.append(self.shape[i])
        # elif 
        # if self.tracked_movement[i] == self.shape[i]:
        #     self.look_for_next_movement(self.shape[i + 1])



class CounterClockwiseCirleState(GestureState):
    def __init__(self):
        super().__init__()
        self.shape = ["→", "↑", "←", "↓"]

    def process_movement(self, cell_history, movement_history):
        for i in range(len(movement_history)):
            if movement_history[i] == "→":
                starting_cell = cell_history[i]
                print(starting_cell)

class UnderlineState(GestureState):
    def __init__(self):
        super().__init__()
        self.shape = ["→", "→", "←", "←"]

    def process_movement(self, cell_history, movement_history):
        for i in range(len(movement_history)):
            if movement_history[i] == "→":
                starting_cell = cell_history[i]
                print(starting_cell)