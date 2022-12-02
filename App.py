import streamlit as st
from PIL import Image
import mediapipe as mp
import cv2
import streamlit.components.v1 as components
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
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
        st.info("Realizar o gesto abaixo para capturar a foto")
        imageCap = Image.open("./media/fingers/2.jpg")
        st.image(imageCap)
        os.system("TakePictureController.py")
        with open("./media/pictures/imagem.png", "rb") as arquivoFinal:
            st.download_button(label="📥 Baixar imagem", data=arquivoFinal, file_name="imagem.png")
        os.remove("./media/pictures/imagem.png")
    if subFuncionalidaEscolhida == "Sistema de contagem (Via câmera)":
        imageCap = Image.open("./media/fingers.JPG")
        st.info("Realizar os gestos abaixo para visualizar a contagem")
        st.image(imageCap)
        botaoExecutar = st.button("Executar")
        if botaoExecutar:
            with st.spinner('Processando...'):
                os.system("FingerCounter.py")

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
