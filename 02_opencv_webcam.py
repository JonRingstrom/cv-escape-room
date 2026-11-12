# 02 - OpenCV: show the webcam feed
#   python 02_opencv_webcam.py      (press q to quit)

import cv2

cap = cv2.VideoCapture(0)               # 0 = the first webcam, try 1 if it doesn't open

while True:
    ok, frame = cap.read()              # grab one frame
    if not ok:
        break

    frame = cv2.flip(frame, 1)          # mirror it, like a selfie camera
    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) == ord("q"):      # quit on q
        break

cap.release()
cv2.destroyAllWindows()
