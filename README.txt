COMPUTER VISION FOR ESCAPE ROOMS
================================

Simple, working Python examples for building escape room puzzles with a webcam.
Everything is free and runs on a normal laptop.


THE FOUR TOOLS
--------------
OpenCV      Reads, changes, shows and saves images and webcam frames
YOLO26      Finds objects and people, or objects you train it on
MediaPipe   Tracks bodies, hands and faces as points
EasyOCR     Reads printed text


GET STARTED
-----------
1. Follow INSTALL.txt once.
2. Run the examples in order, for example:

       python 02_opencv_webcam.py

3. Try the puzzles, then change them into your own.

Press q to close any window.


EXAMPLES (one tool per file)
----------------------------
01_opencv_image.py       Open image.jpg and show it
                         (put any photo called image.jpg in this folder)
02_opencv_webcam.py      Your webcam feed
03_mediapipe_webcam.py   Body points on the webcam
04_yolo_webcam.py        Boxes around objects and people
05_easyocr_webcam.py     Read text from the webcam (press SPACE)


PUZZLES
-------
puzzle_kings_feast.py    YOLO26      Put a cup, a bowl and a knife on the table
puzzle_shield_wall.py    MediaPipe   Stand shoulder to shoulder, shoulders level
puzzle_silent_oath.py    MediaPipe   Show the hand signs in order: thumbs up,
                                     victory, open palm
puzzle_royal_family.py   EasyOCR     Lay out the name tiles GORM, HARALD, SVEND
                                     (print tiles.png first, press SPACE to check)

Every puzzle has the same shape:
  1. Settings at the top: what is needed, how long it must hold.
  2. A webcam loop that runs the model on every frame.
  3. The rule, marked with a comment. Change this to make your own puzzle.
  4. UNLOCKED: put your lock, sound or Arduino code where this is printed.


TIPS
----
- Use steady light: fixed lamps, no window behind the players.
- Mount the camera firmly.
- Test with someone who has never seen the puzzle.
