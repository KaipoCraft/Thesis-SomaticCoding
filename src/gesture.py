import markers

# A push and a pull obserrver
class GestureObserver:
    def __init__(self, marker_id, gesture_type) -> None:
        self.marker_id = marker_id
        self.gesture_type = gesture_type
        self.gesture_observers = []
        self.gesture = None

    # Find out what each marker is
    def update(self, marker):
        if marker.get_id() == self.marker_id:
            if self.gesture_type == 'cursor':
                self.gesture = marker.CursorGesture(marker)
            elif self.gesture_type == 'record':
                self.gesture = marker.RecordGesture(marker)
            self.notify_observers()
    
    # Push the data from the data marker

    # Record the gesture from the cursor marker