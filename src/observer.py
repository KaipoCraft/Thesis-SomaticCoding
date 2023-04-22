import gestures
import singleton
import factory

# The all knowing object that will execute the function associated with a gesture, and notify the display
class Executioner(metaclass=singleton.SingletonMeta):
    def __init__(self) -> None:
        self.active_data_markers = []
        self.gesture_list = [gestures.ClockwiseCircleGesture(), gestures.CounterClockwiseCircleGesture(), gestures.UnderlineGesture()]
        self.gesture_objects = factory.GestureFactory().make_gestures(self.gesture_list)
    
    def update(self, cell_history_, movement_history_):
        # Iterate through each gesture, checking to see if it has been found
        for gesture_object in self.gesture_objects:
            # Run the check inside each gesture object
            gesture_object.update(cell_history_, movement_history_)
            # If the gesture has been found, execute the corresponding command and stop looking for new gestures
            if gesture_object.found:
                altered_data = gesture_object.execute()
                break
    
    # Takes the detected gesture and executes the function associated with it
    def execute(self, detected_gesture):
        for gesture in self.gestures:
            if gesture == detected_gesture:
                gesture.execute()

    # Looks for active DataMarkers and makes changes to data based on the gesture
    def build_data_memory(self, detected_gesture):
        for gesture in self.gestures:
            if gesture == detected_gesture:
                gesture.build_data_memory()