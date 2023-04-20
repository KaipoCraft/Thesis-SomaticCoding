import interpreter

# The all knowing object that will execute the function associated with a gesture, and notify the display
class Executioner():
    def __init__(self) -> None:
        self.gestures = None
        self.active_data_markers = []

    def update(self, marker):
        if marker.is_cursor:
            pass
        else:
            pass
    
    # def cell_update(self, cell):
    #     pass

    # Takes the detected gesture and executes the function associated with it
    def execute(self, detected_gesture):
        for gesture in self.gestures:
            if gesture == detected_gesture:
                gesture.execute()

    # Checks for gestures by passing the cell history to the interpreter
    def check_gesture(self, cell_history):
        detected_gesture = interpreter.GestureInterpreter().check_for_gesture(cell_history)
        if detected_gesture:
            self.execute(detected_gesture)