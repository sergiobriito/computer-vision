import streamlit as st
from PIL import Image
import mediapipe as mp
import cv2
import streamlit.components.v1 as components
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
from datetime import datetime
import av
import subprocess
import os
import sys

# --Funcionalidades--


class FaceMeshDetector:
    def __init__(self):
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=2)
        self.mpDraw = mp.solutions.drawing_utils
        self.drawSpec = self.mpDraw.DrawingSpec(
            thickness=1, circle_radius=1, color=(0, 255, 0))

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(img)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                self.mpDraw.draw_landmarks(
                    img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS, self.drawSpec, self.drawSpec)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


class HandDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, handLms, self.mpHands.HAND_CONNECTIONS)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


class FingerCounter:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        lmList = []
        fingers = []

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, handLms, self.mpHands.HAND_CONNECTIONS)

        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])

        if len(lmList) != 0:
            # First finger
            if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 fingers
            for id in range(1, 5):
                if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id]-1][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        # Total fingers
        totalFingers = fingers.count(1)
        cv2.putText(img, str(int(totalFingers)), (450, 70),
                    cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


class TakePictureController:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img.flags.writeable = False
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img)
        img.flags.writeable = True
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        lmList = []
        fingers = []

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(
                    img, handLms, self.mpHands.HAND_CONNECTIONS)

        if results.multi_hand_landmarks:
            myHand = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                lmList.append([id, cx, cy])

        if len(lmList) != 0:

            # First finger
            if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 fingers
            for id in range(1, 5):
                if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id]-1][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            if fingers == [0, 1, 1, 0, 0]:
                img_name = "./media/imagemCAM.png"
                cv2.imwrite(img_name, img)
                cv2.putText(img, "Imagem salva", (250, 70),cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


# ---Navegador---
st.set_page_config(page_icon="💻", page_title="Visão Computacional")
st.title("💻 Visão Computacional")

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]}]}
)

funcionalidaEscolhida = st.radio("Selecione uma opção:", ("Sobre", "Reconhecimento facial",
                                                          "Reconhecimento das mãos", "Aplicações"))

if funcionalidaEscolhida == "Sobre":
    st.info("Projeto de visão computacional em Python, utilizando OpenCV e MediaPipe")
    imageCap = Image.open("./media/Intro.JPG")
    st.image(imageCap)

if funcionalidaEscolhida == "Reconhecimento facial":
    st.info("Autorizar o uso da câmera")
    webrtc_ctx = webrtc_streamer(
        key="Video",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=FaceMeshDetector,
        async_processing=True,
    )

if funcionalidaEscolhida == "Reconhecimento das mãos":
    st.info("Autorizar o uso da câmera")
    webrtc_ctx = webrtc_streamer(
        key="Video",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIGURATION,
        media_stream_constraints={"video": True, "audio": False},
        video_processor_factory=HandDetector,
        async_processing=True,
    )

if funcionalidaEscolhida == "Aplicações":
    subFuncionalidaEscolhida = st.radio(
        "Selecione uma opção:", ("Sistema para tirar fotos", "Sistema de contagem"), horizontal=True)
    if subFuncionalidaEscolhida == "Sistema para tirar fotos":
        st.info("Autorizar o uso da câmera")
        st.info("Realizar o gesto ✌️ para capturar a foto")
        webrtc_ctx = webrtc_streamer(
            key="Video",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={"video": True, "audio": False},
            video_processor_factory=TakePictureController,
            async_processing=True,
        )

        if os.path.exists("./media/imagemCAM.png"):
            with open("./media/imagemCAM.png", "rb") as arquivoFinal:
                downloadButton = st.download_button(label="📥 Baixar imagem",
                                   data=arquivoFinal, file_name="imagem.png")
            if downloadButton:
                os.remove("./media/imagemCAM.png")


    if subFuncionalidaEscolhida == "Sistema de contagem":
        st.info("Autorizar o uso da câmera")
        st.info("Realizar os gestos abaixo para visualizar a contagem")
        imageCap = Image.open("./media/fingers.jpg")
        st.image(imageCap)
        webrtc_ctx = webrtc_streamer(
            key="Video",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={"video": True, "audio": False},
            video_processor_factory=FingerCounter,
            async_processing=True,
        )

style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
.css-12oz5g7 {padding: 2rem 1rem;}
.css-14xtw13 {visibility: hidden;}
span.css-9ycgxx.exg6vvm12 {
visibility: hidden;
white-space: nowrap;
}
section.css-po3vlj.exg6vvm15 button{visibility:hidden;}
#Linkedin {margin-top: 130px;}
#desenvolvidoPor {color: black;}
#nome {color: black;}
</style>
<div id="Linkedin" class="badge-base LI-profile-badge" data-locale="pt_BR" data-size="medium" data-theme="light" data-type="VERTICAL" data-vanity="sérgio--brito" data-version="v1">
<a href="https://br.linkedin.com/in/s%C3%A9rgio--brito?trk=profile-badge"><img src="https://brand.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" alt="Linkedin" style="width:42px;height:42px;"></a>
<a id="desenvolvidoPor">Desenvolvido por </a>
<a id="nome" class="badge-base__link LI-simple-link" href="https://br.linkedin.com/in/s%C3%A9rgio--brito?trk=profile-badge">Sérgio Brito</a>
</div>
"""

st.markdown(style, unsafe_allow_html=True)
