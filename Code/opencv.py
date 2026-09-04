from PIL.Image import Image
import cv2 as cv
import numpy as np
import time
from math import ceil
import camera


starX, starY = 0, 0
global image

if camera.binning == 2:
    img = np.zeros((1280 / 2, 960 / 2))
else:
    img = np.zeros((1280 / 2, 960 / 2))

#img = np.zeros((1280, 960), np.uint8)

def starCenter(image):
    x = image.shape[0]
    y = image.shape[1]

    averageColor = np.average(image)

    center = np.array([0, 0], np.uint8)

    k = 0

    for i in range(0, x - 2, 1):
        for j in range(0, y - 2, 1):
            if(image.item(j, i, 1) >= 255):
                if(image.item(j + 2, i, 1) >= averageColor and image.item(j - 2, i, 1) >= averageColor and image.item(j, i + 2, 1) >= averageColor and image.item(j, i - 2, 1) >= averageColor):
                    center[0] += i
                    center[1] += j

                    k += 1

    center[0] = int(center[0] / k + 0.5) # X
    center[1] = int(center[1] / k + 0.5) # Y

    return center


def click_event(event, x, y, flags, params):
    global starX, starY

    if event == cv.EVENT_LBUTTONDOWN:
        starX, starY = x, y
        roi = image[y - 16:y + 16, x - 16:x + 16]
        x1, y1 = starCenter(roi)

        x += x1 - 16
        y += y1 - 16

        starX, starY = x, y

        roi = image[y - 16:y + 16, x - 16:x + 16]

        cv.imshow("roi", roi)

        n = 0
        for i in range(32):
            for j in range(32):
                if roi[i, j, 1] == np.max(roi):
                    n += 1

        if(n > 7 and n < 512):
            cv.setMouseCallback('image', lambda *args : None)
            
            print("Done")

#camera.capture(1, 100)

def calibrate(image = None):
    global starX, starY

    if image == None:
    #Show the user captured image to select a star
        image = cv.imread(camera.capture(1, 100))
        cv.imshow('image', image)

        cv.setMouseCallback('image', click_event)   
        #cv.waitKey(0)
        x, y = starX, starY

        roi = image[y - 16:y + 16, x - 16:x + 16]
        x1, y1 = starCenter(roi)

        x += x1 - 16
        y += y1 - 16

        starX, starY = x, y

        roi = image[y - 16:y + 16, x - 16:x + 16]

        cv.imshow("roi", roi)

        n = 0
        for i in range(32):
            for j in range(32):
                if roi[i, j, 1] == np.max(roi):
                    n += 1

        if(n > 7 and n < 512):
            cv.setMouseCallback('image', lambda *args : None)
            
            print("Done")

        cv.waitKey(0)
        cv.destroyAllWindows()

        #Move mount north and capture second image
        print("Moving North...")
        camera.guide("N", 10)
        time.sleep(10)
        image = cv.imread(camera.capture(1, 100)) 
        print("Taking picture...")
        time.sleep(1)
        print("Moving South...")
        camera.guide("S", 10)
        time.sleep(11)

    else:
        image = cv.imread(image, 1)
        cv.imshow('image', image)

        cv.setMouseCallback('image', click_event)

        cv.waitKey(0)
        cv.destroyAllWindows()
        
    roi = image[starY - 16:starY + 16, starX - 16:starX + 16]
    x2, y2 = starCenter(roi)

    #Calculate the angle between sth...
    #(3): https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
    angle = np.rad2deg(np.arctan2(y2 - 16, x2 - 16) - np.arctan2(16 - 16, 0 - 16))
    print(angle)

    roi = image[starY - 64:starY + 64, starX - 64:starX + 64]

    M = cv.getRotationMatrix2D((roi.shape[0] / 2, roi.shape[1] / 2), angle, 1)
    rotated = cv.warpAffine(roi, M, (roi.shape[0], roi.shape[1]))

    roi = rotated[64 - 16:64 + 16, 64 - 16:64 + 16]

    cv.imshow("roi", roi)
    cv.imshow("img", image)
    cv.imshow("rot", rotated)

    cv.waitKey(0)
    cv.destroyAllWindows()

calibrate("image_mono.tiff")