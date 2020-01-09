import cv2

print('cv2 version is ' + str(cv2.getVersionString()))


def capture_config():
    vc = cv2.VideoCapture(0)
    if not vc.isOpened():
        return False
    return vc


while True:
    cap = capture_config()
    if not cap:
        print('Unable to read camera feed')
        break
    grabbed, frame = cap.read()
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('captured frame', frame)
    cv2.imshow('greyed frame', grey)

    if cv2.waitKey(0) & 0xff == 27:
        break

cap.release()
cv2.destroyAllWindows()
