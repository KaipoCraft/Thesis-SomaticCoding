import numpy as np

class GestureObserver:
    def __init__(self):
        self.previous_centers = []
        self.radius_threshold = 5
        
    def update(self, center):
        print("Center updated")
        self.previous_centers.append(center)
    
    # def is_circular_motion(self):
    #     # Check if the last three centers form a circle
    #     if len(self.previous_centers) < 3:
    #         return False
    #     else:
    #         a, b, c = self.previous_centers[-3:]
    #         ab = np.linalg.norm(a-b)
    #         bc = np.linalg.norm(b-c)
    #         ac = np.linalg.norm(a-c)
    #         radius = (ab * bc * ac) / np.sqrt((ab + bc + ac) * (-ab + bc + ac) * (ab - bc + ac) * (ab + bc - ac))
    #         if radius > self.radius_threshold:
    #             return True
    #         else:
    #             return False

class FunctionGestureObserver(GestureObserver):
    def __init__(self, function):
        super().__init__()
        self.function = function
        
    def update(self, center):
        super().update(center)

class DataGestureObserver(GestureObserver):
    def __init__(self, data):
        super().__init__()
        self.data = data
        
    def update(self, center):
        super().update(center)