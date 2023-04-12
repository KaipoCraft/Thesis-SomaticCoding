import numpy as np

class FunctionBehavior:
    def __init__(self, function):
        self.function = function

    def execute(self, center):
        self.function(center)

#TODO check circle logic
class CircleBehavior(FunctionBehavior):
    def __init__(self, function):
        super().__init__(function)
        self.previous_centers = []
        self.radius_threshold = 5

    def execute(self, center):
        self.previous_centers.append(center)
        # Check if the last three centers form a circle
        if len(self.previous_centers) < 3:
            return False
        else:
            a, b, c = self.previous_centers[-3:]
            ab = np.linalg.norm(a-b)
            bc = np.linalg.norm(b-c)
            ac = np.linalg.norm(a-c)
            radius = (ab * bc * ac) / np.sqrt((ab + bc + ac) * (-ab + bc + ac) * (ab - bc + ac) * (ab + bc - ac))
            if radius > self.radius_threshold:
                self.function(center)
                return True
            else:
                return False

#TODO finish tap logic
class TapBehavior(FunctionBehavior):
    def __init__(self, function):
        super().__init__(function)
        self.previous_center = None

    def execute(self, center):
        if self.previous_center is not None and np.array_equal(center, self.previous_center):
            return
        self.previous_center = center
        self.function(center)

#TODO finish slide logic
class SlideBehavior(FunctionBehavior):
    def __init__(self, function):
        super().__init__(function)
        self.previous_center = None

    def execute(self, center):
        if self.previous_center is not None:
            self.function(center - self.previous_center)
        self.previous_center = center