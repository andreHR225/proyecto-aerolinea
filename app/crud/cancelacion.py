from fastapi import APIRouter
from pydantic import BaseModel
from app.database import get_connection

router = APIRouter()

class CancelacionInput(BaseModel):
    reserva_id: int

@router.post("/cancelacion")  
def cancelar_reserva(datos: CancelacionInput):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        resultado = cursor.var(str)

        cursor.callproc("py_sp_cancelar_reserva", [
            datos.reserva_id,
            resultado
        ])

        connection.commit()
        return {"mensaje": resultado.getvalue()}

    except Exception as e:
        return {"error": str(e)}

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass
