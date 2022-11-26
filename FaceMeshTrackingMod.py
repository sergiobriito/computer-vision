import cv2
import mediapipe as mp
import time


class FaceMeshDetector():

    def __init__(self):
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=2)
        self.mpDraw = mp.solutions.drawing_utils
        self.drawSpec = self.mpDraw.DrawingSpec(
            thickness=1, circle_radius=1, color=(0, 255, 0))

    def findFaceMesh(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(imgRGB)

        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec)
        return img

    def findPosition(self, img, faceNo=0, draw=True):
        lmList = []

        if self.results.multi_face_landmarks:
            myFace = self.results.multi_face_landmarks[faceNo]
            for id, lm in enumerate(myFace.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return lmList


def main(option):

    if option == 1:
        cap = cv2.VideoCapture("./media/face.mp4")
        cTime = 0
        pTime = 0
        detector = FaceMeshDetector()
        t_end = time.time() + 20
        while time.time() < t_end:
            success, img = cap.read()

            try:
                img = detector.findFaceMesh(img)
            except:
                break

            lmList = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                print(lmList[1])
                cv2.circle(img, (lmList[1][1], lmList[1][2]),
                           5, (255, 0, 0), cv2.FILLED)

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
        cTime = 0
        pTime = 0
        detector = FaceMeshDetector()
        t_end = time.time() + 30
        while time.time() < t_end:
            success, img = cap.read()

            try:
                img = detector.findFaceMesh(img)
            except:
                break

            lmList = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                print(lmList[1])
                cv2.circle(img, (lmList[1][1], lmList[1][2]),
                           5, (255, 0, 0), cv2.FILLED)

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
