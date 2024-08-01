import os
import streamlit as st
from openai import OpenAI
import requests
import base64
from utils import get_image_description

# Función para mostrar el logo en la cabecera
def display_logo():
    logo_path = "logo-cass.svg"  # Asegúrate de que el archivo esté en el mismo directorio o ajusta la ruta
    with open(logo_path, "r") as f:
        svg_logo = f.read()
    st.markdown(f'<div style="display:flex; align-items:center;"><img src="data:image/svg+xml;base64,{base64.b64encode(svg_logo.encode()).decode()}" style="height: 50px; margin-right: 10px;"> <h1 style="display:inline;">Smart Vision per a la Interpretació de Receptes Mèdiques</h1></div>', unsafe_allow_html=True)

# Mostrar el logo en la cabecera
display_logo()

st.write("Puja una o diverses imatges de les teves receptes mèdiques perquè el sistema les analitzi i interpreti.")

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
        st.error(f"Error en la corrección del nombre del medicamento: {response.status_code}")
        return name

if api_key and tavily_api_key:
    # Inicializar el cliente de OpenAI
    client = OpenAI(api_key=api_key)

    # Prompt predefinido para la descripción de la imagen
    prompt = """
    Por favor, analiza la imagen de la receta médica y proporciona la siguiente información para cada medicamento listado:
    - Nombre del medicamento
    - Dosis del medicamento
    - Posología (indicaciones de uso)

    Si algún dato no está presente en la receta, indica "No especificado".
    """

    # Botón para subir imágenes
    uploaded_files = st.file_uploader("", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if uploaded_files:
        try:
            for uploaded_file in uploaded_files:
                # Mostrar la imagen subida
                st.image(uploaded_file, caption='Imagen subida.', use_column_width=True)
                st.write("Analizando...")

                # Obtener la descripción de la imagen
                try:
                    description = get_image_description(client, uploaded_file, prompt)
                    st.write("Descripción obtenida de la imagen:")
                    st.code(description)  # Mostrar la descripción obtenida para depuración
                except Exception as e:
                    st.error(f"Error al obtener la descripción de la imagen: {e}")
                    continue
                
                # Procesar la descripción para extraer la información de los medicamentos
                try:
                    description_lines = description.split('\n')
                    medications_info = []
                    medication = {}
                    for line in description_lines:
                        if "Nombre del medicamento:" in line:
                            if medication:
                                medications_info.append(medication)
                            medication = {"Nombre": line.split(":", 1)[1].strip()}
                        elif "Dosis del medicamento:" in line:
                            medication["Dosis"] = line.split(":", 1)[1].strip()
                        elif "Posología:" in line:
                            medication["Posología"] = line.split(":", 1)[1].strip()
                    if medication:
                        medications_info.append(medication)

                    # Verificar y corregir los nombres de los medicamentos
                    for med in medications_info:
                        medication_name = med.get("Nombre", "No especificado")
                        corrected_name = get_corrected_medication_name(medication_name)
                        if medication_name != corrected_name:
                            st.warning(f"Nombre del medicamento corregido: {corrected_name} (original: {medication_name})")
                        else:
                            st.success(f"Nombre del medicamento: {medication_name} (válido)")
                        st.write("Dosis del medicamento:", med.get("Dosis", "No especificado"))
                        st.write("Posología:", med.get("Posología", "No especificado"))
                
                except Exception as e:
                    st.error(f"Error al procesar la descripción de la imagen: {e}")

        except Exception as e:
            st.error(f"Error general: {e}")
else:
    st.error("Por favor, proporciona una clave de API válida de OpenAI y Tavily.")
