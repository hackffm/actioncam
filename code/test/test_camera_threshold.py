# thresholding on an image

import cv2
import sys

print(str(cv2.getBuildInformation()))


def capture_config():
    frame_height = 480
    frame_width = 640

    cap = cv2.VideoCapture(1)
    cap.set(3, frame_width)
    cap.set(4, frame_height)
    if not cap.isOpened():
        print('Unable to read camera feed')
        return False
    return cap

cap = capture_config()
if not cap:
    sys.exit()
(grabbed, frame) = cap.read()
# cv2.cvtColor is applied over the image input with applied parameters to convert the image in grayscale
img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# applying different thresholding techniques on the input image
# all pixels value above 120 will be set to 255
ret, thresh1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
ret, thresh2 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY_INV)
ret, thresh3 = cv2.threshold(img, 120, 255, cv2.THRESH_TRUNC)
ret, thresh4 = cv2.threshold(img, 120, 255, cv2.THRESH_TOZERO)
ret, thresh5 = cv2.threshold(img, 120, 255, cv2.THRESH_TOZERO_INV)

# the window showing output images with the corresponding thresholding
# techniques applied to the input images
cv2.imshow('Original Frame', frame)
cv2.imshow('Binary Threshold', thresh1)
cv2.imshow('Binary Threshold Inverted', thresh2)
cv2.imshow('Truncated Threshold', thresh3)
cv2.imshow('Set to 0', thresh4)
cv2.imshow('Set to 0 Inverted', thresh5)

# De-allocate any associated memory usage
if cv2.waitKey(0) & 0xff == 27:
    cap.release()
    cv2.destroyAllWindows()
