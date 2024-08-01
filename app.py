import os
import streamlit as st
from openai import OpenAI
import base64
from utils import get_image_description

# Configuración de la app de Streamlit
st.title("Visión Inteligente para la Interpretación de Recetas Médicas")
st.write("Sube una o varias imágenes de tus recetas médicas y nuestro sistema las interpretará y describirá para ti.")

# Obtener la clave de la API de OpenAI
api_key = st.secrets.get("openai_api_key")
if not api_key:
    api_key = os.environ.get("OPENAI_API_KEY", "")

if api_key:
    # Inicializar el cliente de OpenAI
    client = OpenAI(api_key=api_key)

    # Prompt predefinido para la descripción de la imagen
    prompt = """
    Por favor, analiza la imagen de la receta médica y proporciona la siguiente información de manera clara y estructurada:
    1. Nombre del medicamento:
    2. Dosis del medicamento:
    3. Fecha de prescripción:
    
    Si algún dato no está presente en la receta, indica "No especificado".
    """

    # Botón para subir imágenes
    uploaded_files = st.file_uploader("Elige una o más imágenes...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        try:
            for uploaded_file in uploaded_files:
                # Mostrar la imagen subida
                st.image(uploaded_file, caption='Imagen subida.', use_column_width=True)
                st.write("Analizando...")

                # Obtener la descripción de la imagen
                description = get_image_description(client, uploaded_file, prompt)
                st.write(description.strip())
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.error("Por favor, proporciona una clave de API válida de OpenAI.")
