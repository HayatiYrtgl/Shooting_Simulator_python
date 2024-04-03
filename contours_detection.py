import cv2
from point_calculator import calculate_points


# function for contours
def contours(get_frame, write_frame):
    """This method find contours and calculates the points"""

    contour, hierarchy = cv2.findContours(get_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contour:
        if cv2.contourArea(cnt) > 1000:

            # contour centroid
            M = cv2.moments(cnt)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(write_frame, (cX, cY), 7, (0, 255, 0), -1)

            # point calculation
            point_variable = calculate_points(cX, cY)

            return point_variable
