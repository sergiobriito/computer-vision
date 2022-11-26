import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
import FaceMeshTrackingMod
import HandTrackingMod
import PoseTrackingMod
import os

path = os.path.dirname(__file__)

# ---Navegador---
st.set_page_config(page_icon="💻", page_title="Visão Computacional")
st.title("💻 Visão Computacional")

funcionalidaEscolhida = st.radio("Selecione uma opção:", ("Sobre", "Reconhecimento facial", "Reconhecimento corporal",
                                 "Reconhecimento das mãos", "Aplicações"))

if funcionalidaEscolhida == "Sobre":
    st.info("Projeto de soluções de visão computacional em Python, utilizando OpenCV e MediaPipe")

if funcionalidaEscolhida == "Reconhecimento facial":
    subFuncionalidaEscolhida = st.radio(
        "Selecione uma opção:", ("Exemplo", "Ativar câmera"), horizontal=True)
    if subFuncionalidaEscolhida == "Exemplo":
        botaoExecutar = st.button("Executar")
        if botaoExecutar:
            with st.spinner('Processando...'):
                FaceMeshTrackingMod.main(1)
    if subFuncionalidaEscolhida == "Ativar câmera":
        botaoExecutar = st.button("Executar")
        if botaoExecutar:
            with st.spinner('Processando...'):
                FaceMeshTrackingMod.main(2)


if funcionalidaEscolhida == "Reconhecimento corporal":
    subFuncionalidaEscolhida = st.radio(
        "Selecione uma opção:", ("Exemplo", "Ativar câmera"), horizontal=True)
    if subFuncionalidaEscolhida == "Exemplo":
        botaoExecutar = st.button("Executar")
        if botaoExecutar:
            with st.spinner('Processando...'):
                PoseTrackingMod.main(1)
    if subFuncionalidaEscolhida == "Ativar câmera":
        botaoExecutar = st.button("Executar")
        if botaoExecutar:
            with st.spinner('Processando...'):
                PoseTrackingMod.main(2)


if funcionalidaEscolhida == "Reconhecimento das mãos":
    subFuncionalidaEscolhida = st.radio(
        "Selecione uma opção:", ("Exemplo", "Ativar câmera"), horizontal=True)
    if subFuncionalidaEscolhida == "Exemplo":
        botaoExecutar = st.button("Executar")
        if botaoExecutar:
            with st.spinner('Processando...'):
                HandTrackingMod.main(1)
    if subFuncionalidaEscolhida == "Ativar câmera":
        botaoExecutar = st.button("Executar")
        if botaoExecutar:
            with st.spinner('Processando...'):
                HandTrackingMod.main(2)


if funcionalidaEscolhida == "Aplicações":
    subFuncionalidaEscolhida = st.radio(
        "Selecione uma opção:", ("Sistema para tirar fotos (Via câmera)", "Sistema de contagem (Via câmera)"), horizontal=True)
    if subFuncionalidaEscolhida == "Sistema para tirar fotos (Via câmera)":
        imageCap = Image.open("./media/fingers/2.jpg")
        st.info("Realizar o gesto abaixo para capturar a foto")
        st.image(imageCap)
        botaoExecutar = st.button("Executar")
        if botaoExecutar:
            with st.spinner('Processando...'):
                os.system("TakePictureController.py")
                with open("./media/pictures/imagem.png", "rb") as arquivoFinal:
                    st.download_button(
                        label="📥 Baixar imagem", data=arquivoFinal, file_name="imagem.png")
                os.remove(
                    "./media/pictures/imagem.png")
    if subFuncionalidaEscolhida == "Sistema de contagem (Via câmera)":
        imageCap = Image.open("./media/fingers.JGP")
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
#Linkedin {margin-top: 190px;}
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
