import oracledb

def get_connection():
    try:
        connection = oracledb.connect(
            user="ANDREA22",
            password="ANDREA22",
            dsn="localhost:1521/XE"
        )
        print("Conectado a Oracle")
        return connection
    except Exception as e:
        print("❌ Error al conectar a Oracle:", e)
        raise

