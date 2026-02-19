import pymysql
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de base de datos desde variables de entorno
host = os.getenv("DB_HOST", "localhost")
port = int(os.getenv("DB_PORT", "3306"))
user = os.getenv("DB_USER", "root")
clave = os.getenv("DB_PASSWORD", "")
db = os.getenv("DB_NAME", "seronoser")


def conexionMySQL():
    """
    Establece y retorna una conexión a la base de datos MySQL.
    
    Returns:
        pymysql.Connection: Objeto de conexión a la base de datos
        
    Raises:
        pymysql.Error: Si hay un error al conectar con la base de datos
    """
    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=clave,
            database=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        raise