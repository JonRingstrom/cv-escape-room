# The royal family line  (EasyOCR, no training)
# Lay out the name tiles from father to son, click the webcam window,
# and press SPACE to check. Print tiles.png first. THYRA and KNUD are decoys.
#   python puzzle_royal_family.py           (SPACE = check, q = quit)

import cv2
import easyocr

ANSWER = ["GORM", "HARALD", "SVEND"]
NAMES = ["GORM", "HARALD", "SVEND", "THYRA", "KNUD"]    # every name on a tile

reader = easyocr.Reader(["en"])
cap = cv2.VideoCapture(0)
found = []
read_line = ""                          # everything EasyOCR read
message = "Press SPACE to check"
unlocked = False

while True:
    ok, frame = cap.read()
    if not ok:
        break

    key = cv2.waitKey(1)
    if key == ord(" ") and not unlocked:
        cv2.putText(frame, "Reading...", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow("The royal family line", frame)
        cv2.waitKey(1)
        found = reader.readtext(frame)
        read_line = "Read: " + ", ".join(text for box, text, conf in found)
        print(read_line)

        names = sorted((box[0][0], text.upper()) for box, text, conf in found if text.upper() in NAMES)
        order = [name for x, name in names]                  # the names from left to right

        # The rule: the names, left to right, are exactly the answer
        if order == ANSWER:
            unlocked = True
            message = "UNLOCKED: the royal line is restored!"
            print(message)                                   # open your lock here
        elif not order:
            message = "No names found, try again"
        else:
            message = "Wrong: " + " -> ".join(order) + ", try again"
    if key == ord("q"):
        break

    for box, text, conf in found:           # green = a known name, red = something else
        color = (0, 255, 0) if text.upper() in NAMES else (0, 0, 255)
        top_left = tuple(int(v) for v in box[0])
        bottom_right = tuple(int(v) for v in box[2])
        cv2.rectangle(frame, top_left, bottom_right, color, 2)
        cv2.putText(frame, text, (top_left[0], top_left[1] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    color = (0, 255, 0) if unlocked else (0, 255, 255)
    cv2.putText(frame, message, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, read_line, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.imshow("The royal family line", frame)

cap.release()
cv2.destroyAllWindows()
