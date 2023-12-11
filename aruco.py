#!/usr/bin/env python

# import the necessary packages
import argparse
import imutils
import cv2
import sys
import numpy as np

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
#     help="path to input image containing ArUCo tag")
# ap.add_argument("-t", "--type", type=str,
#     default="DICT_ARUCO_ORIGINAL",
#     help="type of ArUCo tag to detect")
# args = vars(ap.parse_args())

# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
    "DICT_4X4_50": cv2.aruco.DICT_4X4_50,
    "DICT_4X4_100": cv2.aruco.DICT_4X4_100,
    "DICT_4X4_250": cv2.aruco.DICT_4X4_250,
    "DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
    "DICT_5X5_50": cv2.aruco.DICT_5X5_50,
    "DICT_5X5_100": cv2.aruco.DICT_5X5_100,
    "DICT_5X5_250": cv2.aruco.DICT_5X5_250,
    "DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
    "DICT_6X6_50": cv2.aruco.DICT_6X6_50,
    "DICT_6X6_100": cv2.aruco.DICT_6X6_100,
    "DICT_6X6_250": cv2.aruco.DICT_6X6_250,
    "DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
    "DICT_7X7_50": cv2.aruco.DICT_7X7_50,
    "DICT_7X7_100": cv2.aruco.DICT_7X7_100,
    "DICT_7X7_250": cv2.aruco.DICT_7X7_250,
    "DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
    "DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
#	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
#	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
#	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
#	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

pocket_points = []

def detect_aruco(img):
    # load the input image from disk and resize it
    print("[INFO] loading image...")
    image = img
    image = imutils.resize(image, width=600)

    # verify that the supplied ArUCo tag exists and is supported by
    # OpenCV
    if ARUCO_DICT.get("DICT_6X6_100", None) is None:
        print("[INFO] ArUCo tag of '{}' is not supported".format("DICT_6X6_100"))
        sys.exit(0)

    # load the ArUCo dictionary, grab the ArUCo parameters, and detect
    # the markers
    print("[INFO] detecting '{}' tags...".format("DICT_6X6_100"))
    # arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT[args["type"]])
    # arucoParams = cv2.aruco.DetectorParameters_create()
    # (corners, ids, rejected) = cv2.aruco.detectMarkers(image, arucoDict,
    # 	parameters=arucoParams)

    dictionary = cv2.aruco.getPredefinedDictionary(ARUCO_DICT["DICT_6X6_100"])
    parameters =  cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)

    corners, ids, rejected = detector.detectMarkers(image)

    # verify *at least* one ArUco marker was detected
    if len(corners) > 0:
        # flatten the ArUco IDs list
        ids = ids.flatten()

        # loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
            # extract the marker corners (which are always returned in
            # top-left, top-right, bottom-right, and bottom-left order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners

            # convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            # draw the bounding box of the ArUCo detection
            # cv2.line(image, topLeft, topRight, (0, 255, 0), 2)
            # cv2.line(image, topRight, bottomRight, (0, 255, 0), 2)
            # cv2.line(image, bottomRight, bottomLeft, (0, 255, 0), 2)
            # cv2.line(image, bottomLeft, topLeft, (0, 255, 0), 2)

            # compute and draw the center (x, y)-coordinates of the ArUco
            # marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            # cv2.circle(image, (cX, cY), 4, (0, 0, 255), -1)

            # draw the ArUco marker ID on the image
            # cv2.putText(image, str(markerID),
            #     (topLeft[0], topLeft[1] - 15), cv2.FONT_HERSHEY_SIMPLEX,
            #     0.5, (0, 255, 0), 2)
            print("[INFO] ArUco marker ID: {}".format(markerID))

            # show the output image
            # cv2.imshow("Image", image)
            # cv2.waitKey(0)

            # Find pocket
            if markerID == 7:
                cv2.circle(image, (cX + 33, cY + 33), 4, (0, 0, 255), -1)
                pocket_points.append((cX + 33, cY + 33))
            elif markerID == 11:
                cv2.circle(image, (cX, cY + 28), 4, (0, 0, 255), -1)
                pocket_points.append((cX, cY + 28))
            elif markerID == 3:
                cv2.circle(image, (cX - 33, cY + 33), 4, (0, 0, 255), -1)
                pocket_points.append((cX - 33, cY + 33))
            elif markerID == 12:
                cv2.circle(image, (cX + 30, cY - 30), 4, (0, 0, 255), -1)
                pocket_points.append((cX + 30, cY - 30))
            elif markerID == 2:
                cv2.circle(image, (cX, cY - 22), 4, (0, 0, 255), -1)
                pocket_points.append((cX, cY - 22))
            elif markerID == 1:
                cv2.circle(image, (cX - 33, cY - 33), 4, (0, 0, 255), -1)
                pocket_points.append((cX - 33, cY - 33))

    f = open("pockets.txt", "w")
    for point in pocket_points:
        f.write(str(point) + "\n")
    f.close()
    
    return image
