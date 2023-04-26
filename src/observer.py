import gestures
import singleton
import factory

# The all knowing object that will execute the function associated with a gesture, and notify the display
class Executioner(metaclass=singleton.SingletonMeta):
    def __init__(self, markers) -> None:
        self.markers = markers
        self.active_data_markers = []
        self.gesture_list = [gestures.ClockwiseCircleGesture(), gestures.CounterClockwiseCircleGesture(), gestures.UnderlineGesture(), gestures.VerticalLineGesture()]
    
    def update(self, movement_history_, cell_history_):
        # Iterate through each gesture, checking to see if it has been found
        for gesture_object in self.gesture_list:
            # Run the check inside each gesture object
            gesture_object.check_for_gesture(movement_history_, cell_history_)
            # If the gesture has been found, execute the corresponding command and stop looking for new gestures
            if gesture_object.found:
                gesture_object.execute(self.active_data_markers)
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

    def set_active_data_markers(self):
        for marker in self.markers:
            if marker.has_data & marker.is_visible:
                self.active_data_markers.append(marker)
            else:
                if marker in self.active_data_markers:
                    self.active_data_markers.remove(marker)