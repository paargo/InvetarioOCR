#from database import get_db
from pydantic import BaseModel
from typing import Optional, List
from fastapi import HTTPException
import sqlite3
import csv
from io import StringIO
import pandas as pd

# Modelo de Producto con nuevos campos
class ProductoCreate(BaseModel):
    codigo_alfa: str
    codigo_barras: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    proveedor_codigo: Optional[str] = None
    proveedor_nombre: Optional[str] = None

class ProductoUpdate(BaseModel):
    codigo_barras: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    proveedor_codigo: Optional[str] = None
    proveedor_nombre: Optional[str] = None

def conectar_db():
    return sqlite3.connect("inventario.db")


# Crear un producto
def crear_producto(producto: ProductoCreate):
    conn = conectar_db()
    db = conn.cursor()
    try:
        # Verificar si el código_alfa ya existe
        db.execute("SELECT id FROM producto WHERE codigo_alfa = ?", (producto.codigo_alfa,))
        if db.fetchone():
            return {"success": False, "message": "El código Alfa ya existe."}

        # Insertar nuevo producto
        db.execute("""
            INSERT INTO producto (codigo_alfa, codigo_barras, descripcion, precio, proveedor_codigo, proveedor_nombre)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (producto.codigo_alfa, producto.codigo_barras, producto.descripcion, producto.precio, producto.proveedor_codigo, producto.proveedor_nombre))
        
        conn.commit()
        return {"success": True, "message": "Producto creado exitosamente"}
    
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error en la base de datos: {str(e)}"}
    
    finally:
        db.close()

def crear_productos_desde_csv(csv_content: str):
    conn = conectar_db()
    db = conn.cursor()
    productos_creados = []
    try:
        reader = csv.DictReader(StringIO(csv_content))
        for row in reader:
            producto = ProductoCreate(**row)
            # Verificar si el código_alfa ya existe
            db.execute("SELECT id FROM producto WHERE codigo_alfa = ?", (producto.codigo_alfa,))
            if db.fetchone():
                continue  # Saltar productos con código_alfa duplicado

            # Insertar nuevo producto
            db.execute("""
                INSERT INTO producto (codigo_alfa, codigo_barras, descripcion, precio, proveedor_codigo, proveedor_nombre)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (producto.codigo_alfa, producto.codigo_barras, producto.descripcion, producto.precio, producto.proveedor_codigo, producto.proveedor_nombre))
            
            productos_creados.append(producto.codigo_alfa)
        
        conn.commit()
        return {"success": True, "message": "Productos creados exitosamente", "data": productos_creados}
    
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error en la base de datos: {str(e)}"}
    
    finally:
        db.close()

def crear_productos_desde_xlsx(xlsx_content: bytes):
    conn = conectar_db()
    db = conn.cursor()
    productos_creados = []
    try:
        df = pd.read_excel(xlsx_content)
        for _, row in df.iterrows():
            producto = ProductoCreate(**row.to_dict())
            # Verificar si el código_alfa ya existe
            db.execute("SELECT id FROM producto WHERE codigo_alfa = ?", (producto.codigo_alfa,))
            if db.fetchone():
                continue  # Saltar productos con código_alfa duplicado

            # Insertar nuevo producto
            db.execute("""
                INSERT INTO producto (codigo_alfa, codigo_barras, descripcion, precio, proveedor_codigo, proveedor_nombre)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (producto.codigo_alfa, producto.codigo_barras, producto.descripcion, producto.precio, producto.proveedor_codigo, producto.proveedor_nombre))
            
            productos_creados.append(producto.codigo_alfa)
        
        conn.commit()
        return {"success": True, "message": "Productos creados exitosamente", "data": productos_creados}
    
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error en la base de datos: {str(e)}"}
    
    finally:
        db.close()

# Modificar un producto
def modificar_producto(codigo_alfa: str, producto: ProductoUpdate):
    conn = conectar_db()
    db = conn.cursor()
    try:
        # Verificar si el producto existe
        db.execute("SELECT id FROM producto WHERE codigo_alfa = ?", (codigo_alfa,))
        if not db.fetchone():
            return {"success": False, "message": "Producto no encontrado"}

        # Actualizar los campos
        db.execute("""
            UPDATE producto SET codigo_barras = ?, descripcion = ?, precio = ?, proveedor_codigo = ?, proveedor_nombre = ?
            WHERE codigo_alfa = ?
        """, (producto.codigo_barras, producto.descripcion, producto.precio, producto.proveedor_codigo, producto.proveedor_nombre, codigo_alfa))
        
        conn.commit()
        return {"success": True, "message": "Producto actualizado exitosamente"}
    
    except sqlite3.Error as e:
        return {"success": False, "message": f"Error en la base de datos: {str(e)}"}
    
    finally:
        db.close()

# Consultar producto por código Alfa
def consultar_producto(codigo_alfa: str):
    conn = conectar_db()
    db = conn.cursor()
    try:
        producto = db.execute("SELECT * FROM producto WHERE codigo_alfa = ?", (codigo_alfa,)).fetchone()
        if not producto:
            return None
        column_names = [description[0] for description in db.description]
        return dict(zip(column_names, producto))
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    
    finally:
        db.close()

# Listar productos con filtros opcionales
def listar_productos(filtros: dict = None):
    conn = conectar_db()
    db = conn.cursor()
    try:
        query = "SELECT * FROM producto"
        params = []
        if filtros:
            conditions = []
            for campo, valor in filtros.items():
                conditions.append(f"{campo} = ?")
                params.append(valor)
            query += " WHERE " + " AND ".join(conditions)

        productos = db.execute(query, params).fetchall()
        column_names = [description[0] for description in db.description]
        return [dict(zip(column_names, prod)) for prod in productos]
    
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Error en la base de datos: {str(e)}")
    
    finally:
        db.close()

def eliminar_producto(codigo_alfa: str):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificar si el depósito tiene productos asociados
    #cursor.execute("SELECT id FROM inventario_detalle WHERE deposito_id = ?", (id,))
    #if cursor.fetchone():
    #    conn.close()
    #    return {"success": False,"data":"No se puede eliminar un depósito que contiene productos."}
    
    # Eliminar producto
    cursor.execute("DELETE FROM producto WHERE codigo_alfa = ?", (codigo_alfa,))
    conn.commit()
    conn.close()
    return {"success": True,"data":"Producto eliminado."}