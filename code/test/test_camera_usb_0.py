import cv2

print('cv2 version is ' + str(cv2.getVersionString()))


def capture_config(camera_port=0):
    frame_height = 480
    frame_width = 640

    cap = cv2.VideoCapture(camera_port)
    cap.set(3, frame_width)
    cap.set(4, frame_height)
    if not cap.isOpened():
        print('Unable to read camera feed')
        return False
    return cap


cap = capture_config()
while cap:
    ret, frame = cap.read()

    cv2.imshow('captured frame', frame)

    if cv2.waitKey(0) & 0xff == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break
