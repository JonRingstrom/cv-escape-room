# 01 - OpenCV: open an image and show it
# Put any photo called image.jpg in this folder, then run:
#   python 01_opencv_image.py      (press any key to close)

import cv2

img = cv2.imread("image.jpg")          # load the image
if img is None:
    raise SystemExit("Could not find image.jpg in this folder")

cv2.imshow("My image", img)            # show it in a window
cv2.waitKey(0)                         # wait until a key is pressed
cv2.destroyAllWindows()
