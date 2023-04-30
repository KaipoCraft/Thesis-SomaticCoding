import gestures
import singleton

# The all knowing object that will execute the function associated with a gesture, and notify the display
class Executioner(metaclass=singleton.SingletonMeta):
    def __init__(self, markers) -> None:
        self.markers = markers
        self.visible_data_markers = []
        self.display = None
        self.gesture_list = [gestures.ClockwiseCircleGesture(), gestures.CounterClockwiseCircleGesture(), gestures.UnderlineGesture(), gestures.VerticalLineGesture()]

    def attach_observer(self, display):
        self.display = display
    def notify_display(self, gesture_name):
        self.display.update(gesture_name)
    
    def update(self, movement_history_, cell_history_):
        gesture_found = False
        # Iterate through each gesture, checking to see if it has been found
        for gesture_object in self.gesture_list:
            # Run the check inside each gesture object
            gesture_object.check_for_gesture(movement_history_, cell_history_)
            # If the gesture has been found, execute the corresponding command and stop looking for new gestures
            if gesture_object.found:
                gesture_object.execute(self.visible_data_markers, self.display)
                gesture_found = True
                break

    # def print_to_output(self, function_name, data):
    #     self.display.update(function_name, data)

    # def update_display(self, gesture_name):
    #     self.display_observer.update(gesture_name)
    
    # Takes the detected gesture and executes the function associated with it
    # def execute(self, detected_gesture):
    #     for gesture in self.gestures:
    #         if gesture == detected_gesture:
    #             gesture.execute()

    # Looks for active DataMarkers and makes changes to data based on the gesture
    # def build_data_memory(self, detected_gesture):
    #     for gesture in self.gestures:
    #         if gesture == detected_gesture:
    #             gesture.build_data_memory()

    def update_visibility(self, marker):
        if (marker.is_visible) & (marker not in self.visible_data_markers):
            self.visible_data_markers.append(marker)
        elif (not marker.is_visible) & (marker in self.visible_data_markers):
            self.visible_data_markers.remove(marker)