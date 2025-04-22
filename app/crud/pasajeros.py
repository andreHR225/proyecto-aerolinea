from fastapi import APIRouter
from pydantic import BaseModel
from app.database import get_connection

router = APIRouter()

class PasajeroInput(BaseModel):
    reserva_id: int
    nombre: str
    dpi: str
    edad: int
    vacunacion: str
    procedencia: str
    costo: float
    noasiento: str

@router.post("/pasajero")
def registrar_pasajero_boleto(datos: PasajeroInput):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        resultado = cursor.var(str)

        cursor.callproc("py_sp_registrar_pasajero_boleto", [
            datos.reserva_id,
            datos.nombre,
            datos.dpi,
            datos.edad,
            datos.vacunacion,
            datos.procedencia,
            datos.costo,
            datos.noasiento,
            resultado
        ])

        connection.commit()
        return {"mensaje": resultado.getvalue()}

    except Exception as e:
        print("❌ Error:", e)
        return {"error": str(e)}

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass

