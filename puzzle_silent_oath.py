# The silent oath  (MediaPipe Gestures, no training)
# Show the guard the secret hand signs in the right order:
# thumbs up, victory, open palm. A wrong sign starts it over.
# Needs gesture_recognizer.task (see INSTALL.txt)
#   python puzzle_silent_oath.py            (press q to quit)

import time
import cv2
import mediapipe as mp

SECRET = ["Thumb_Up", "Victory", "Open_Palm"]   # signs MediaPipe already knows
HOLD_SECONDS = 0.8                              # hold each sign this long

vision = mp.tasks.vision
options = vision.GestureRecognizerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path="gesture_recognizer.task"))
recognizer = vision.GestureRecognizer.create_from_options(options)

cap = cv2.VideoCapture(0)
step = 0                    # how many signs are done
last_sign, since = "None", time.time()
message = "Show the first sign"

while True:
    ok, frame = cap.read()
    if not ok:
        break
    h, w = frame.shape[:2]

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = recognizer.recognize(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))

    sign = "None"
    if result.gestures:                                  # the best guess for the first hand
        sign = result.gestures[0][0].category_name
        for point in result.hand_landmarks[0]:
            cv2.circle(frame, (int(point.x * w), int(point.y * h)), 4, (0, 255, 0), -1)

    if sign != last_sign:                                # a new sign: start the hold timer
        last_sign, since = sign, time.time()
    held = time.time() - since > HOLD_SECONDS

    # The rule: each sign in the secret order, held for a moment
    if held and step < len(SECRET):
        if sign == SECRET[step]:
            step += 1
            message = f"Good! {step} of {len(SECRET)}"
            if step == len(SECRET):
                message = "UNLOCKED: the guard lets you pass!"
                print(message)                           # open your lock here
        elif sign != "None" and (step == 0 or sign != SECRET[step - 1]):
            step = 0
            message = "Wrong sign, start over"

    cv2.putText(frame, message, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0) if step == len(SECRET) else (0, 255, 255), 2)
    cv2.putText(frame, f"Seeing: {sign}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("The silent oath", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
