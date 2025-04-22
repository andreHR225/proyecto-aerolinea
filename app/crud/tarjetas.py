from fastapi import APIRouter, Query
from app.database import get_connection

router = APIRouter()

@router.get("/tarjeta")
def obtener_tarjeta(cliente_id: int = Query(...)):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT idtarjeta
            FROM pytarjeta
            WHERE cliente_idcliente = :cliente_id
            FETCH FIRST 1 ROW ONLY
        """, {"cliente_id": cliente_id})

        row = cursor.fetchone()
        if row:
            return {"tarjeta_id": row[0]}
        else:
            return {"error": "Cliente no tiene tarjeta registrada."}

    except Exception as e:
        return {"error": str(e)}

    finally:
        cursor.close()
        connection.close()
