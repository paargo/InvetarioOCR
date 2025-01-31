import streamlit as st
import requests

# Configuración de la API
API_URL = "http://127.0.0.1:8000"

def listar_depositos():
    response = requests.get(f"{API_URL}/depositos/")
    return response.json().get("data", [])

def crear_deposito(nombre, padre_id, almacena):
    response = requests.post(f"{API_URL}/depositos/", json={"nombre": nombre, "padre_id": padre_id, "almacena": almacena})
    return response.json()

def modificar_deposito(deposito_id, nombre, padre_id, almacena):
    response = requests.put(f"{API_URL}/depositos/{deposito_id}", json={"nombre": nombre, "padre_id": padre_id, "almacena": almacena})
    return response.json()

def eliminar_deposito(deposito_id):
    response = requests.delete(f"{API_URL}/depositos/{deposito_id}")
    return response.json()

def listar_productos():
    response = requests.get(f"{API_URL}/productos/")
    return response.json().get("data", [])

def crear_producto(codigo_alfa, descripcion, precio, proveedor_codigo, proveedor_nombre):
    response = requests.post(f"{API_URL}/productos/", json={"codigo_alfa": codigo_alfa, "descripcion": descripcion, "precio": precio, "proveedor_codigo": proveedor_codigo, "proveedor_nombre": proveedor_nombre})
    return response.json()

def modificar_producto(codigo_alfa, descripcion, precio, proveedor_codigo, proveedor_nombre):
    response = requests.put(f"{API_URL}/productos/{codigo_alfa}", json={"descripcion": descripcion, "precio": precio, "proveedor_codigo": proveedor_codigo, "proveedor_nombre": proveedor_nombre})
    return response.json()

def eliminar_producto(codigo_alfa):
    response = requests.delete(f"{API_URL}/productos/{codigo_alfa}")
    return response.json()

def listar_inventarios():
    response = requests.get(f"{API_URL}/inventario/")
    return response.json().get("data", [])

def crear_inventario(descripcion):
    response = requests.post(f"{API_URL}/inventario/", json={"inventario_descripcion": descripcion})
    return response.json()

def modificar_inventario(inventario_id, descripcion):
    response = requests.put(f"{API_URL}/inventario/{inventario_id}", json={"descripcion": descripcion})
    return response.json()

def eliminar_inventario(inventario_id):
    response = requests.delete(f"{API_URL}/inventario/{inventario_id}")
    return response.json()

def listar_inventario_detalle():
    response = requests.get(f"{API_URL}/inventario_detalle/")
    return response.json().get("data", [])

def crear_inventario_detalle(inventario_id, deposito_id, codigo_alfa, cantidad):
    response = requests.post(f"{API_URL}/inventario_detalle/", json={"inventario_id": inventario_id, "deposito_id": deposito_id, "codigo_alfa": codigo_alfa, "cantidad": cantidad})
    return response.json()

def modificar_inventario_detalle(detalle_id, cantidad):
    response = requests.put(f"{API_URL}/inventario_detalle/{detalle_id}", json={"cantidad": cantidad})
    return response.json()

def eliminar_inventario_detalle(detalle_id):
    response = requests.delete(f"{API_URL}/inventario_detalle/{detalle_id}")
    return response.json()

# Interfaz Streamlit
st.title("Gestión de Inventarios")

menu = st.sidebar.selectbox("Seleccionar módulo", ["Depósitos", "Productos", "Inventarios", "Detalle de Inventarios"])

if menu == "Inventarios":
    st.subheader("Gestión de Inventarios")
    inventarios = listar_inventarios()
    st.table(inventarios)
    
    with st.form("Modificar Inventario"):
        inventario_id = st.number_input("ID del Inventario a modificar", min_value=1, format="%d")
        descripcion = st.text_input("Nueva descripción")
        submit = st.form_submit_button("Modificar")
        
        if submit:
            resultado = modificar_inventario(inventario_id, descripcion)
            st.write(resultado)
    
    with st.form("Eliminar Inventario"):
        inventario_id = st.number_input("ID del Inventario a eliminar", min_value=1, format="%d")
        submit = st.form_submit_button("Eliminar")
        
        if submit:
            resultado = eliminar_inventario(inventario_id)
            st.write(resultado)
    
elif menu == "Detalle de Inventarios":
    st.subheader("Gestión de Detalle de Inventarios")
    inventario_detalle = listar_inventario_detalle()
    st.table(inventario_detalle)
    
    with st.form("Crear Detalle de Inventario"):
        inventarios = listar_inventarios()
        inventario_id = st.selectbox("ID del Inventario", [inv['id'] for inv in inventarios])
        
        depositos = listar_depositos()
        deposito_id = st.selectbox("ID del Depósito", [dep['id'] for dep in depositos])
        
        productos = listar_productos()
        codigo_alfa = st.selectbox("Código Alfa del Producto", [prod['codigo_alfa'] for prod in productos])
        
        cantidad = st.number_input("Cantidad", min_value=1, format="%d")
        submit = st.form_submit_button("Crear")
        
        if submit:
            resultado = crear_inventario_detalle(inventario_id, deposito_id, codigo_alfa, cantidad)
            st.write(resultado)


    with st.form("Modificar Detalle de Inventario"):
        detalle_id = st.number_input("ID del Detalle de Inventario a modificar", min_value=1, format="%d")
        cantidad = st.number_input("Nueva Cantidad", min_value=1, format="%d")
        submit = st.form_submit_button("Modificar")
        
        if submit:
            resultado = modificar_inventario_detalle(detalle_id, cantidad)
            st.write(resultado)
    
    with st.form("Eliminar Detalle de Inventario"):
        detalle_id = st.number_input("ID del Detalle de Inventario a eliminar", min_value=1, format="%d")
        submit = st.form_submit_button("Eliminar")
        
        if submit:
            resultado = eliminar_inventario_detalle(detalle_id)
            st.write(resultado)


elif menu == "Depósitos":
    st.subheader("Gestión de Depósitos")
    depositos = listar_depositos()
    st.table(depositos)
    
    with st.form("Crear Depósito"):
        nombre = st.text_input("Nombre del depósito")
        padre_id = st.number_input("ID del depósito padre", min_value=0, format="%d")
        almacena = st.checkbox("¿Almacena productos?")
        submit = st.form_submit_button("Crear")
        
        if submit:
            resultado = crear_deposito(nombre, padre_id, almacena)
            st.write(resultado)

elif menu == "Productos":
    st.subheader("Gestión de Productos")
    productos = listar_productos()
    st.table(productos)
    
    with st.form("Crear Producto"):
        codigo_alfa = st.text_input("Código Alfa")
        descripcion = st.text_input("Descripción")
        precio = st.number_input("Precio", min_value=0.0, format="%.2f")
        proveedor_codigo = st.text_input("Código del Proveedor")
        proveedor_nombre = st.text_input("Nombre del Proveedor")
        submit = st.form_submit_button("Crear")
        
        if submit:
            resultado = crear_producto(codigo_alfa, descripcion, precio, proveedor_codigo, proveedor_nombre)
            st.write(resultado)