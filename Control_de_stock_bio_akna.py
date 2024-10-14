import streamlit as st
import json
import os

# Path del archivo JSON
file_path = 'stock.json'

# Cargar productos desde el archivo JSON
def cargar_productos():
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    else:
        return [
            {"nombre": "Chips de chocolate", "precio": "$1.800 por 100 gramos", "categoria": "Producto a un precio por kilo", "ubicacion": "Heladera", "stock en venta": 1, "stock en despensa": 0},
            {"nombre": "Jugo de manzana roja Pura Frutta 1 litro", "precio": "$3.500", "ubicacion": "Heladera", "stock en venta": 2, "stock en despensa": 0},
            {"nombre": "Jugo de sabor multifruta (manzana, pera, banana y naranja) Pura Frutta 1 litro", "precio": "$3.500", "ubicacion": "Heladera", "stock en venta": 2, "stock en despensa": 0},
            {"nombre": "Jugo de manzana y frutilla Pura Frutta 1 litro", "precio": "$3.700", "ubicacion": "Heladera", "stock en venta": 2, "stock en despensa": 0},
            {"nombre": "Kombucha Bravia sabor superberry (con frutos rojos) 473ml", "precio": "$3.100", "ubicacion": "Heladera", "stock en venta": 2, "stock en despensa": 0}
        ]

# Guardar productos en el archivo JSON
def guardar_productos(productos):
    with open(file_path, 'w') as file:
        json.dump(productos, file, indent=4)

# Cargar productos
productos = cargar_productos()

# Función de búsqueda
def buscar_producto(nombre_producto):
    resultados = [producto for producto in productos if nombre_producto.lower() in producto['nombre'].lower()]
    return resultados

# Función para sumar stock en venta
def sumar_stock_venta(producto, cantidad):
    producto["stock en venta"] += cantidad
    guardar_productos(productos)  # Guardar cambios

# Función para sumar stock en despensa
def sumar_stock_despensa(producto, cantidad):
    producto["stock en despensa"] += cantidad
    guardar_productos(productos)  # Guardar cambios

# Interfaz de usuario con Streamlit
st.title('Buscador de Productos')
nombre_a_buscar = st.text_input('Buscar producto por nombre:')

if nombre_a_buscar:
    resultados = buscar_producto(nombre_a_buscar)
    if resultados:
        st.write(f"Productos encontrados ({len(resultados)}):")
        for producto in resultados:
            st.write(f"Nombre: {producto['nombre']}, Precio: {producto['precio']}, Ubicación: {producto['ubicacion']}, Stock en venta: {producto['stock en venta']}, Stock en despensa: {producto['stock en despensa']}")
            if st.button(f"Sumar stock en venta a {producto['nombre']}"):
                sumar_stock_venta(producto, 1)
                st.write(f"Nuevo stock en venta: {producto['stock en venta']}")
            if st.button(f"Sumar stock en despensa a {producto['nombre']}"):
                sumar_stock_despensa(producto, 1)
                st.write(f"Nuevo stock en despensa: {producto['stock en despensa']}")
    else:
        st.write("No se encontraron productos con ese nombre.")