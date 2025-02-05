from cvzone.HandTrackingModule import HandDetector
from threading import Thread
import cv2
import math


class Webcam:
    def __init__(self, src = 0, fps = 60, width = 120, height = 720) -> None:
        self.width, self.height = width, height
        self.fps = fps
        self.stopped = False
        self.src = src
        self.handMovement = {'middleFingerMCPXPosition': 471, 'middleFingerMCPYPosition': 261, 'moveLeft': False, 'moveRight': False, 'shoot': False}
        self.detector = HandDetector(maxHands=2, detectionCon=0.8, staticMode=True)


        self.stream = cv2.VideoCapture(src)
        # self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        # self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        # (self.grabbed, self.frame) = self.stream.read()
        print("Camera gestart")


    def getHandGestures(self, xPositionHand, yPositionHand):

        self.handMovement["middleFingerMCPXPosition"] = xPositionHand / self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.handMovement["middleFingerMCPYPosition"] = yPositionHand / self.stream.get(cv2.CAP_PROP_FRAME_WIDTH)

        if self.handMovement['middleFingerMCPXPosition'] <= 0.45:
            self.handMovement["moveLeft"] = True
        else:
            self.handMovement['moveLeft'] = False

        if self.handMovement['middleFingerMCPXPosition'] >= 0.55:
            self.handMovement['moveRight'] = True
        else:
            self.handMovement['moveRight'] = False


    def checkIfShipShouldShoot(self,xPositionThumb, yPositionThumb, xPositionIndex, yPositionIndex):
        print(xPositionIndex,yPositionIndex,xPositionThumb,yPositionThumb)

        distance = math.sqrt(pow(xPositionIndex - yPositionIndex, 2) + pow(xPositionThumb - yPositionThumb, 2))
        
        if distance <= 0.2 * self.stream.get(cv2.CAP_PROP_FRAME_WIDTH):
            self.handMovement['shoot'] = True
        else:
            self.handMovement['shoot'] = False

        print(distance)
        print(distance)
        print(distance)
        print(distance)

    def update(self):
        # Capture each frame from the webcam
        # 'success' will be True if the frame is successfully captured, 'img' will contain the frame
        success, img = self.stream.read()
        img = cv2.flip(img,1)

        # Find hands in the current frame
        # The 'draw' parameter draws landmarks and hand outlines on the image if set to True
        # The 'flipType' parameter flips the image, making it easier for some detections
        hands, img = self.detector.findHands(img, draw=True, flipType=True)

        # Check if any hands are detected
        if hands:
            # Information for the first hand detected
            hand1 = hands[0]  # Get the first hand detected
            lmList1 = hand1["lmList"]  # List of 21 landmarks for the first hand
            self.checkIfShipShouldShoot(lmList1[4][0], lmList1[4][1], lmList1[8][0], lmList1[8][1])
            self.getHandGestures(lmList1[9][0], lmList1[9][1])
            print(self.handMovement)
            print(lmList1[4][0])

            bbox1 = hand1["bbox"]  # Bounding box around the first hand (x,y,w,h coordinates)
            center1 = hand1['center']  # Center coordinates of the first hand
            handType1 = hand1["type"]  # Type of the first hand ("Left" or "Right")

            # Count the number of fingers up for the first hand
            fingers1 = self.detector.fingersUp(hand1)
            # print(f'H1 = {fingers1.count(1)}', end=" ")  # Print the count of fingers that are up

            # Calculate distance between specific landmarks on the first hand and draw it on the image
            length, info, img = self.detector.findDistance(lmList1[8][0:2], lmList1[12][0:2], img, color=(255, 0, 255),
                                                    scale=10)

            # # Check if a second hand is detected
            # if len(hands) == 2:
            #     # Information for the second hand
            #     hand2 = hands[1]
            #     lmList2 = hand2["lmList"]
            #     bbox2 = hand2["bbox"]
            #     center2 = hand2['center']
            #     handType2 = hand2["type"]

            #     # Count the number of fingers up for the second hand
            #     fingers2 = self.detector.fingersUp(hand2)
            #     print(f'H2 = {fingers2.count(1)}', end=" ")

            #     # Calculate distance between the index fingers of both hands and draw it on the image
            #     length, info, img = self.detector.findDistance(lmList1[8][0:2], lmList2[8][0:2], img, color=(255, 0, 0),
            #                                             scale=10)

            # print(" ")  # New line for better readability of the printed output

        # Display the image in a window
        cv2.imshow("Image", img)

        # Keep the window open and update it for each frame; wait for 1 millisecond between frames
        cv2.waitKey(1)



if __name__ == "__main__":
    camera = Webcam(1)
    while True:
        camera.update()
