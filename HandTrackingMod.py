import cv2
import mediapipe as mp
import time


class handDetector():

    def __init__(self, mode=False, detectionCon=0.5):
        self.mode = mode
        self.detectionCon = detectionCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            self.mode)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []

        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        return lmList


def main(option):

    if option == 1:
        cap = cv2.VideoCapture(
            r"media\hands.mp4")
        detector = handDetector()
        pTime = 0
        cTime = 0
        t_end = time.time() + 20
        while time.time() < t_end:
            sucess, img = cap.read()
            
            try:
                img = detector.findHands(img)
            except:
                break

            lmList = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                print(lmList[1])
                cv2.circle(img, (lmList[1][1], lmList[1][2]),
                           5, (0, 255, 0), cv2.FILLED)

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            cv2.putText(img, f'FPS:{str(int(fps))}', (10, 70),
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

    if option == 2:
        cap = cv2.VideoCapture(0)
        detector = handDetector()
        pTime = 0
        cTime = 0
        t_end = time.time() + 30
        while time.time() < t_end:
            sucess, img = cap.read()

            try:
                img = detector.findHands(img)
            except:
                break

            lmList = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                print(lmList[1])
                cv2.circle(img, (lmList[1][1], lmList[1][2]),
                           5, (0, 255, 0), cv2.FILLED)

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            cv2.putText(img, f'FPS:{str(int(fps))}', (10, 70),
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


if __name__ == "__main__":
    main(1)
