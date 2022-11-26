import cv2
import mediapipe as mp
import time


class poseDetector():

    def __init__(self, mode=False, upBody=False, smooth=True):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth)
        self.mpDraw = mp.solutions.drawing_utils

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(
                    img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img, draw=True):
        lmList = []

        if self.results.pose_landmarks:
            myPose = self.results.pose_landmarks
            for id, lm in enumerate(myPose.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        return lmList


def main(option):

    if option == 1:
        cap = cv2.VideoCapture(r"media\pose.mp4")
        detector = poseDetector()
        cTime = 0
        pTime = 0

        t_end = time.time() + 20
        while time.time() < t_end:
            sucess, img = cap.read()

            try:
                img = detector.findPose(img)
            except:
                break

            lmList = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                print(lmList[14])
                cv2.circle(img, (lmList[14][1], lmList[14][2]),
                           5, (0, 255, 0), cv2.FILLED)

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            cv2.putText(img, f'FPS:{str(int(fps))}', (10, 70),
                        cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            cv2.imshow("Image", img)
            cv2.setWindowProperty("Image", cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(10)

            if cv2.waitKey(1) % 256 == 27:
                # ESC pressed
                cap.release()
                break

        cap.release()
        cv2.destroyAllWindows()

    if option == 2:

        cap = cv2.VideoCapture(0)
        detector = poseDetector()
        cTime = 0
        pTime = 0
        t_end = time.time() + 30
        while time.time() < t_end:
            sucess, img = cap.read()

            try:
                img = detector.findPose(img)
            except:
                break

            lmList = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                print(lmList[14])
                cv2.circle(img, (lmList[14][1], lmList[14][2]),
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
