import cv2
import numpy as np
from detection import DetectionClass
from masking import BackgroundMasking
from contours_detection import contours


# class for perspective transform main py
class MainClass:
    def __init__(self):

        # detection
        self.c = DetectionClass()
        self.coordinates = self.c.detect_and_extract()
        self.c.cap.release()

        # background masker
        self.bgmask = BackgroundMasking()

        # new video
        self.video = cv2.VideoCapture(0)

    def main_loop(self):
        while True:
            _, frame = self.video.read()
            frame = cv2.resize(frame, (640, 480))

            # source and destination
            source = np.float32(self.coordinates)
            dst = np.float32([[0, 0], [0, 480], [640, 480], [640, 0]])

            # perspective transform
            matrx = cv2.getPerspectiveTransform(source, dst)
            perspective_frame = cv2.warpPerspective(frame, matrx, (640, 480))

            # bg mask
            bgframe = self.bgmask.background_subtracted(frame=perspective_frame)

            # contours image
            point = contours(bgframe, perspective_frame)

            if point:
                print(point)

            cv2.imshow("frame", perspective_frame)

            if cv2.waitKey(1) == 27:
                break

        self.video.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    m = MainClass()
    m.main_loop()

