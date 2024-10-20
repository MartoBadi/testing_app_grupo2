import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
from PIL import Image

# Cargar el modelo TFLite
interpreter = tf.lite.Interpreter(model_path='modelNella.tflite')
interpreter.allocate_tensors()

repo_path = os.path.dirname(os.path.abspath(__file__))

# Obtener detalles de entrada y salida
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Definir nombres de clases
class_names = ['burj_khalifa', 'chichen_itza', 'christ the reedemer', 'eiffel_tower', 
               'great_wall_of_china', 'machu_pichu', 'pyramids_of_giza', 'roman_colosseum', 
               'statue_of_liberty', 'stonehenge', 'taj_mahal', 'venezuela_angel_falls']

# Definir umbral de confianza (por ejemplo, 80%)
confidence_threshold = 0.6050201058387756

# Preprocesar la imagen subida
def preprocess_image(image):
    size = (224, 224)  # Asegúrate de que este tamaño sea el correcto para tu modelo
    image = np.array(image)
    image = np.resize(image, (size[0], size[1], 3))  # Redimensionar la imagen
    img_array = image / 255.0  # Normalizar la imagen
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array.astype(np.float32) 
    return img_array

# Función para buscar la carpeta de la imagen
def find_image_folder(image_name, base_dir=repo_path):
    for root, dirs, files in os.walk(base_dir):
        if image_name in files:
            return os.path.basename(root)
    return "Unknown"

# Función para cargar y procesar imágenes desde un directorio
def load_and_process_images(image_directory):
    for root, dirs, files in os.walk(image_directory):
        for image_name in files:
            if image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, image_name)
                image = Image.open(image_path)
                st.image(image, caption=image_name)
                
                # Preprocesar la imagen
                img_array = preprocess_image(image)
                
                # Hacer predicciones
                interpreter.set_tensor(input_details[0]['index'], img_array)
                interpreter.invoke()
                predictions = interpreter.get_tensor(output_details[0]['index'])

                max_probabilidad = np.max(predictions)

                # Verificar si la probabilidad supera el umbral de confianza
                if max_probabilidad < confidence_threshold:
                    st.write(f"No se pudo clasificar la imagen. La probabilidad maxima fue de {max_probabilidad:.2f}")
                    predicted_class = " "
                else:
                    # Obtener la clase con mayor probabilidad
                    predicted_class = class_names[np.argmax(predictions)]
                    st.write(f"Prediction: {predicted_class} con una probabilidad de {max_probabilidad:.2f}")

                # Buscar la carpeta de la imagen
                real_class = find_image_folder(image_name, base_dir=repo_path)
                st.write(f"Real class: {real_class}")
                st.write(f"Prediction: {predicted_class}")

                # Inicializar el contador en session_state si no existe
                if 'correct_predictions' not in st.session_state:
                    st.session_state.correct_predictions = 0

                # Incrementar el contador si la clase real es igual a la clase predicha
                if real_class == predicted_class:
                    st.session_state.correct_predictions += 1

                # Mostrar el contador actualizado
                st.write(f"Correct Predictions: {st.session_state.correct_predictions}")

# Título de la aplicación
st.title("Clasificación de imágenes de maravillas del mundo")
st.write("Este sitio web fue creado para la materia Modelizado de Sistemas de IA de la Tecnicatura Superior en Ciencias de Datos e Inteligencia Artificial del IFTS 18. La idea es que subas una imagen de una de las maravillas del mundo y el modelo la clasificará.")

# Subir archivo
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

load_and_process_images(image_directory)

if uploaded_file is not None:
    # Leer la imagen usando Matplotlib
    image = mpimg.imread(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    
    # Preprocesar la imagen
    img_array = preprocess_image(image)
    print("Pruebas finalizadas")
    
    # Hacer predicciones
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])

    max_probabilidad = np.max(predictions)

    # Verificar si la probabilidad supera el umbral de confianza
    if max_probabilidad < confidence_threshold:
        st.write(f"No se pudo clasificar la imagen. La probabilidad maxima fue de {max_probabilidad:.2f}")
        predicted_class = " "
    else:
        # Obtener la clase con mayor probabilidad
        predicted_class = class_names[np.argmax(predictions)]
        st.write(f"Prediction: {predicted_class} con una probabilidad de {max_probabilidad:.2f}")

    image_name = uploaded_file.name
    
    # Buscar la carpeta de la imagen
    real_class = find_image_folder(image_name, base_dir=repo_path)
  
    st.write(f"Real class: {real_class}")
    st.write(f"Prediction: {predicted_class}")

    # Inicializar el contador en session_state si no existe
    if 'correct_predictions' not in st.session_state:
        st.session_state.correct_predictions = 0

    # Incrementar el contador si la clase real es igual a la clase predicha
    if real_class == predicted_class:
        st.session_state.correct_predictions += 1
    
    # Mostrar el contador actualizado
    st.write(f"Correct Predictions: {st.session_state.correct_predictions}")
