import interpreter
import singleton

# The all knowing object that will execute the function associated with a gesture, and notify the display
class Executioner(metaclass=singleton.SingletonMeta):
    def __init__(self) -> None:
        self.gestures = None
        self.active_data_markers = []

    # Takes the detected gesture and executes the function associated with it
    def execute(self, detected_gesture):
        for gesture in self.gestures:
            if gesture == detected_gesture:
                gesture.execute()

    # Checks for gestures by passing the cell history to the interpreter
    def check_gesture(self, cell_history_, movement_history_):
        detected_gesture = interpreter.GestureInterpreter().interpret_gesture(cell_history_, movement_history_)
        # if detected_gesture:
        #     self.execute(detected_gesture)
        # else:
            # print("No gesture detected")