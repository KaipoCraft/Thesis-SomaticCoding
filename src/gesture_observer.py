# This code will keep an eye out for any recognized gestures
# and will call the appropriate function to handle them.

import numpy as np

class ObserverCalculator:
    def __init__(self, marker_corners):
        self.marker_corners = marker_corners

    def get_centers(self):
        center = np.mean(self.marker_corners[0], axis=0).astype(int)
        marker_position = center
        return marker_position

# class CircleObserver:
#     def __init__(self):