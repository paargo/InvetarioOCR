import streamlit as st
import requests
from PIL import Image
import io

# URL de tu servicio Flask
FLASK_URL = "http://127.0.0.1:5000/extract"  # Asegúrate de que Flask esté corriendo en este puerto

def upload_image(image):
    """Función que hace la solicitud POST al backend Flask"""
    # Convertir la imagen a bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Hacer la solicitud POST al servicio Flask
    files = {'image': img_bytes}
    response = requests.post(FLASK_URL, files=files)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Hubo un problema con la extracción del código."}

# Título de la app
st.title("Extractor de Código de Etiqueta")

# Subir la imagen
uploaded_file = st.file_uploader("Sube una imagen con la etiqueta", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Mostrar la imagen
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagen subida", use_column_width=True)

    # Botón para procesar la imagen
    if st.button('Extraer código'):
        # Llamar al servicio Flask
        result = upload_image(image)

        # Mostrar los resultados
        if "code" in result:
            st.subheader(f"Código extraído: {result['code']}")
        else:
            st.subheader(f"Error: {result['error']}")
            st.write(f"Texto detectado: {result.get('text_detected', 'N/A')}")
