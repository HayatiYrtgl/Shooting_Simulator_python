import cv2
import numpy as np


# class for masking
class BackgroundMasking:
    def __init__(self):

        self.fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=False)

    def background_subtracted(self, frame):
        fgmask = self.fgbg.apply(frame)
        return fgmask
