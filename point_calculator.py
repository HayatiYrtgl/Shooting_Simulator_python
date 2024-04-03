import cv2
import numpy as np

# function for clculating the point
p7 = np.load("target_contours/head/7p.npy")
p8 = np.load("target_contours/head/8p.npy")
p9 = np.load("target_contours/head/9p.npy")
p10 = np.load("target_contours/head/10p.npy")


def calculate_points(x: int, y: int) -> str:
    puan = '6'
    coord = (x, y)
    # controls
    for points in p7:
        if cv2.pointPolygonTest(points, coord,  measureDist=False) > 0:
            puan = "7"
    for points in p8:
        if cv2.pointPolygonTest( points,coord, measureDist=False) > 0:
            puan = "8"
    for points in p9:
        if cv2.pointPolygonTest( points,coord, measureDist=False) > 0:
            puan = "9"
    for points in p10:
        if cv2.pointPolygonTest( points, coord, measureDist=False) > 0:
            puan = "10"
    return puan
