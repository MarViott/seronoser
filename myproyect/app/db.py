import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de base de datos desde variables de entorno
host = os.getenv("DB_HOST", "localhost")
port = int(os.getenv("DB_PORT", "5432"))
user = os.getenv("DB_USER", "postgres")
clave = os.getenv("DB_PASSWORD", "")
db = os.getenv("DB_NAME", "ecommerce")


def conexionMySQL():
    """
    Establece y retorna una conexión a la base de datos PostgreSQL.
    
    Returns:
        psycopg2.Connection: Objeto de conexión a la base de datos
        
    Raises:
        psycopg2.Error: Si hay un error al conectar con la base de datos
    """
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=clave,
            database=db
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise