from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from db import conexionMySQL
import pymysql
import secrets
from datetime import datetime, timedelta


class User(UserMixin):
    """Modelo de usuario para Flask-Login"""
    
    def __init__(self, id, nombre, apellido, email, activo=True):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.activo = activo
    
    @property
    def is_active(self):
        return self.activo
    
    def get_id(self):
        return str(self.id)
    
    @staticmethod
    def get_by_id(user_id):
        """Obtener usuario por ID"""
        try:
            conexion = conexionMySQL()
            with conexion.cursor() as cursor:
                query = "SELECT id, nombre, apellido, email, activo FROM usuarios_auth WHERE id = %s AND activo = TRUE"
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
            conexion.close()
            
            if result:
                return User(
                    id=result['id'],
                    nombre=result['nombre'],
                    apellido=result['apellido'],
                    email=result['email'],
                    activo=result['activo']
                )
            return None
        except Exception as e:
            print(f"Error al obtener usuario por ID: {e}")
            return None
    
    @staticmethod
    def get_by_email(email):
        """Obtener usuario por email - retorna objeto User"""
        try:
            conexion = conexionMySQL()
            with conexion.cursor() as cursor:
                query = "SELECT id, nombre, apellido, email, password_hash, activo FROM usuarios_auth WHERE email = %s"
                cursor.execute(query, (email,))
                result = cursor.fetchone()
            conexion.close()
            
            if result:
                # Crear objeto User a partir del resultado
                user = User(
                    id=result['id'],
                    nombre=result['nombre'],
                    apellido=result['apellido'],
                    email=result['email'],
                    activo=result['activo']
                )
                # Guardar el hash para verificación de contraseña
                user.password_hash = result['password_hash']
                return user
            return None
        except Exception as e:
            print(f"Error al obtener usuario por email: {e}")
            return None
    
    @staticmethod
    def create(nombre, apellido, email, password, telefono=None):
        """Crear un nuevo usuario"""
        try:
            password_hash = generate_password_hash(password)
            conexion = conexionMySQL()
            with conexion.cursor() as cursor:
                query = """INSERT INTO usuarios_auth 
                          (nombre, apellido, email, password_hash, telefono) 
                          VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(query, (nombre, apellido, email, password_hash, telefono))
                conexion.commit()
                user_id = cursor.lastrowid
            conexion.close()
            return user_id
        except pymysql.IntegrityError:
            print(f"El email {email} ya está registrado")
            return None
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return None
    
    def verify_password(self, password):
        """Verificar contraseña del usuario (método de instancia)"""
        if hasattr(self, 'password_hash'):
            return check_password_hash(self.password_hash, password)
        return False
    
    @staticmethod
    def authenticate(email, password):
        """Autenticar usuario por email y contraseña (método estático)"""
        user = User.get_by_email(email)
        if user and user.verify_password(password):
            return user
        return None


# Funciones para manejar obras
def obtener_obras(solo_estrenos=False):
    """Obtiene obras de teatro desde la base de datos"""
    try:
        conexion = conexionMySQL()
        with conexion.cursor() as cursor:
            if solo_estrenos:
                query = "SELECT * FROM obras WHERE activo = TRUE AND es_estreno = TRUE ORDER BY fecha_creacion DESC"
            else:
                query = "SELECT * FROM obras WHERE activo = TRUE ORDER BY fecha_creacion DESC"
            cursor.execute(query)
            result = cursor.fetchall()
        conexion.close()
        return result
    except Exception as e:
        print(f"Error al obtener obras: {e}")
        return []


def obtener_obra_por_id(obra_id):
    """Obtiene una obra específica por ID"""
    try:
        conexion = conexionMySQL()
        with conexion.cursor() as cursor:
            query = "SELECT * FROM obras WHERE id = %s AND activo = TRUE"
            cursor.execute(query, (obra_id,))
            result = cursor.fetchone()
        conexion.close()
        return result
    except Exception as e:
        print(f"Error al obtener obra: {e}")
        return None


def crear_orden(usuario_id, obra_id, cantidad, precio_unitario, fecha_funcion):
    """Crea una nueva orden de compra"""
    try:
        conexion = conexionMySQL()
        subtotal = cantidad * precio_unitario
        
        with conexion.cursor() as cursor:
            # Crear orden
            query_orden = "INSERT INTO ordenes (usuario_id, total, estado) VALUES (%s, %s, 'pendiente')"
            cursor.execute(query_orden, (usuario_id, subtotal))
            orden_id = cursor.lastrowid
            
            # Crear detalle de orden
            query_detalle = """INSERT INTO orden_detalles 
                              (orden_id, obra_id, cantidad, precio_unitario, subtotal, fecha_funcion)
                              VALUES (%s, %s, %s, %s, %s, %s)"""
            cursor.execute(query_detalle, (orden_id, obra_id, cantidad, precio_unitario, subtotal, fecha_funcion))
            
            conexion.commit()
        conexion.close()
        return orden_id
    except Exception as e:
        print(f"Error al crear orden: {e}")
        return None


def obtener_ordenes_usuario(usuario_id):
    """Obtiene todas las órdenes de un usuario"""
    try:
        conexion = conexionMySQL()
        with conexion.cursor() as cursor:
            query = """
                SELECT o.*, od.obra_id, od.cantidad, od.fecha_funcion, ob.titulo, ob.teatro
                FROM ordenes o
                JOIN orden_detalles od ON o.id = od.orden_id
                JOIN obras ob ON od.obra_id = ob.id
                WHERE o.usuario_id = %s
                ORDER BY o.fecha_orden DESC
            """
            cursor.execute(query, (usuario_id,))
            result = cursor.fetchall()
        conexion.close()
        return result
    except Exception as e:
        print(f"Error al obtener órdenes: {e}")
        return []


# ===== FUNCIONES DE RECUPERACIÓN DE CONTRASEÑA =====

def crear_token_recuperacion(email):
    """
    Crea un token de recuperación de contraseña para un usuario
    
    Args:
        email: Email del usuario
    
    Returns:
        str: Token generado, o None si hay error
    """
    try:
        # Verificar que el usuario existe
        user = User.get_by_email(email)
        if not user:
            return None
        
        # Generar token único
        token = secrets.token_urlsafe(32)
        
        # Expiración: 1 hora desde ahora
        fecha_expiracion = datetime.now() + timedelta(hours=1)
        
        conexion = conexionMySQL()
        with conexion.cursor() as cursor:
            query = """INSERT INTO password_reset_tokens 
                      (usuario_id, token, fecha_expiracion) 
                      VALUES (%s, %s, %s)"""
            cursor.execute(query, (user.id, token, fecha_expiracion))
            conexion.commit()
        conexion.close()
        
        return token
    except Exception as e:
        print(f"Error al crear token de recuperación: {e}")
        return None


def validar_token_recuperacion(token):
    """
    Valida un token de recuperación de contraseña
    
    Args:
        token: Token a validar
    
    Returns:
        dict: Datos del token si es válido, None si no lo es
    """
    try:
        conexion = conexionMySQL()
        with conexion.cursor() as cursor:
            query = """SELECT * FROM password_reset_tokens 
                      WHERE token = %s 
                      AND usado = FALSE 
                      AND fecha_expiracion > NOW()"""
            cursor.execute(query, (token,))
            result = cursor.fetchone()
        conexion.close()
        return result
    except Exception as e:
        print(f"Error al validar token: {e}")
        return None


def resetear_password(token, nueva_password):
    """
    Resetea la contraseña de un usuario usando un token válido
    
    Args:
        token: Token de recuperación
        nueva_password: Nueva contraseña
    
    Returns:
        bool: True si se resetó correctamente, False si no
    """
    try:
        # Validar token
        token_data = validar_token_recuperacion(token)
        if not token_data:
            return False
        
        usuario_id = token_data['usuario_id']
        
        # Actualizar contraseña
        password_hash = generate_password_hash(nueva_password)
        
        conexion = conexionMySQL()
        with conexion.cursor() as cursor:
            # Actualizar password
            query_update = """UPDATE usuarios_auth 
                            SET password_hash = %s 
                            WHERE id = %s"""
            cursor.execute(query_update, (password_hash, usuario_id))
            
            # Marcar token como usado
            query_token = """UPDATE password_reset_tokens 
                           SET usado = TRUE 
                           WHERE token = %s"""
            cursor.execute(query_token, (token,))
            
            conexion.commit()
        conexion.close()
        
        return True
    except Exception as e:
        print(f"Error al resetear password: {e}")
        return False
