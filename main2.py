import cv2
import pickle
import cvzone
import numpy as np

# video feed
cap = cv2.VideoCapture("carPark.mp4")
# cap = cv2.VideoCapture("FF22-221111-033514-1920x1080.mp4")
# width, height = 107, 48
width, height = 273, 165

with open('CarParkPos', "rb") as f:
    posList = pickle.load(f)
# with open('TimePos', "rb") as f:
#     posList = pickle.load(f)

def checkParkingSpace(imgPro):
    spaceCounter = 0
    for pos in posList:
        x,y = pos
        imgCrop = imgPro[y:y+height, x:x+width]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)
        cvzone.putTextRect(img,str(count),(x,y+height-3), scale=1, thickness=2, offset=0)

        if count < 5706 or count > 8000:
            color = [0, 0, 255]
            thickness = 5
            spaceCounter=0
        else:
            color = [0,255,0]
            thickness = 2
            spaceCounter=1

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

    cvzone.putTextRect(img, str(spaceCounter), (100,50), scale=3, thickness=5, offset=20, colorR=(0,200,0))

while True:
    # replay video many times
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3,3),1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5) # remove dots

    kernel = np.ones((3,3), np.int8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1) # make thicker

    checkParkingSpace(imgDilate)

    # for pos in posList:
    #     cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)


    cv2.imshow("Image", img)
    # cv2.imshow("imgBlur", imgBlur)
    # cv2.imshow("imgThreshold", imgThreshold)
    # cv2.imshow("imgMedian", imgMedian)
    # cv2.imshow("imgDilate", imgDilate)
    if cv2.waitKey(1)==ord("q"):
        break