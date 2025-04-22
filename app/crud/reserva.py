from fastapi import APIRouter
from pydantic import BaseModel
from app.database import get_connection

router = APIRouter()

class ReservaInput(BaseModel):
    cliente_id: int
    tarjeta_id: str
    vuelo_id: int
    total_asientos: int
    total_cobro: float

@router.post("/reserva")
def crear_reserva(datos: ReservaInput):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        resultado = cursor.var(str)

        cursor.callproc("py_sp_reservar_asientos", [
            datos.cliente_id,
            datos.tarjeta_id,
            datos.vuelo_id,
            datos.total_asientos,
            datos.total_cobro,
            resultado
        ])

        connection.commit()
        return {"mensaje": resultado.getvalue()}

    except Exception as e:
        print("❌ Error en reserva:", e)
        return {"error": str(e)}

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass

