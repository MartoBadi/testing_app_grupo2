import streamlit as st
import tensorflow as tf
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os
from PIL import Image

# Cargar el modelo TFLite
interpreter = tf.lite.Interpreter(model_path='model.tflite')
interpreter.allocate_tensors()

# Obtener detalles de entrada y salida
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Definir nombres de clases
class_names = ['burj_khalifa', 'chichen_itza', 'christ the reedemer', 'eiffel_tower', 'great_wall_of_china', 'machu_pichu', 'pyramids_of_giza', 'roman_colosseum', 'statue_of_liberty', 'stonehenge', 'taj_mahal', 'venezuela_angel_falls']

# Preprocesar la imagen subida
def preprocess_image(image):
    # Redimensionar la imagen al tamaño esperado por el modelo
    image = Image.fromarray(image).resize((150, 150))
    
    # Convertir la imagen a un array de numpy
    image = np.array(image)
    
    # Normalizar la imagen
    img_array = image / 255.0
    
    # Expandir las dimensiones para que coincida con el formato esperado por el modelo
    img_array = np.expand_dims(img_array, axis=0)
    
    # Asegurarse de que la imagen sea de tipo FLOAT32
    img_array = img_array.astype(np.float32)
    
    return img_array

st.title("Clasificación de imágenes de maravillas del mundo")
st.write("Este sitio web fue creado para la materia Modelizado de Sistemas de IA de la Tecnicatura Superior en Ciencias de Datos e Inteligencia Artificial del IFTS 18. La idea es que subas una imagen de uno de las siguientes maravillas del mundo: burj_khalifa, chichen_itza, christ the reedemer, eiffel_tower, great_wall_of_china, machu_pichu, pyramids_of_giza, roman_colosseum, statue_of_liberty, stonehenge, taj_mahal, venezuela_angel_falls y el modelo te dirá qué maravilla aparece en la imagen. ¡Diviértete!")

# Subir archivo
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Leer la imagen usando Matplotlib
    image = mpimg.imread(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Classifying...")
    
    # Preprocesar la imagen
    img_array = preprocess_image(image)
    
    # Hacer predicciones
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])
    
    # Obtener la clase con mayor probabilidad
    predicted_class = class_names[np.argmax(predictions)]
    
    # Obtener la clase real (nombre de la carpeta)
    real_class = os.path.basename(os.path.dirname(uploaded_file.name))
    
    st.write(f"Real class: {real_class}")
    st.write(f"Predicted class: {predicted_class}")
