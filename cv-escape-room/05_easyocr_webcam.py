# 05 - EasyOCR: read text from the webcam
# Hold printed text up to the camera, click the webcam window,
# and press SPACE to read it.
#   python 05_easyocr_webcam.py     (SPACE = read, q = quit)

import cv2
import easyocr

reader = easyocr.Reader(["en"])         # downloads its models the first time
cap = cv2.VideoCapture(0)
found = []                              # the text from the last read
message = "Press SPACE to read text"

while True:
    ok, frame = cap.read()
    if not ok:
        break

    key = cv2.waitKey(1)
    if key == ord(" "):
        cv2.putText(frame, "Reading...", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.imshow("EasyOCR", frame)
        cv2.waitKey(1)                  # show "Reading..." while it works
        found = reader.readtext(frame)  # takes about a second
        words = [text for box, text, conf in found]
        message = "Read: " + ", ".join(words) if words else "No text found, try again"
        print(message)
    if key == ord("q"):
        break

    for box, text, conf in found:       # box = the 4 corners around the text
        top_left = tuple(int(v) for v in box[0])
        bottom_right = tuple(int(v) for v in box[2])
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(frame, text, (top_left[0], top_left[1] - 8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.putText(frame, message, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    cv2.imshow("EasyOCR", frame)

cap.release()
cv2.destroyAllWindows()
