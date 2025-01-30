from fastapi import FastAPI, HTTPException, Depends, Query
from typing import List, Optional
from pydantic import BaseModel
from services import deposito_service
from database import conectar_db
import services.producto_service as producto_service
from datetime import datetime


# Inicializamos la API
app = FastAPI(title="Inventario API", version="1.0")

# Inicializamos la base de datos
conectar_db()

# Modelos Pydantic para validación
class DepositoCreate(BaseModel):
    nombre: str
    padre_id: Optional[int] = None
    almacena: bool

class DepositoUpdate(BaseModel):
    nombre: Optional[str] = None
    padre_id: Optional[int] = None
    almacena: Optional[bool] = None

class InventarioCreate(BaseModel):
    inventario_id: int

class InventarioUpdate(BaseModel):
    inventario_id: Optional[int]
    fecha: Optional[datetime]


# Endpoints para depósitos

@app.post("/depositos/", response_model=dict)
def crear_deposito(deposito: DepositoCreate):
    """Crea un nuevo depósito con validaciones."""
    result = deposito_service.crear_deposito(deposito.nombre, deposito.padre_id, deposito.almacena)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["data"])
    return {"mensaje": "Depósito creado exitosamente", "data": result["data"]}

@app.put("/depositos/{deposito_id}", response_model=dict)
def modificar_deposito(deposito_id: int, deposito: DepositoUpdate):
    """Modifica un depósito existente."""
    result = deposito_service.modificar_deposito(deposito_id, deposito.nombre, deposito.padre_id, deposito.almacena)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["data"])
    return {"mensaje": "Depósito actualizado", "data": result["data"]}

@app.delete("/depositos/{deposito_id}", response_model=dict)
def eliminar_deposito(deposito_id: int):
    """Elimina un depósito si cumple con las condiciones."""
    result = deposito_service.eliminar_deposito(deposito_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["data"])
    return {"mensaje": "Depósito eliminado"}

@app.get("/depositos/{deposito_id}", response_model=dict)
def consultar_deposito(deposito_id: int):
    """Consulta un depósito por su ID."""
    result = deposito_service.consultar_deposito(deposito_id)
    if not result:
        raise HTTPException(status_code=404, detail="Depósito no encontrado")
    return {"data": result}

@app.get("/depositos/", response_model=dict)
def listar_depositos(almacena: Optional[bool] = Query(None, description="Filtrar por almacena")):
    """Lista todos los depósitos, con opción de filtrar por almacena."""
    result = deposito_service.listar_depositos(almacena)
    return {"data": result}

@app.post("/productos/", response_model=dict)
def crear_producto(producto: producto_service.ProductoCreate):
    """Crea un nuevo producto."""
    result = producto_service.crear_producto(producto)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {"mensaje": result["message"]}

@app.put("/productos/{codigo_alfa}", response_model=dict)
def modificar_producto(codigo_alfa: str, producto: producto_service.ProductoUpdate):
    """Modifica un producto existente."""
    result = producto_service.modificar_producto(codigo_alfa, producto)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {"mensaje": result["message"]}

@app.get("/productos/{codigo_alfa}", response_model=dict)
def consultar_producto(codigo_alfa: str):
    """Consulta un producto por su Código Alfa."""
    producto = producto_service.consultar_producto(codigo_alfa)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"data": producto}

@app.get("/productos/", response_model=dict)
def listar_productos(
    codigo_alfa: Optional[str] = Query(None),
    codigo_barras: Optional[str] = Query(None),
    descripcion: Optional[str] = Query(None),
    precio: Optional[float] = Query(None),
    proveedor_codigo: Optional[str] = Query(None),
    proveedor_nombre: Optional[str] = Query(None)
):
    """Lista productos con filtros opcionales."""
    filtros = {k: v for k, v in {
        "codigo_alfa": codigo_alfa,
        "codigo_barras": codigo_barras,
        "descripcion": descripcion,
        "precio": precio,
        "proveedor_codigo": proveedor_codigo,
        "proveedor_nombre": proveedor_nombre
    }.items() if v is not None}

    productos = producto_service.listar_productos(filtros)
    return {"data": productos}

@app.delete("/productos/{codigo_alfa}", response_model=dict)
def eliminar_producto(codigo_alfa: str):
    """Elimina un producto si cumple con las condiciones."""
    result = producto_service.eliminar_producto(codigo_alfa)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["data"])
    return {"mensaje": "Producto eliminado"}

# Endpoints para inventario

@app.post("/inventario/", response_model=dict)
def crear_inventario(inventario: InventarioCreate):
    """Crea un nuevo registro de inventario."""
    result = inventario_service.crear_inventario(inventario.inventario_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {"mensaje": "Inventario creado exitosamente", "data": result["data"]}

@app.put("/inventario/{inventario_id}", response_model=dict)
def modificar_inventario(inventario_id: int, inventario: InventarioUpdate):
    """Modifica un registro de inventario existente."""
    result = inventario_service.modificar_inventario(inventario_id, inventario.inventario_id, inventario.fecha)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {"mensaje": "Inventario actualizado", "data": result["data"]}

@app.delete("/inventario/{inventario_id}", response_model=dict)
def eliminar_inventario(inventario_id: int):
    """Elimina un registro de inventario."""
    result = inventario_service.eliminar_inventario(inventario_id)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return {"mensaje": "Inventario eliminado", "data": result["data"]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)