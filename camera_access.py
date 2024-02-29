import cv2
from matplotlib import pyplot as plt


def take_photo():
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    cv2.imwrite("webcamphoto.jpg", frame)

    plt.imshow(frame)
    plt.show()


def realtime_vid():
    capture = cv2.VideoCapture(0)

    while capture.isOpened():
        ret, frame = capture.read()

        cv2.imshow("Drone Camera", frame)

        key = cv2.waitKey(1)
        # Detects keystroke inputs

        if key == 27 or cv2.getWindowProperty("Drone Camera", cv2.WND_PROP_VISIBLE) < 1:
            break
        # 27 is the number that represents 'esc' and chekcs for window visibility of camera

    capture.release()
    cv2.destroyAllWindows()


realtime_vid()
