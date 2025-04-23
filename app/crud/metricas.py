from fastapi import APIRouter
from app.database import get_connection

router = APIRouter()

@router.get("/reservas_activas")
def listar_reservas_activas():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT r.idreserva, c.nombre, r.valortotal
            FROM pyreserva r
            JOIN pycliente c ON r.cliente_idcliente = c.idcliente
            WHERE r.estado = 1
            ORDER BY r.idreserva
        """)
        resultado = [
            {"idreserva": row[0], "cliente": row[1], "total": row[2]}
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


@router.get("/pasajeros")
def listar_pasajeros():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT nombre, dpi, edad, procedencia
            FROM pypasajero
            ORDER BY nombre
        """)
        resultado = [
            {"nombre": row[0], "dpi": row[1], "edad": row[2], "procedencia": row[3]}
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


@router.get("/pasajeros_por_vuelo")
def pasajeros_por_vuelo():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT p.nombre, v.descripcion, b.noasiento, b.costo
            FROM pyboleto b
            JOIN pypasajero p ON b.pasajero_idpasajero = p.idpasajero
            JOIN pyvuelo v ON b.vuelo_idvuelo = v.idvuelo
            ORDER BY v.descripcion, p.nombre
        """)
        resultado = [
            {"pasajero": row[0], "vuelo": row[1], "asiento": row[2], "costo": row[3]}
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


@router.get("/escalas")
def escalas_por_vuelo():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("""
            SELECT v.idvuelo, v.descripcion, p.nombre
            FROM pyescala e
            JOIN pyvuelo v ON e.vuelo_idvuelo = v.idvuelo
            JOIN pypais p ON e.pais_escala = p.idpais
            ORDER BY v.idvuelo, p.nombre
        """)
        resultado = [
            {"vuelo_id": row[0], "descripcion": row[1], "pais_escala": row[2]}
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
