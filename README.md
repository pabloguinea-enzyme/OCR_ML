# Visión Inteligente para la Interpretación de Recetas Médicas

Este proyecto es una aplicación web desarrollada con Streamlit para analizar y describir imágenes de recetas médicas, proporcionando una interpretación clara y estructurada de los medicamentos, dosis y posología presentes en las recetas.

## Features

- Subir una o varias imágenes (jpg, jpeg, png).
- Obtener una descripción detallada de los medicamentos, dosis y posología.
- Verificación y corrección de nombres de medicamentos utilizando la API de Tavily.
- Interfaz amigable e intuitiva

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/pabloguinea-enzyme/OCR_ML.git
    cd OCR-ML
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the app:
    ```bash
    streamlit run app.py
    ```

4. Open your browser and go to `http://localhost:8501` to use the app OR go to https://cass-demo.streamlit.app/

## Usage

- Enter your OpenAI API key.
- Enter a prompt for image description.
- Upload an image and get the description.

## Contributing

Feel free to open issues or submit pull requests for any improvements or bug fixes.

## License

This project is licensed under the MIT License.
