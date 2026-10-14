import pyautogui as pag
import cv2
import numpy as np

resolution = (1920, 1080)
codec = cv2.VideoWriter_fourcc(*"XVID")
filename = "Recording.avi"
fps = 60.0

output = cv2.VideoWriter(filename=filename, fourcc=codec, fps=fps, frameSize=resolution)

cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Live", 480, 270)

while True:
    img = pag.screenshot()
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output.write(frame)
    cv2.imshow("Live", frame)

    if cv2.waitKey(1) == ord("p"):
        break


output.release()
cv2.destroyAllWindows()

