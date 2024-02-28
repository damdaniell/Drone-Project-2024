import cv2
from matplotlib import pyplot as plt
from time import *
import os


folder_path = "C:/Users/datta/Desktop/VS Code Projects/Drone Camera/Drone Photos"
x = 1


def take_photo():
    i = x
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    cv2.imwrite(os.path.join(folder_path, "webcamphoto{}.jpg".format(i)), frame)

    plt.imshow(frame)
    plt.pause(1)


while x < 4:
    take_photo()
    sleep(5)
    x += 1
