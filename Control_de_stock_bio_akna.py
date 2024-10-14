import streamlit as st

# Definición de productos como diccionarios
productos = [
    {"nombre": "Chips de chocolate", "precio": "$1.800 por 100 gramos", "categoria": "Producto a un precio por kilo", "ubicacion": "Heladera", "stock en venta": 1, "stock en despensa: 0},
    {"nombre": "Jugo de manzana roja Pura Frutta 1 litro", "precio": "$3.500", "ubicacion": "Heladera", "stock en venta": 2, "stock en despensa: 0},
    {"nombre": "Jugo de sabor multifruta (manzana, pera, banana y naranja) Pura Frutta 1 litro", "precio": "$3.500", "ubicacion": "Heladera", "stock en venta": 2, "stock en despensa": 0},
{"nombre": "Jugo de manzana y frutilla Pura Frutta 1 litro"  ,"precio": "$3.700" "  ,"ubicacion": "Heladera", "stock en venta": 2, "stock en despensa" 0    }
{"nombre": "Kombucha Bravia sabor superberry (con frutos rojos) 473ml"  ,"precio": "$3.100"  ,"ubicacion":  "Heladera", "stock en venta": 2, "stock en despensa": 0  }
]

# Función de búsqueda
def buscar_producto(nombre_producto):
    resultados = [producto for producto in productos if nombre_producto.lower() in producto['nombre'].lower()]
    return resultados

# Interfaz de usuario con Streamlit
st.title('Buscador de Productos')
nombre_a_buscar = st.text_input('Buscar producto por nombre:')

if nombre_a_buscar:
    resultados = buscar_producto(nombre_a_buscar)
    if resultados:
        st.write(f"Productos encontrados ({len(resultados)}):")
        for producto in resultados:
            st.write(f"Nombre: {producto['nombre']}, Precio: {producto['precio']}, Ubicación: {producto['ubicacion']}")
    else:
        st.write("No se encontraron productos con ese nombre.")
