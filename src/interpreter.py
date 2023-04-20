class GestureInterpreter:
    def __init__(self):
        self.gestures = []
    
    def add_gesture(self, gesture):
        self.gestures.append(gesture)
    
    def check_for_gesture(self, cell_history):
        for gesture in self.gestures:
            if self.analyze(cell_history):
                return gesture
            
    def analyze(self, cell_history):
        # Compare the cell history to the gesture
        return True
