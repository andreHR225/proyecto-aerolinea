from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import oracledb
from app.database import get_connection  # Asegúrate que 'app/database.py' exista
from datetime import datetime

router = APIRouter()

# Modelo de entrada para registrar un vuelo
class VueloInput(BaseModel):
    descripcion: str
    avion_id: int
    pais_origen: int
    pais_destino: int
    fecha: str  # Formato YYYY-MM-DD
    disponibles: int
    escalas: List[int]

# POST /vuelos - Registrar nuevo vuelo
@router.post("/vuelos")
def registrar_vuelo(data: VueloInput):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        resultado = cursor.var(str)

        # Obtener el tipo Oracle T_NUM_TABLA y convertir la lista
        T_NUM_TABLA = connection.gettype("T_NUM_TABLA")
        escalas_obj = T_NUM_TABLA.newobject()
        escalas_obj.extend(data.escalas)

        fecha_date = datetime.strptime(data.fecha, "%Y-%m-%d")


        # Llamar al procedimiento en Oracle
        cursor.callproc("SP_REGISTRAR_VUELO", [
            data.descripcion,
            data.avion_id,
            data.pais_origen,
            data.pais_destino,
            fecha_date,
            data.disponibles,
            escalas_obj,
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

# GET /vuelos - Listar vuelos disponibles
@router.get("/vuelos")
def listar_vuelos():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT idvuelo, descripcion, TO_CHAR(fecha, 'YYYY-MM-DD'), disponibles
            FROM pyvuelo
            ORDER BY idvuelo
        """)

        vuelos = [
            {
                "id": row[0],
                "descripcion": row[1],
                "fecha": row[2],
                "disponibles": row[3]
            }
            for row in cursor.fetchall()
        ]

        return vuelos

    except Exception as e:
        return {"error": str(e)}

    finally:
        try:
            cursor.close()
            connection.close()
        except:
            pass
