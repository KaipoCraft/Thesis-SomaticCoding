class GestureInterpreter:
    def __init__(self):
        self.gestures = []
    
    def add_gesture(self, gesture):
        self.gestures.append(gesture)
    
    def check_for_gesture(self, cell_history):
        for gesture in self.gestures:
            if gesture.analyze(cell_history):
                return gesture
