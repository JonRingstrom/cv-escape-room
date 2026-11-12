# 03 - MediaPipe: find the body pose on the webcam
# Needs pose_landmarker_lite.task (see INSTALL.txt)
#   python 03_mediapipe_webcam.py   (press q to quit)

import cv2
import mediapipe as mp

vision = mp.tasks.vision
options = vision.PoseLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path="pose_landmarker_lite.task"))
landmarker = vision.PoseLandmarker.create_from_options(options)

cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    if not ok:
        break
    h, w = frame.shape[:2]

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)           # MediaPipe wants RGB
    result = landmarker.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))

    for person in result.pose_landmarks:                   # 33 points per person
        for point in person:                               # x and y go from 0 to 1
            cv2.circle(frame, (int(point.x * w), int(point.y * h)), 4, (0, 255, 0), -1)

        nose = person[0]                                   # point 0 is the nose
        cv2.putText(frame, f"nose: x={nose.x:.2f} y={nose.y:.2f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("MediaPipe pose", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
