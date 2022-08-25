import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
# https://github.com/AndreMiras/pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#width and height of camera
wCam, hCam = 640, 480

capture = cv2.VideoCapture(0)
capture.set(3, wCam)
capture.set(4, hCam)
pTime = 0
# we increase detectionCon from 0.5 to 0.7 to make sure that what we detect is dfinitely a hand
detector = htm.handDetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# print(volume.GetVolumeRange())
# (-65.25, 0.0, 0.03125) -> output
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
while True:
    success, img = capture.read()
    # to find the hand position 
    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)
    # to avoid list index out of range
    if len(lmList) != 0: 
        # print(lmList[4])
        # print(lmList[8])
        # 4 -> tip of thumb, 8 -> tip of index finger
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        # to get center of the line between index and thumb
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        # to make sure we are using the correct ones
        # radius = 15
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED) 
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        # to create a line between the thumb and index
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        # circle for the center of line
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        # get length of line. volume cna be changed based on this. use hypotenuse function
        length = math.hypot(x2 - x1, y2 - y1)
        # hand range -> 50 to 300
        # volume range -> -65 to 0
        # convert volume range to hand range
        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
        if length < 50:
            # change the color of centre circle
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    # for the volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    # frame rate, current time and previous time
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    # image, output, position, font, scale, color, thickness
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Img", img)
    cv2.waitKey(1)