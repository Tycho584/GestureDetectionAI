from threading import Thread
import mediapipe as mp
from cvzone import HandTrackingModule
import mediapipe.python
import mediapipe.python.solutions.hands as mp_hands
import cv2
import math

class Webcam:
    def __init__(self, src = 0, fps = 60, width = 120, height = 720) -> None:
        self.width, self.height = width, height
        self.fps = fps
        self.stopped = False
        self.src = src
        self.handMovement = {}
        self.detector = HandTrackingModule.HandDetector(maxHands=2, detectionCon=0.8, staticMode=True)
        self.mp_drawing = mp.solutions.drawing_utils


        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        (self.grabbed, self.frame) = self.stream.read()
        print("Camera gestart")

    def start(self):
        my_thread = Thread(target=self.update, args=())
        my_thread.start()
        print("de camera heeft thread id:", my_thread)

    def getHandGestures(self, xPositionHand, yPositionHand):

        handMovement = {}

        handMovement["middleFingerMCPXPosition"] = xPositionHand
        handMovement["middleFingerMCPYPosition"] = yPositionHand

        if handMovement['middleFingerMCPXPosition'] <= 0.45:
            handMovement["moveLeft"] = True
        else:
            handMovement['moveLeft'] = False

        if handMovement['middleFingerMCPXPosition'] >= 0.55:
            handMovement['moveRight'] = True
        else:
            handMovement['moveRight'] = False

        self.handMovement = handMovement

    def checkIfShipShouldShoot(self,xPositionThumb, yPositionThumb, xPositionIndex, yPositionIndex):
        print(xPositionIndex,yPositionIndex,xPositionThumb,yPositionThumb)

        distance = math.sqrt(pow(pow(xPositionIndex,2) - pow(yPositionIndex,2),2) + pow(pow(xPositionThumb,2) - pow(yPositionThumb,2),2))
        
        if distance <= 0.2:
            self.handMovement['schoot'] = True
        else:
            self.handMovement['shoot'] = False

        return self.handMovement

    def update(self):
        print("Update start")
        with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
            print("Handen gedetecteerd")
            while self.stream.isOpened():

                if self.stopped:
                    break

                ret, frame = self.stream.read()
                frame = cv2.flip(frame, 1)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                detected_image = hands.process(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if detected_image.multi_hand_landmarks:
                    for hand_lms in detected_image.multi_hand_landmarks:
                        self.mp_drawing.draw_landmarks(image, hand_lms,
                                                    mp_hands.HAND_CONNECTIONS,
                                                    landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                                                        color=(255, 0, 255), thickness=4, circle_radius=2),
                                                    connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                                                        color=(20, 180, 90), thickness=2, circle_radius=2)
                                                    )  

                        for index, landmark in enumerate(hand_lms.landmark):
                            if index == 4:
                                self.checkIfShipShouldShoot(landmark.x, landmark.y, hand_lms.landmark[8].x, hand_lms.landmark[8].y)


                            if index == 9:
                                self.getHandGestures(landmark.x, landmark.y)
                print(self.handMovement)

            self.stream.release()

    def stop(self):
        self.stopped = True

if __name__ == "__main__":
    camera = Webcam(0)
    camera.start()
    try:
        while True:
            pass
    except:
        print("Camera gestopt!!!")
        camera.stop()
