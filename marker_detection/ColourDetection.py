import cv2
import numpy as np
import pyautogui
import pytesseract
import time


def nothing(x):
    pass


# video_stream = cv2.VideoCapture('video/yabi_resized.mp4')
img = cv2.imread('shapes.png')

# if math.sqrt((578-add_x)**2 + (345-add_y)**2) <= 80:
cv2.namedWindow('HSV')
cv2.resizeWindow('HSV', 640, 360)

cv2.createTrackbar('Hue min', 'HSV', 170, 255, nothing)  # 10 20 50 150 0 50
cv2.createTrackbar('Sat min', 'HSV', 98, 255, nothing)
cv2.createTrackbar('Value min', 'HSV', 55, 255, nothing)

cv2.createTrackbar('Hue max', 'HSV', 190, 255, nothing)
cv2.createTrackbar('Sat max', 'HSV', 255, 255, nothing)
cv2.createTrackbar('Value max', 'HSV', 255, 255, nothing)

while True:
    img = cv2.imread('shapes.png')
    # _, imageFrame = video_stream.read()

    h_min = cv2.getTrackbarPos("Hue min", "HSV")
    h_max = cv2.getTrackbarPos('Hue max', 'HSV')
    s_min = cv2.getTrackbarPos('Sat min', 'HSV')
    s_max = cv2.getTrackbarPos('Sat max', 'HSV')
    v_min = cv2.getTrackbarPos('Value min', 'HSV')
    v_max = cv2.getTrackbarPos('Value max', 'HSV')

    hsvFrame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Set range for red color and
    # define mask
    blue_lower = np.array([h_min, s_min, v_min], np.uint8)
    blue_upper = np.array([h_max, s_max, v_max], np.uint8)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    contours, hierarchy = cv2.findContours(blue_mask,
                                           cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(img, (x, y),
                                       (x + w, y + h),
                                       (255, 0, 0), 2)

            cv2.putText(imageFrame, "Red Colour", (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 0, 0))

    cv2.imshow("Multiple Color Detection in Real-TIme", blue_mask)

    # cv2.imshow('bremın', image)
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
# cap.release()
time.sleep(10)
cv2.destroyAllWindows()
