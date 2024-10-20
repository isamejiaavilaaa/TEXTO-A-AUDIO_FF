import os

# Instalación automática de dependencias
os.system('pip install streamlit gtts googletrans==4.0.0-rc1 pillow')

import streamlit as st
import time
import glob
from gtts import gTTS
from PIL import Image
import base64
from googletrans import Translator  # Traducción automática

# Configuración inicial
st.title("Conversión de Texto a Audio")
image = Image.open('el gato y el raton.jpg')
st.image(image, width=350)

with st.sidebar:
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

# Crear carpeta temporal para los archivos de audio
os.makedirs("temp", exist_ok=True)

st.subheader("Una pequeña Fábula.")
st.write(
    '¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. '
    'Al principio era tan grande que le tenía miedo. Corría y corría '
    'y por cierto que me alegraba ver esos muros, a diestra y siniestra, '
    'en la distancia. Pero esas paredes se estrechan tan rápido que me encuentro '
    'en el último cuarto y ahí en el rincón está la trampa sobre la cual debo pasar. '
    'Todo lo que debes hacer es cambiar de rumbo -dijo el gato... y se lo comió. '
    'Franz Kafka.'
)

st.markdown("¿Quieres escucharlo? Copia el texto:")
text = st.text_area("Ingrese el texto a escuchar.")

# Opciones del idioma con sus respectivos códigos
option_lang = st.selectbox(
    "Selecciona el lenguaje",
    ["Español", "English", "Deutsch", "한국어 (Coreano)", "Esperanto"]
)

# Diccionario para convertir la selección a códigos de idioma
lang_codes = {
    "Español": "es",
    "English": "en",
    "Deutsch": "de",
    "한국어 (Coreano)": "ko",
    "Esperanto": "eo"
}

# Inicializamos el traductor
translator = Translator()

# Función para traducir texto
def translate_text(text, target_lang):
    if target_lang != 'es':  # Si no es español, traducimos
        translated = translator.translate(text, dest=target_lang).text
        return translated
    return text  # Si es español, no se traduce

# Función para convertir texto a audio
def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    file_name = text[:20].strip().replace(" ", "_") + ".mp3"
    file_path = f"temp/{file_name}"
    tts.save(file_path)
    return file_path

# Convertimos la opción seleccionada a código de lenguaje
lang_code = lang_codes[option_lang]

# Botón para convertir texto a audio
if st.button("Convertir a Audio"):
    if text.strip():
        # Traducimos si es necesario
        translated_text = translate_text(text, lang_code)
        audio_path = text_to_speech(translated_text, lang_code)

        # Mostrar el audio en la app
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()
        st.markdown("## Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Enlace para descargar el archivo de audio
        def get_binary_file_downloader_html(file_path, file_label='Audio File'):
            with open(file_path, "rb") as f:
                data = f.read()
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(file_path)}">Download {file_label}</a>'
            return href

        st.markdown(get_binary_file_downloader_html(audio_path), unsafe_allow_html=True)
    else:
        st.warning("Por favor, ingrese un texto para convertir a audio.")

# Función para eliminar archivos antiguos
def remove_files(days_old):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    n_seconds = days_old * 86400  # Días a segundos
    for f in mp3_files:
        if os.stat(f).st_mtime < now - n_seconds:
            os.remove(f)
            print(f"Deleted {f}")

# Eliminar archivos antiguos cada 7 días
remove_files(7)

