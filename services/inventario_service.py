import sqlite3

def conectar_db():
    return sqlite3.connect("inventario.db")

def crear_inventario_detalle(inventario_id, deposito_id, codigo_alfa, cantidad):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Validar que el inventario exista
    cursor.execute("SELECT id FROM inventario WHERE id = ?", (inventario_id,))
    if not cursor.fetchone():
        conn.close()
        return {"success": False, "data": "El inventario no existe."}
    
    # Validar que el depósito exista
    cursor.execute("SELECT id FROM deposito WHERE id = ?", (deposito_id,))
    if not cursor.fetchone():
        conn.close()
        return {"success": False, "data": "El depósito no existe."}
    
    # Validar que el producto exista
    cursor.execute("SELECT codigo_alfa FROM producto WHERE codigo_alfa = ?", (codigo_alfa,))
    if not cursor.fetchone():
        conn.close()
        return {"success": False, "data": "El producto no existe."}
    
    # Insertar el nuevo detalle de inventario
    cursor.execute("INSERT INTO inventario_detalle (inventario_id, deposito_id, codigo_alfa, cantidad) VALUES (?, ?, ?, ?)", 
                   (inventario_id, deposito_id, codigo_alfa, cantidad))
    conn.commit()
    conn.close()
    return {"success": True, "data": "Detalle de inventario creado exitosamente."}

def modificar_inventario_detalle(id, inventario_id=None, deposito_id=None, codigo_alfa=None, cantidad=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificar si el detalle de inventario existe
    cursor.execute("SELECT id FROM inventario_detalle WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return {"success": False, "data": "Detalle de inventario no encontrado."}
    
    # Validar inventario
    if inventario_id:
        cursor.execute("SELECT id FROM inventario WHERE id = ?", (inventario_id,))
        if not cursor.fetchone():
            conn.close()
            return {"success": False, "data": "El inventario no existe."}
    
    # Validar depósito
    if deposito_id:
        cursor.execute("SELECT id FROM deposito WHERE id = ?", (deposito_id,))
        if not cursor.fetchone():
            conn.close()
            return {"success": False, "data": "El depósito no existe."}
    
    # Validar producto
    if codigo_alfa:
        cursor.execute("SELECT codigo_alfa FROM producto WHERE codigo_alfa = ?", (codigo_alfa,))
        if not cursor.fetchone():
            conn.close()
            return {"success": False, "data": "El producto no existe."}
    
    # Actualizar el detalle de inventario
    cursor.execute("""
        UPDATE inventario_detalle
        SET inventario_id = COALESCE(?, inventario_id),
            deposito_id = COALESCE(?, deposito_id),
            codigo_alfa = COALESCE(?, codigo_alfa),
            cantidad = COALESCE(?, cantidad)
        WHERE id = ?
    """, (inventario_id, deposito_id, codigo_alfa, cantidad, id))
    conn.commit()
    conn.close()
    return {"success": True, "data": "Detalle de inventario actualizado."}

def eliminar_inventario_detalle(id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificar si el detalle de inventario existe
    cursor.execute("SELECT id FROM inventario_detalle WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return {"success": False, "data": "Detalle de inventario no encontrado."}
    
    # Eliminar detalle de inventario
    cursor.execute("DELETE FROM inventario_detalle WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"success": True, "data": "Detalle de inventario eliminado."}

def consultar_inventario_detalle(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, inventario_id, deposito_id, codigo_alfa, cantidad FROM inventario_detalle WHERE id = ?", (id,))
    detalle = cursor.fetchone()
    conn.close()
    return {"id": detalle[0], "inventario_id": detalle[1], "deposito_id": detalle[2], "codigo_alfa": detalle[3], "cantidad": detalle[4]} if detalle else {"error": "Detalle de inventario no encontrado."}

def listar_inventarios_detalle(filtro_inventario_id=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT id, inventario_id, deposito_id, codigo_alfa, cantidad FROM inventario_detalle"
    params = []
    
    if filtro_inventario_id is not None:
        query += " WHERE inventario_id = ?"
        params.append(filtro_inventario_id)
    
    cursor.execute(query, params)
    detalles = cursor.fetchall()
    conn.close()
    
    return [{"id": det[0], "inventario_id": det[1], "deposito_id": det[2], "codigo_alfa": det[3], "cantidad": det[4]} for det in detalles]


def crear_inventario(descripcion):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Insertar el nuevo inventario
    cursor.execute("INSERT INTO inventario (descripcion,estado) VALUES (?,?)", (descripcion,'En Proceso',))
    conn.commit()
    inventario_id = cursor.lastrowid
    conn.close()
    return {"success": True, "data": {"id": inventario_id, "descripcion": descripcion, "estado": 'En Proceso'}}

def modificar_inventario(id, fecha, estado=None, descripcion=None):
    if estado not in ['En Proceso', 'Finalizado']:
        return {"success": False, "data": "Estado inválido. Debe ser 'En Proceso' o 'Finalizado'."}
    
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificar si el inventario existe
    cursor.execute("SELECT id FROM inventario WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return {"success": False, "data": "Inventario no encontrado."}
    
    # Actualizar el inventario
    cursor.execute("""
        UPDATE inventario
        SET estado = COALESCE(?, estado),
            descripcion = COALESCE(?, descripcion),
            fecha = COALESCE(?, fecha)
        WHERE id = ?
    """, (estado, descripcion, fecha, id))
    conn.commit()
    conn.close()
    return {"success": True, "data": "Inventario actualizado."}

def eliminar_inventario(id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificar si el inventario existe
    cursor.execute("SELECT id FROM inventario WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return {"success": False, "data": "Inventario no encontrado."}
    
    # Eliminar inventario
    cursor.execute("DELETE FROM inventario WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"success": True, "data": "Inventario eliminado."}

def consultar_inventario(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, fecha, estado, descripcion FROM inventario WHERE id = ?", (id,))
    inventario = cursor.fetchone()
    conn.close()
    return {"id": inventario[0], "fecha": inventario[1], "estado": inventario[2], "descripcion": inventario[3]} if inventario else {"error": "Inventario no encontrado."}

def listar_inventarios():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, fecha, estado, descripcion FROM inventario")
    inventarios = cursor.fetchall()
    conn.close()
    
    return [{"id": inv[0], "fecha": inv[1], "estado": inv[2], "descripcion": inv[3]} for inv in inventarios]

