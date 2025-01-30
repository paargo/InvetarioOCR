import sqlite3

def conectar_db():
    return sqlite3.connect("inventario.db")

def crear_deposito(nombre, padre_id, almacena):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificar unicidad del nombre
    cursor.execute("SELECT id FROM deposito WHERE nombre = ?", (nombre,))
    if cursor.fetchone():
        conn.close()
        return {"success": False,"data": "El nombre del depósito ya existe."}
    
    # Validar que el padre exista si se proporciona
    if padre_id:
        cursor.execute("SELECT id FROM deposito WHERE id = ?", (padre_id,))
        if not cursor.fetchone():
            conn.close()
            return {"success": False,"data": "El depósito padre no existe."}
    
    # Insertar el nuevo depósito
    cursor.execute("INSERT INTO deposito (nombre, padre_id, almacena) VALUES (?, ?, ?)", (nombre, padre_id, almacena))
    conn.commit()
    conn.close()
    return {"success": True,"data": "Depósito creado exitosamente."}

def modificar_deposito(id, nombre=None, padre_id=None, almacena=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificar si el depósito existe
    cursor.execute("SELECT id FROM deposito WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return {"success": False,"data":"Depósito no encontrado."}
    
    # Validar nombre único
    if nombre:
        cursor.execute("SELECT id FROM deposito WHERE nombre = ? AND id != ?", (nombre, id))
        if cursor.fetchone():
            conn.close()
            return {"success": False,"data":"El nombre del depósito ya está en uso."}
    
    # Validar padre
    if padre_id:
        cursor.execute("SELECT id FROM deposito WHERE id = ?", (padre_id,))
        if not cursor.fetchone():
            conn.close()
            return {"success": False,"data":"El depósito padre no existe."}
    
    # Actualizar el depósito
    cursor.execute("""
        UPDATE deposito
        SET nombre = COALESCE(?, nombre),
            padre_id = COALESCE(?, padre_id),
            almacena = COALESCE(?, almacena)
        WHERE id = ?
    """, (nombre, padre_id, almacena, id))
    conn.commit()
    conn.close()
    return {"success": True,"data": "Depósito actualizado."}

def eliminar_deposito(id):
    conn = conectar_db()
    cursor = conn.cursor()
    
    # Verificar si el depósito tiene hijos
    cursor.execute("SELECT id FROM deposito WHERE padre_id = ?", (id,))
    if cursor.fetchone():
        conn.close()
        return {"success": False,"data":"No se puede eliminar un depósito que tiene sub-depósitos."}
    
    # Verificar si el depósito tiene productos asociados
    cursor.execute("SELECT id FROM inventario_detalle WHERE deposito_id = ?", (id,))
    if cursor.fetchone():
        conn.close()
        return {"success": False,"data":"No se puede eliminar un depósito que contiene productos."}
    
    # Eliminar depósito
    cursor.execute("DELETE FROM deposito WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return {"success": True,"data":"Depósito eliminado."}

def consultar_deposito(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, padre_id, almacena FROM deposito WHERE id = ?", (id,))
    deposito = cursor.fetchone()
    conn.close()
    return {"id": deposito[0], "nombre": deposito[1], "padre_id": deposito[2], "almacena": bool(deposito[3])} if deposito else {"error": "Depósito no encontrado."}

def listar_depositos(filtro_almacena=None):
    conn = conectar_db()
    cursor = conn.cursor()
    
    query = "SELECT id, nombre, padre_id, almacena FROM deposito"
    params = []
    
    if filtro_almacena is not None:
        query += " WHERE almacena = ?"
        params.append(filtro_almacena)
    
    cursor.execute(query, params)
    depositos = cursor.fetchall()
    conn.close()
    
    # Construir estructura jerárquica
    depositos_dict = {dep[0]: {"id": dep[0], "nombre": dep[1], "padre_id": dep[2], "almacena": bool(dep[3]), "hijos": []} for dep in depositos}
    
    for dep in depositos_dict.values():
        if dep["padre_id"] is not None and dep["padre_id"] in depositos_dict:
            depositos_dict[dep["padre_id"]]["hijos"].append(dep)
    
    return [dep for dep in depositos_dict.values() if dep["padre_id"] is None]
