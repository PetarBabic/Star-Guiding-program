from PIL.Image import Image
import cv2 as cv
import numpy as np
import camera
import time

starX, starY = 0, 0
angle = 361
pulseStrenghtDir = np.array([1.00, 1.00, 1.00, 1.00], np.float32)

debug = True

#Zamjena za: binarized.item(j + 1, i + 1, 1) >= 255 and binarized.item(j - 1, i + 1, 1) >= 255 and binarized.item(j - 1, i - 1, 1) >= 255 and binarized.item(j + 1, i - 1, 1) >= 255 and binarized.item(j + 1, i, 1) >= 255 and binarized.item(j - 1, i, 1) >= 255 and binarized.item(j, i + 1, 1) >= 255 and binarized.item(j, i - 1, 1) >= 255 and binarized.item(j, i, 1) >= 255
def BrighterThanAverage(image, xOffset, yOffset, radius):
  average = np.mean(image)
  
  for y in range(-radius, radius + 1):
    for x in range(-radius, radius + 1):
      if ((x or y) and image.item(y + yOffset, x + xOffset, 1) < average):
        return False
  return True
   
def RotateImage(image, angle, pointX = 0, pointY = 0):
    if((pointX or pointY) == 0):
        pointX = image.shape[1] / 2
        pointY = image.shape[0] / 2
    
    M = cv.getRotationMatrix2D((pointX, pointY), angle, 1)  
    return cv.warpAffine(image, M, (image.shape[1], image.shape[0]))
   
def StarCenter(image):
    y = image.shape[0]
    x = image.shape[1]

    center = np.array([0, 0], np.uint8)
    
    blur = cv.GaussianBlur(image,(5,5),0)
    
    maxBrightness = np.max(image)
    
    ret, binarized = cv.threshold(blur, maxBrightness - 80, 255, cv.THRESH_BINARY)
    
    # Pocetne vrijednosti za izracun sredista zvijezde (najvece i najmanje vrijednosti koordinata zvijezde)
    maxX, maxY = 0, 0
    minX, minY = x, y
    n = 0

    # i = x
    # j = y
    for i in range(1, x - 1):       
        for j in range(1, y - 1):  
            # Looks if current pixel and pixels around it are brighter than 255     
            if(binarized.item(j + 1, i, 1) >= 255 and binarized.item(j - 1, i, 1) >= 255 and binarized.item(j, i + 1, 1) >= 255 and binarized.item(j, i - 1, 1) >= 255 and 
               binarized.item(j, i, 1) >= 255):
                if(j > maxY):
                    maxY = j
                if(i > maxX):
                    maxX = i
                if(j < minY):
                    minY = j
                if(i < minX):
                    minX = i
                    
                n += 1

    if(n >= 3 and n < x * y - x * y * 0.3 and np.min(binarized) == 0):    
        # Izracun koordinata centra zvijezde
        center = int((minY + maxY) / 2), int((minX + maxX) / 2)
        if(debug):
            print(center)

        return center
    
    else:
        print("No stars found")
        return -1, -1
  

# Calibrate the mount movment
def Calibrate(image):
    global angle
    global starX, starY
    global pulseStrenghtDir
    
    if(angle >= 361):
        # WEST
        # move the telescope westward 
        k = 0
        while(True):
            print("Moving west")
            camera.guide("W", 5)
            # capture new image
            imageW = cv.imread(camera.capture(1, 75))
            
            # for testing:
            # imageW = cv.imread("/Users/petar/Desktop/Astrofoto/zavrsni/stars/E1.tif")
            # end of testing
            
            roi = imageW[starY - 16:starY + 16, starX - 16:starX + 16]
                
            y2, x2 = StarCenter(roi)

            #Calculate the angle between top center and new star location
            #(3): https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
            angle1 = np.rad2deg(np.arctan2(y2 - 16, x2 - 16) - np.arctan2(16 - 16, 0 - 16)) % 360
    
            # For debuging      
            if(debug):
                print("Zapad: ", angle1)
                print("\tX: ", x2)
                print("\tY: ", y2)
            
            print("Moving east")
            # move telescope back
            camera.guide("E", 5)
            # capture new image
            image = cv.imread(camera.capture(1, 75))
            roi = image[starY - 16:starY + 16, starX - 16:starX + 16]
            # find star center coordinates
            y2, x2 = StarCenter(roi)
            if(x2 == -1):
                print("Calibration failed\nLost guide star")
                break
            starX += x2 - 16
            starY += y2 - 16
            # END
            
            
            # NORTH
            
            # move the telescope northward
            print("Moving north")
            camera.guide("N", 5)
            # capture new image
            imageN = cv.imread(camera.capture(1, 75))
            
            
            # for testing:
            # imageN = cv.imread("/Users/petar/Desktop/Astrofoto/zavrsni/stars/N1.tif")
            # end of testing
            
            roi = imageN[starY - 16:starY + 16, starX - 16:starX + 16]

            y2, x2 = StarCenter(roi)
            
            #Calculate the angle between right center and new star location
            #(3): https://stackoverflow.com/questions/1211212/how-to-calculate-an-angle-from-three-points
            angle2 = np.rad2deg(np.arctan2(y2 - 16, x2 - 16) - np.arctan2(0 - 16, 16 - 16)) % 360

            # For debuging
            if(debug):
                print("Istok: ", angle2)
                print("\tX: ", x2)
                print("\tY: ", y2)

            print("Moving south")
            # move telescope back
            camera.guide("S", 5)
            # capture new image
            image = cv.imread(camera.capture(1, 75))
            cv.imwrite("./stars/pulse-1.tif", image)
            roi = image[starY - 16:starY + 16, starX - 16:starX + 16]
            # find star center coordinates
            y2, x2 = StarCenter(roi)
            if(x2 == -1):
                print("Calibration failed\nLost guide star")
                break
            starX += x2 - 16
            starY += y2 - 16
            # END

            if(np.abs(angle1 - angle2) < 50):
                break
            print("Calibration failed...")
        print("Angle calibration success")
        
        angle = (angle1 + angle2) / 2
        
        
        # Calculateing the pulse strenght
        dir = np.array(["N", "S", "E", "W"])
        

        for i in range(4):           
            # move north, south, east, west
            print("Calculating pulse strenght: " + dir[i])

            camera.guide(dir[i], 5)

            image = cv.imread(camera.capture(1, 75))
            xOld = starX
            yOld = starY
            
            roi = image[starY - 16:starY + 16, starX - 16:starX + 16]
            starX += StarCenter(roi)[1] - 16
            starY += StarCenter(roi)[0] - 16

            image = RotateImage(image, angle, xOld, yOld)
            roi = image[yOld - 16:yOld + 16, xOld - 16:xOld + 16]
            
            dirY, dirX = StarCenter(roi)

            if(i <= 1):
                if(dirY != 16):
                    pulseStrenghtDir[i] = np.abs(5 / (dirY - 16))
                else:
                    i -= 1
            else:
                if(dirX != 16):
                    pulseStrenghtDir[i] = np.abs(5 / (dirX - 16))
                else:
                    i -= 1            
            print(pulseStrenghtDir)
            
            if(pulseStrenghtDir[i] > 1):
                i -= 1
            # strenght = guideTime / nPx
            # guideTime = strenght * nPx

        # capture image
        image = cv.imread(camera.capture(1, 75))
        roi = image[starY - 16:starY + 16, starX - 16:starX + 16]
        starX += StarCenter(roi)[1] - 16
        starY += StarCenter(roi)[0] - 16

        print("Pulse strenght calibration success")
        return 0
    
    return RotateImage(image, angle, starX, starY)

def Guide():
    global starX, starY
    print("Guiding")

    while True:
        guideTime = 0
        maxDir = "0"
        guideTime = 0
        minDir = "0"
            
        image = cv.imread(camera.capture(2, 75))

        image = Calibrate(image)
        roi = image[starY - 16:starY + 16, starX - 16:starX + 16]
        
        dirY, dirX = StarCenter(roi)

        if(dirY != -1):
            dirX -= 16
            dirY -= 16

            if(dirX > 0):
                maxTime = pulseStrenghtDir[0] * np.abs(dirX)
                if(maxTime > 2):
                    maxTime = 2

                maxDir = "W"
            elif(dirX < 0):
                maxTime = pulseStrenghtDir[1] * np.abs(dirX)
                if(maxTime > 2):
                    maxTime = 2

                maxDir = "E"
            else:
                maxTime = 0
            
            if(dirY > 0):
                minTime = pulseStrenghtDir[3] * np.abs(dirY)
                if(minTime > 2):
                    minTime = 2

                minDir = "N"
            elif(dirY < 0):
                minTime = pulseStrenghtDir[2] * np.abs(dirY)
                if(minTime > 2):
                    minTime = 2

                minDir = "S" 
            else:
                minTime = 0               
           
            if(minTime > maxTime):
                temp = maxTime
                maxTime = minTime
                minTime = temp

                temps = maxDir
                maxDir = minDir
                minDir = temps

            starTime = time.time()
            camera.StartGuide(maxDir)
            camera.StartGuide(minDir)
            
            if(maxTime > 2):
                maxTime = 2
            if(minTime > 2):
                minTime = 2
            
            if(maxTime != 0):
                while(time.time() < starTime + maxTime):
                    if(time.time() > starTime + minTime):
                        camera.StopGuide(minDir)
                camera.StopGuide(maxDir)

            print(maxDir + "\t" + str(maxTime))
            print(minDir + "\t" + str(minTime))
            
            time.sleep(2)

def click_event(event, x, y, flags, params):
    global starX, starY
    
    if event == cv.EVENT_LBUTTONDOWN:
        roi = image[y - 16:y + 16, x - 16:x + 16]
        
        y1, x1 = StarCenter(roi)

        x += x1 - 16
        y += y1 - 16

        roi = image[y - 16:y + 16, x - 16:x + 16]
        
        if(y1 != -1 or x1 != -1):
            cv.setMouseCallback('image', lambda *args : None)
            
            print("Done")
            
            starX = x
            starY = y

def StarSelect(posX, posY):
    global starX, starY, image
    
    image = cv.imread("./image_mono.tif")

    roi = image[posY - 16:posY + 16, posX - 16:posX + 16]
        
    y1, x1 = StarCenter(roi)

    posX += x1 - 16
    posY += y1 - 16

    roi = image[posY - 16:posY + 16, posX - 16:posX + 16]

    cv.imshow("roi", roi)
    
    if(y1 != -1 or x1 != -1):
        starX, starY = posX, posY
        return True

    else:
        return False

"""
image = cv.imread(camera.capture(1, 75))
cv.imwrite("/home/astroberry/Desktop/zavrsni/normal.tif", image)

camera.guide("N", 15)
image = cv.imread(camera.capture(1, 75))
cv.imwrite("/home/astroberry/Desktop/zavrsni/north.tif", image)

camera.guide("S", 15)
image = cv.imread(camera.capture(1, 75))
cv.imwrite("/home/astroberry/Desktop/zavrsni/south.tif", image)

camera.guide("E", 15)
image = cv.imread(camera.capture(1, 75))
cv.imwrite("/home/astroberry/Desktop/zavrsni/east.tif", image)

camera.guide("W", 15)
image = cv.imread(camera.capture(1, 75))
cv.imwrite("/home/astroberry/Desktop/zavrsni/west.tif", image)



image = cv.imread(camera.capture(1, 75))
# image = cv.imread("/Users/petar/Desktop/Astrofoto/zavrsni/stars/E0.tif")

while(True):
    cv.imshow("image", image)
    cv.setMouseCallback('image', click_event)

    if(starX != 0 or starY != 0):
        cv.destroyAllWindows()
        print("Found a star")
        break

    cv.waitKey(1)
    
cv.imshow("cal", Calibrate(image))
print("Rotation angle: ", angle)
cv.waitKey(0)
cv.destroyAllWindows()

Guide()

"""