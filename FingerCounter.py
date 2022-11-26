import cv2
import time
import os
import HandTrackingMod as htm

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

cTime = 0
pTime = 0

folderPath = r".\media\fingers"
myList = os.listdir(folderPath)
overLayList = []

detector = htm.handDetector(detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overLayList.append(image)

t_end = time.time() + 30
while time.time() < t_end:
    success, img = cap.read()

    try:
        img = detector.findHands(img)
    except:
        break

    lmList = detector.findPosition(img, draw=False)
    fingers = []

    if len(lmList) != 0:

        # First finger
        if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-1][2]:
                fingers.append(1)
            else:
                fingers.append(0)

    # Total fingers
    totalFingers = fingers.count(1)
    print(totalFingers)

    h, w, c = overLayList[totalFingers-1].shape
    img[0:h, 0:w] = overLayList[totalFingers-1]

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS:{str(int(fps))}', (450, 70),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.setWindowProperty("Image", cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(1)

    if cv2.waitKey(1) % 256 == 27:
        # ESC pressed
        cap.release()
        break
        
cap.release()
cv2.destroyAllWindows()
