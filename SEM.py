import cv2, vars, sys
from cvzone import HandTrackingModule
from camera import Camera, getCamera_src
from gui.gmain import gMain, terminateWindow
import mouseControl, gFrame
 
detector = HandTrackingModule.HandDetector(maxHands=2, detectionCon=0.8, staticMode=True)
# cameraList = getCamera_src()
camera = Camera(src=0).start()
 
vars.videoDimensions = camera.getVideoDimensions()
vars.touchPadSurface = (vars.videoDimensions[0] / 5 * 3, vars.videoDimensions[1] / 5 * 3)
vars.touchPadMargin = (vars.videoDimensions[0] / 5, vars.videoDimensions[1] / 5)
touchPadCornerPoints = ((vars.touchPadMargin[0], vars.touchPadMargin[1]), (vars.touchPadMargin[0] + vars.touchPadSurface[0], vars.touchPadMargin[1]), (vars.touchPadMargin[0] + vars.touchPadSurface[0], vars.touchPadMargin[1] + vars.touchPadSurface[1]), (vars.touchPadMargin[0], vars.touchPadMargin[1] + vars.touchPadSurface[1]))
vars.touchPadRect = gFrame.Rect(vars.touchPadMargin[0], 240 + vars.touchPadMargin[1], vars.touchPadSurface[0], vars.touchPadSurface[1])
 
previousPointerPos = (-100, -100)
 
def exit():
    camera.stop()
    terminateWindow()
    cv2.destroyAllWindows()
    sys.exit()
 
def main_loop(func):
    while vars.running:
        try:
            func()
        except KeyboardInterrupt:
            exit()
    exit()
           
 
@main_loop
def main():
    global previousPointerPos
    _, img = camera.read()
    if not vars.flipCamera:
        img = cv2.flip(img, -1)
 
    hands, img = detector.findHands(img, draw=True, flipType=vars.flipHand)
   
    if hands:
        leftHand1 = hands[0]
        lmlist1 = leftHand1["lmList"]
        pointer = (lmlist1[8][0], lmlist1[8][1])
       
        lmbDistance, info, img = detector.findDistance([lmlist1[4][0], lmlist1[4][1]], [lmlist1[6][0], lmlist1[6][1]], img)
        rmbDistance, info, img = detector.findDistance([lmlist1[4][0], lmlist1[4][1]], [lmlist1[5][0], lmlist1[5][1]], img)
       
        if gFrame.Draw.pointInPolygon(pointer, touchPadCornerPoints):
            movement, previousPointerPos = mouseControl.checkForPointerMovement(pointer, previousPointerPos)
           
            pointer = mouseControl.getMousePosFromFingerPos(*previousPointerPos)
            mouseControl.move(*pointer)
           
            if lmbDistance < 40 and not vars.fingerMakesClickGesture:
                vars.fingerMakesClickGesture = True
                mouseControl.click(*pointer)
           
            if lmbDistance >= 40 and vars.fingerMakesClickGesture:
                vars.fingerMakesClickGesture = False
                mouseControl.release(*pointer)
               
            if vars.fingerMakesClickGesture:
                mouseControl.drag(*pointer)
           
            if rmbDistance < 40 and not vars.fingerMakesRightClickGesture:
                vars.fingerMakesRightClickGesture = True
                mouseControl.rmbClick(*pointer)
               
            if rmbDistance >= 40 and vars.fingerMakesRightClickGesture:
                vars.fingerMakesRightClickGesture = False
                mouseControl.rmbRelease(*pointer)
           
           
           
       
    gMain(img)
