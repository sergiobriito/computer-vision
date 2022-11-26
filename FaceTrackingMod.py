import cv2
import mediapipe as mp
import time


class faceDetector():

    def __init__(self):
        self.mpFace = mp.solutions.face_detection
        self.face = self.mpFace.FaceDetection()
        self.mpDraw = mp.solutions.drawing_utils

    def findFaces(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.face.process(imgRGB)
        bboxs = []

        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                h, w, c = img.shape
                bbox = int(bboxC.xmin * w), int(bboxC.ymin * h), \
                    int(bboxC.width * w), int(bboxC.height * h)
                bboxs.append([id, bbox, detection.score])

                if draw:
                    img = self.fancyDraw(img, bbox)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20),
                                cv2.FONT_HERSHEY_PLAIN, 1,  (0, 255, 0), 2)

        return img, bboxs

    def fancyDraw(self, img, bbox, l=30, t=5, rt=1):
        x, y, h, w = bbox
        x1, y1 = x+w, y+h
        cv2.rectangle(img, bbox,  (0, 255, 0), rt)
        # Top Left x,y
        cv2.line(img, (x, y), (x+l, y),  (0, 255, 0), t)
        cv2.line(img, (x, y), (x, y+l),  (0, 255, 0), t)
        # Top Right x1,y
        cv2.line(img, (x1, y), (x1-l, y),  (0, 255, 0), t)
        cv2.line(img, (x1, y), (x1, y+l),  (0, 255, 0), t)
        # Bottom Left x,y1
        cv2.line(img, (x, y1), (x+l, y1),  (0, 255, 0), t)
        cv2.line(img, (x, y1), (x, y1-l),  (0, 255, 0), t)
        # Bottom Right x1,y1
        cv2.line(img, (x1, y1), (x1-l, y1),  (0, 255, 0), t)
        cv2.line(img, (x1, y1), (x1, y1-l),  (0, 255, 0), t)

        return img


def main():
    cap = cv2.VideoCapture(r"media\face.mp4")
    cTime = 0
    pTime = 0
    detector = faceDetector()

    while True:
        success, img = cap.read()

        try:
            img, bboxs = detector.findFaces(img)
        except:
            break

        print(bboxs)

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
    main()
