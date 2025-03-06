import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

st.title("Conversión de Texto a Audio")
image = Image.open('gato_raton.png')
st.image(image, width=350)
with st.sidebar:
    st.subheader("Escribe y/o selecciona texto para ser escuchado.")

try:
    os.mkdir("temp")
except:
    pass

st.subheader("Una pequeña Fábula.")
st.write('¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo. '  
         ' Corría y corría y por cierto que me alegraba ver esos muros, a diestra y siniestra, en la distancia. ' 
         ' Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está '  
         ' la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo el gato...y se lo comió. ' 
         '  '
         ' Franz Kafka.')

st.markdown(f"Quieres escucharlo?, copia el texto")
text = st.text_area("Ingrese El texto a escuchar.")

# Cambiar la selección del idioma a botones
st.subheader("Selecciona el lenguaje")

# Definir el comportamiento de los botones
col1, col2 = st.columns(2)

with col1:
    if st.button("Español"):
        lg = 'es'

with col2:
    if st.button("English"):
        lg = 'en'

def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)  # gTTS con idioma
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    audio_file_path = f"temp/{my_file_name}.mp3"
    tts.save(audio_file_path)
    return audio_file_path, text

# Al presionar el botón para convertir a audio
if st.button("Convertir a Audio"):
    if not text:
        st.warning("Por favor ingresa un texto.")
    else:
        # Generar el archivo de audio
        result_path, output_text = text_to_speech(text, lg)  
        
        # Reproductor de audio
        st.markdown("### Escucha tu audio:")
        audio_file = open(result_path, "rb")
        audio_bytes = audio_file.read()
        
        # Mostrar el reproductor de audio
        st.audio(audio_bytes, format="audio/mp3", start_time=0)

        # Descargar el archivo de audio
        with open(result_path, "rb") as f:
            data = f.read()

        def get_binary_file_downloader_html(bin_file, file_label='File'):
            bin_str = base64.b64encode(data).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
            return href
        st.markdown(get_binary_file_downloader_html(result_path, file_label="Audio File"), unsafe_allow_html=True)

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)


