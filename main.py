import cv2
from matplotlib import pyplot as plt



def take_photo():
    i = 1
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()
    cv2.imwrite("webcamphoto{}.jpg".format(i), frame)

    i += 1
    plt.imshow(frame)
    plt.show()


def face_detection():
    capture = cv2.VideoCapture(0)

    dnn = cv2.dnn.readNetFromCaffe(
        "deploy.prototxt", "res10_300x300_ssd_iter_140000_fp16.caffemodel"
    )

    length = 300
    width = 300
    mean = [104, 117, 123]
    threshold = 0.7

    while capture.isOpened():
        ret, frame = capture.read()

        frame_height = frame.shape[0]
        frame_width = frame.shape[1]

        blob = cv2.dnn.blobFromImage(
            frame, 1.0, (length, width), mean, swapRB=False, crop=False
        )

        dnn.setInput(blob)
        detections = dnn.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > threshold:
                x_left_bottom = int(detections[0, 0, i, 3] * frame_width)
                y_left_bottom = int(detections[0, 0, i, 4] * frame_height)
                x_right_top = int(detections[0, 0, i, 5] * frame_width)
                y_right_top = int(detections[0, 0, i, 6] * frame_height)

                cv2.rectangle(
                    frame,
                    (x_left_bottom, y_left_bottom),
                    (x_right_top, y_right_top),
                    (0, 255, 0),
                )
                label = "Confidence: %.4f" % confidence
                label_size, base_line = cv2.getTextSize(
                    label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1
                )

                cv2.rectangle(
                    frame,
                    (x_left_bottom, y_left_bottom - label_size[1]),
                    (x_left_bottom + label_size[0], y_left_bottom + base_line),
                    (255, 255, 255),
                    cv2.FILLED,
                )
                cv2.putText(
                    frame,
                    label,
                    (x_left_bottom, y_left_bottom),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                )

        t, _ = dnn.getPerfProfile()
        label = "Inference time: %.2f ms" % (t * 1000.0 / cv2.getTickFrequency())
        cv2.putText(frame, label, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))

        cv2.imshow("Drone Camera", frame)

        key = cv2.waitKey(1)
        # Detects keystroke inputs

        if confidence > 0.9995:
            take_photo()

        if key == 27 or cv2.getWindowProperty("Drone Camera", cv2.WND_PROP_VISIBLE) < 1:
            break
        # 27 is the number that represents 'esc' and chekcs for window visibility of camera

    capture.release()
    cv2.destroyAllWindows()


face_detection()
