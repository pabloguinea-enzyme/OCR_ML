import os
import streamlit as st
from openai import OpenAI
import requests
from utils import get_image_description

# Función para mostrar el logo en la cabecera
def display_logo():
    logo_path = "logo-cass.svg"  # Asegúrate de que el archivo esté en el mismo directorio o ajusta la ruta
    with open(logo_path, "r") as f:
        svg_logo = f.read()
    st.markdown(f'<div style="display:flex; align-items:center;"><img src="data:image/svg+xml;base64,{base64.b64encode(svg_logo.encode()).decode()}" style="height: 50px; margin-right: 10px;"> <h1 style="display:inline;">Visión Inteligente para la Interpretación de Recetas Médicas</h1></div>', unsafe_allow_html=True)

# Mostrar el logo en la cabecera
display_logo()

st.write("Sube una o varias imágenes de tus recetas médicas y nuestro sistema las interpretará y describirá para ti.")

# Obtener la clave de la API de OpenAI
api_key = st.secrets.get("openai_api_key")
tavily_api_key = st.secrets.get("tavily_api_key")  # Añade tu clave de API de Tavily a tus secretos de Streamlit

if not api_key:
    api_key = os.environ.get("OPENAI_API_KEY", "")
if not tavily_api_key:
    tavily_api_key = os.environ.get("TAVILY_API_KEY", "")

def get_corrected_medication_name(name):
    url = f"https://api.tavily.com/medication-correction"
    headers = {
        "Authorization": f"Bearer {tavily_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json={"name": name}, headers=headers)
    if response.status_code == 200:
        return response.json().get("corrected_name", name)
    else:
        return name

if api_key and tavily_api_key:
    # Inicializar el cliente de OpenAI
    client = OpenAI(api_key=api_key)

    # Prompt predefinido para la descripción de la imagen
    prompt = """
    Por favor, proporciona solo la siguiente información de manera clara y estructurada:
    Nombre del medicamento:
    Dosis del medicamento:
    Fecha de prescripción:
    
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
                
                # Procesar la descripción para extraer el nombre del medicamento
                description_lines = description.split('\n')
                medication_info = {line.split(':')[0].strip(): line.split(':')[1].strip() for line in description_lines if ':' in line}
                
                # Verificar y corregir el nombre del medicamento
                medication_name = medication_info.get("Nombre del medicamento", "No especificado")
                corrected_name = get_corrected_medication_name(medication_name)
                if medication_name != corrected_name:
                    st.warning(f"Nombre del medicamento corregido: {corrected_name} (original: {medication_name})")
                else:
                    st.success(f"Nombre del medicamento: {medication_name} (válido)")

                # Mostrar la información restante
                st.write("Dosis del medicamento:", medication_info.get("Dosis del medicamento", "No especificado"))
                st.write("Fecha de prescripción:", medication_info.get("Fecha de prescripción", "No especificado"))
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.error("Por favor, proporciona una clave de API válida de OpenAI y Tavily.")
