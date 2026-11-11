# Shield wall  (MediaPipe Pose, no training)
# Enough warriors stand shoulder to shoulder, with their shoulders level.
# Needs pose_landmarker_lite.task (see INSTALL.txt)
#   python puzzle_shield_wall.py            (press q to quit)

import time
import cv2
import mediapipe as mp

PEOPLE_NEEDED = 4          # set to 1 to test on your own
LEVEL = 0.3                # how level: max height difference, in shoulder widths
HOLD_SECONDS = 2.0         # how long the rule must hold

vision = mp.tasks.vision
options = vision.PoseLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path="pose_landmarker_lite.task"),
    num_poses=6)                                   # look for up to 6 people
landmarker = vision.PoseLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)
held_since = None
unlocked = False

while True:
    ok, frame = cap.read()
    if not ok:
        break
    h, w = frame.shape[:2]

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = landmarker.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))

    heights, widths = [], []
    for person in result.pose_landmarks:
        left, right = person[11], person[12]       # points 11 and 12 are the shoulders
        heights.append((left.y + right.y) / 2)
        widths.append(abs(left.x - right.x))
        cv2.line(frame, (int(left.x * w), int(left.y * h)), (int(right.x * w), int(right.y * h)), (0, 255, 0), 4)

    # The rule: enough people, and all shoulders at the same height
    people = len(heights)
    level = people > 0 and max(heights) - min(heights) < LEVEL * (sum(widths) / people)
    if people >= PEOPLE_NEEDED and level:
        held_since = held_since or time.time()
        if time.time() - held_since > HOLD_SECONDS and not unlocked:
            unlocked = True
            print("UNLOCKED: the shield wall holds!")    # open your lock here
    else:
        held_since = None

    cv2.putText(frame, f"Warriors: {people}/{PEOPLE_NEEDED}  Level: {'yes' if level else 'no'}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    if unlocked:
        cv2.putText(frame, "UNLOCKED", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 0), 4)

    cv2.imshow("Shield wall", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
