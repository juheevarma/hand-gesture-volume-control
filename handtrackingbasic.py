import cv2
# Mediapipe is a ready-to-use and customizable Python solution as a prebuilt Python package
import mediapipe as mp
# to check frame rate, import time
import time 

# always to be done before we can start using this Mediapipe Hands module
mpHands = mp.solutions.hands 
""" default values -> static image mode (Flase) : if true, it makes the code slow since it is
always detecting, max_num_hands = 2, min_detection_confidence = 0.5 = 50%, 
min_tracking_confidence = 0.5 = 50% : if min_tracking_confidence < 0.5 then it detects """
hands = mpHands.Hands() 
mpDraw = mp.solutions.drawing_utils

previous_time = 0
current_time = 0
# web cam number 0
video_object = cv2.VideoCapture(0) 

# to run the web cam
while True:
    # gives us our frame
    success, image = video_object.read()
    # to convert to RGB since hands uses only RGB
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    results = hands.process(imageRGB)
    """print(results.multi_hand_landmarks)
    a for loop to check presence of multiple hands and extract them one by one"""
    if results.multi_hand_landmarks:
        # extracting information of each hand
        for hand_landmarks in results.multi_hand_landmarks:
            """ get Id no. and landmark information (X,Y) for each hand. 
            each ID has a corresponding landmark, each landmark has corresponding x, y and z. we'll use x & y 
            to find the landmark on the hand. These are in decimals (ratio of the image), and we need them to 
            be in pixels. To do this, we must multiply it with width and height to get pixel value."""
            for id, landmarks in enumerate(hand_landmarks.landmark):
                # print(id, landmarks)
                height, width, channel = image.shape
                center_x, center_y  = int(landmarks.x * width), int(landmarks.y * height)
                print(id, center_x, center_y) 
                # id is the points on hand in mediapipe hand module
                if id == 0:
                    # circle first id with radius 15
                    cv2.circle(image, (center_x, center_y), 15,  (255, 0, 255), cv2.FILLED)
            """ we don't draw on RGB image as we display only image captured
             mpHands.HAND_CONNECTIONS connects the dots """

            mpDraw.draw_landmarks(image, hand_landmarks, mpHands.HAND_CONNECTIONS) 
        
    current_time = time.time()
    # fps -> frame rate per second
    fps = 1/(current_time - previous_time)
    previous_time = current_time

    """ see the fps on the screen image instead of console, and round off to int, at position (10,70), font, scale
    and colour is purple(RGB(255, 0, 255)), thickeness   """
    cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0,255), 3)
    cv2.imshow("Image", image)
    cv2.waitKey(1)