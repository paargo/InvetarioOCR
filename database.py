import sqlite3

def conectar_db():
    return sqlite3.connect("inventario.db")

def crear_tablas():
    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deposito (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            padre_id INTEGER,
            almacena BOOLEAN NOT NULL CHECK (almacena IN (0,1)),
            FOREIGN KEY (padre_id) REFERENCES deposito(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
            estado TEXT CHECK (estado IN ('En Proceso', 'Finalizado')) NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,      
            codigo_alfa TEXT NOT NULL UNIQUE,
            codigo_barras TEXT,
            descripcion TEXT,
            precio REAL,
            proveedor_codigo TEXT,
            proveedor_nombre TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inventario_id INTEGER NOT NULL,
            fecha DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventario_detalle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inventario_id INTEGER NOT NULL,
            deposito_id INTEGER NOT NULL,
            codigo_alfa TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            FOREIGN KEY (inventario_id) REFERENCES inventario(inventario_id),
            FOREIGN KEY (deposito_id) REFERENCES deposito(id),
            FOREIGN KEY (codigo_alfa) REFERENCES producto(codigo_alfa)
        )
    ''')
    
    conn.commit()
    conn.close()

# Ejecutar la creación de tablas al inicio
crear_tablas()
