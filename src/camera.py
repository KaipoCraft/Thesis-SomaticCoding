# This script is in charge of running the camera

import cv2
import numpy as np
import time
import os

cap = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    cv2.destroyWindow('frame')
    cap.release()