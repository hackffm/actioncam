# simple  image capture

# organizing imports
import cv2
import sys


print('cv2 version is ' + str(cv2.getVersionString()))


def capture_config():
    vc = cv2.VideoCapture(0)
    if not vc.isOpened():
        print('Unable to read camera feed')
        return False
    return vc


cap = capture_config()
if not cap:
    sys.exit()
(grabbed, frame) = cap.read()
grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

cv2.imshow('captured frame', frame)
cv2.imshow('greyed frame', grey)

# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cap.release()
    cv2.destroyAllWindows()
