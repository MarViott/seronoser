from db import conexionMySQL
import psycopg2
import psycopg2.extras

# Read - select
def obtener_usuarios():
    """
    Obtiene todos los usuarios de la base de datos.
    
    Returns:
        list: Lista de usuarios o lista vacía si hay error
    """
    try:
        conexion = conexionMySQL()
        with conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            query = "SELECT * FROM usuarios ORDER BY id"
            cursor.execute(query)
            result = cursor.fetchall()
        conexion.close()
        return result
    except psycopg2.Error as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    except Exception as e:
        print(f"Error inesperado al obtener usuarios: {e}")
        return []
    

def cargar_nuevo_usuario(nombre, email, ocupacion):
    """
    Crea un nuevo usuario en la base de datos.
    
    Args:
        nombre (str): Nombre del usuario
        email (str): Email del usuario
        ocupacion (str): Ocupación del usuario
        
    Returns:
        bool: True si se creó exitosamente, False en caso contrario
    """
    try:
        conexion = conexionMySQL()
        with conexion.cursor() as cursor:
            query = "INSERT INTO usuarios (nombre, email, ocupacion) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre, email, ocupacion))
            conexion.commit()
        conexion.close()
        return True
    except psycopg2.Error as e:
        print(f"Error al cargar nuevo usuario: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado al cargar nuevo usuario: {e}")
        return False
    

def obtener_usuario_por_id(id):
    """
    Obtiene un usuario específico por su ID.
    
    Args:
        id (int): ID del usuario
        
    Returns:
        dict/tuple: Usuario encontrado o None si no existe o hay error
    """
    try:
        conexion = conexionMySQL()
        with conexion.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            query = "SELECT * FROM usuarios WHERE id = %s"
            cursor.execute(query, (id,))
            usuario = cursor.fetchone()
        conexion.close()
        return usuario
    except psycopg2.Error as e:
        print(f"Error al obtener usuario por id {id}: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al obtener usuario por id {id}: {e}")
        return None


def actualizar_usuario(nombre, email, ocupacion, id):
    """
    Actualiza los datos de un usuario existente.
    
    Args:
        nombre (str): Nuevo nombre del usuario
        email (str): Nuevo email del usuario
        ocupacion (str): Nueva ocupación del usuario
        id (int): ID del usuario a actualizar
        
    Returns:
        bool: True si se actualizó exitosamente, False en caso contrario
    """
    try:
        conexion = conexionMySQL()
        with conexion.cursor() as cursor:
            query = "UPDATE usuarios SET nombre = %s, email = %s, ocupacion = %s WHERE id = %s"
            cursor.execute(query, (nombre, email, ocupacion, id))
            conexion.commit()
        conexion.close()
        return True
    except psycopg2.Error as e:
        print(f"Error al actualizar usuario {id}: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado al actualizar usuario {id}: {e}")
        return False


# borrar -> delete
def eliminar_usuario(id):
    """
    Elimina un usuario de la base de datos.
    
    Args:
        id (int): ID del usuario a eliminar
        
    Returns:
        bool: True si se eliminó exitosamente, False en caso contrario
    """
    try:
        conexion = conexionMySQL()
        with conexion.cursor() as cursor:
            query = "DELETE FROM usuarios WHERE id = %s"
            cursor.execute(query, (id,))
            conexion.commit()
        conexion.close()
        return True
    except psycopg2.Error as e:
        print(f"Error al eliminar usuario {id}: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado al eliminar usuario {id}: {e}")
        return False