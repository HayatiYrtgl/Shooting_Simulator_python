import cv2
import numpy as np


# class for detection
class DetectionClass:

    # initializer
    def __init__(self):

        # read image
        self.image = cv2.imread("targets/head_target.jpg", cv2.IMREAD_GRAYSCALE)

        self.image = cv2.GaussianBlur(self.image, (5, 5), sigmaX=0)

        # camera var
        self.cap = cv2.VideoCapture(0)

        # sift object
        self.sift = cv2.SIFT.create()

        # key points and describe
        self.kp_image, self.desc_image = self.sift.detectAndCompute(self.image, None)

        # feature matching
        self.index_params = dict(algorithm=0, trees=10)  # tree default 5

        self.search_params = dict()

        # create flann
        self.flann = cv2.FlannBasedMatcher(indexParams=self.index_params, searchParams=self.search_params)

        # coordinates
        self.coordinates = []

    # detect function
    def detect_and_extract(self):
        """This method uses while loop to detect the given image from frame"""

        while True:
            _, frame = self.cap.read()

            # grayframe
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # key point
            kp_frame, desc_frame = self.sift.detectAndCompute(gray_frame, None)

            # match
            matches = self.flann.knnMatch(self.desc_image, desc_frame, k=2)

            # create good points
            good_points = []

            # fill the good points
            for m, n in matches:
                if m.distance < 0.6 * n.distance:
                    good_points.append(m)

            # if good points > 10
            if len(good_points) > 10:

                try:

                    # query and train points
                    query_pts = np.float32([self.kp_image[m.queryIdx].pt for m in good_points]).reshape(-1, 1, 2)
                    train_pts = np.float32([kp_frame[m.trainIdx].pt for m in good_points]).reshape(-1, 1, 2)

                    matrix, mask = cv2.findHomography(query_pts, train_pts, cv2.RANSAC, 5.0)

                    # image height and width
                    h, w = self.image.shape

                    # perspective transform
                    pts = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)

                    approx = cv2.perspectiveTransform(pts, matrix)

                    # perspective transform

                    # draw polygon
                    homography = cv2.polylines(frame, [np.int32(approx)], True, (255, 0, 0), 3)

                    approx = [np.int32(approx)]

                    # return section
                    left_top = approx[0][0][0]

                    left_bot = approx[0][1][0]

                    right_bot = approx[0][2][0]

                    right_top = approx[0][3][0]

                    self.coordinates.append([tuple(left_top), tuple(left_bot), tuple(right_bot), tuple(right_top)])

                    cv2.imshow("frame", homography)

                    if len(self.coordinates) == 10:
                        return self.coordinates[0]

                    # exit the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

                except:
                    cv2.imshow("frame", frame)
                    print("kamerayı sabit tutunuz...")
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

        # release the camera and close all windows
        self.cap.release()
        cv2.destroyAllWindows()





