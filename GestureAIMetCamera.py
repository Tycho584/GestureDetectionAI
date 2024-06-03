import mediapipe as mp
import mediapipe.python
import mediapipe.python.solutions.hands as mp_hands

import cv2

handMovement = {}

def getHandGestures(xPositionHand, yPositionHand):
    print(xPositionHand,yPositionHand)
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

    return handMovement

def  checkIfShipShouldShoot(xPosiitonThumb, yPositionThumb, xPositionIndex, yPositionIndex):
    print(xPosiitonThumb,yPositionThumb, xPositionIndex, yPositionIndex)


mp_drawing = mp.solutions.drawing_utils
# mediapipe_hands = mediapipe.solutions.hands
# mp_hands = hands.Hands

capture = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while capture.isOpened():
        ret, frame = capture.read()
        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detected_image = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
        if detected_image.multi_hand_landmarks:
            for hand_lms in detected_image.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_lms,
                                            mp_hands.HAND_CONNECTIONS,
                                            landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                                                color=(255, 0, 255), thickness=4, circle_radius=2),
                                            connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
                                                color=(20, 180, 90), thickness=2, circle_radius=2)
                                            )  

                for index, landmark in enumerate(hand_lms.landmark):
                    if index == 4:
                        checkIfShipShouldShoot(landmark.x, landmark.y, hand_lms.landmark[8].x, hand_lms.landmark[8].y)

                    if index == 9:
                        getHandGestures(landmark.x, landmark.y)
    
        cv2.imshow('Webcam', image)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
capture.release()
cv2.destroyAllWindows()