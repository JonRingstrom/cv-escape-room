# 04 - YOLO26: find objects and people on the webcam
# yolo26n.pt downloads automatically the first time.
#   python 04_yolo_webcam.py        (press q to quit)

import cv2
from ultralytics import YOLO

model = YOLO("yolo26n.pt")              # n = nano, the smallest and fastest
cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    if not ok:
        break

    result = model(frame, verbose=False)[0]

    for box in result.boxes:            # one box per object found
        name = result.names[int(box.cls)]
        print(name, round(float(box.conf), 2))

    cv2.imshow("YOLO26", result.plot())     # plot() draws all boxes and labels
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
