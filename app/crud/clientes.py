from fastapi import APIRouter
from pydantic import BaseModel
from app.database import get_connection

router = APIRouter()


class ClienteInput(BaseModel):
    nombre: str
    dpi: str
    telefono: str
    tarjeta: str
    descripcion: str
    saldo: float


@router.post("/cliente")
def registrar_cliente_y_tarjeta(datos: ClienteInput):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Obtener nuevo ID de cliente
        cursor.execute("SELECT NVL(MAX(idcliente), 0) + 1 FROM pycliente")
        nuevo_id = cursor.fetchone()[0]

        # Insertar cliente
        cursor.execute("""
            INSERT INTO pycliente (idcliente, nombre, dpi, telefono)
            VALUES (:1, :2, :3, :4)
        """, (nuevo_id, datos.nombre, datos.dpi, datos.telefono))

        # Insertar tarjeta vinculada al cliente
        cursor.execute("""
            INSERT INTO pytarjeta (idtarjeta, descripcion, saldo, cliente_idcliente)
            VALUES (:1, :2, :3, :4)
        """, (datos.tarjeta, datos.descripcion, datos.saldo, nuevo_id))

        connection.commit()
        return {"mensaje": "✅ Cliente y tarjeta registrados correctamente."}

    except Exception as e:
        connection.rollback()
        return {"error": f"❌ Error al registrar cliente: {str(e)}"}

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass


@router.get("/clientes")
def listar_clientes():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT idcliente, nombre FROM pycliente")
        resultado = [
            {"id": row[0], "nombre": row[1]}
            for row in cursor.fetchall()
        ]
        return resultado
    except Exception as e:
        return {"error": str(e)}
    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass

