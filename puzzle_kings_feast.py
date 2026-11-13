# The king's feast  (YOLO26, no training)
# Set Harald's table: a cup, a bowl and a knife must all be seen at the same time.
#   python puzzle_kings_feast.py            (press q to quit)

import time
import cv2
from ultralytics import YOLO

NEEDED = {"cup", "bowl", "knife"}       # YOLO26 already knows these
HOLD_SECONDS = 1.5                      # how long the rule must hold

model = YOLO("yolo26n.pt")
KEEP = [i for i, name in model.names.items() if name in NEEDED]   # only look for these
cap = cv2.VideoCapture(0)
held_since = None
unlocked = False

while True:
    ok, frame = cap.read()
    if not ok:
        break

    result = model(frame, classes=KEEP, verbose=False)[0]
    seen = {result.names[int(box.cls)] for box in result.boxes if box.conf > 0.4}
    frame = result.plot()

    # The rule: everything we need is on the table
    if NEEDED <= seen:
        held_since = held_since or time.time()
        if time.time() - held_since > HOLD_SECONDS and not unlocked:
            unlocked = True
            print("UNLOCKED: the feast is ready!")      # open your lock here
    else:
        held_since = None

    missing = ", ".join(sorted(NEEDED - seen)) or "nothing"
    cv2.putText(frame, f"Missing: {missing}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    if unlocked:
        cv2.putText(frame, "UNLOCKED", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 0), 4)

    cv2.imshow("The king's feast", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
