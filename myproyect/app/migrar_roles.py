"""
Script para agregar el campo 'rol' a la tabla usuarios_auth
Ejecuta este script para aplicar la migración de roles
"""

from db import conexionMySQL

def migrar_roles():
    """Agregar columna rol a la tabla usuarios_auth"""
    try:
        conexion = conexionMySQL()
        cursor = conexion.cursor()
        
        print("🔄 Iniciando migración de roles...")
        
        # Verificar si la columna ya existe
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'ser_o_no_ser'
            AND TABLE_NAME = 'usuarios_auth'
            AND COLUMN_NAME = 'rol'
        """)
        
        result = cursor.fetchone()
        
        if result['count'] > 0:
            print("⚠️  La columna 'rol' ya existe en la tabla usuarios_auth")
            print("✅ No es necesario ejecutar la migración")
        else:
            # Agregar columna rol
            print("📝 Agregando columna 'rol' a usuarios_auth...")
            cursor.execute("""
                ALTER TABLE usuarios_auth 
                ADD COLUMN rol ENUM('usuario', 'editor', 'administrador') 
                DEFAULT 'usuario' 
                AFTER activo
            """)
            
            # Agregar índice
            print("📝 Agregando índice para optimización...")
            cursor.execute("""
                ALTER TABLE usuarios_auth 
                ADD INDEX idx_rol (rol)
            """)
            
            conexion.commit()
            print("✅ Migración completada exitosamente!")
            print()
            print("📌 Próximos pasos:")
            print("1. Asigna roles a los usuarios existentes")
            print("2. Ejemplo: UPDATE usuarios_auth SET rol = 'administrador' WHERE id = 1;")
            print("3. Reinicia el servidor Flask")
        
        # Mostrar usuarios actuales
        print()
        print("👥 Usuarios en la base de datos:")
        print("-" * 80)
        cursor.execute("SELECT id, nombre, apellido, email, rol FROM usuarios_auth")
        usuarios = cursor.fetchall()
        
        if usuarios:
            for usuario in usuarios:
                print(f"ID: {usuario['id']} | {usuario['nombre']} {usuario['apellido']} | {usuario['email']} | Rol: {usuario['rol']}")
        else:
            print("No hay usuarios registrados todavía")
        
        print("-" * 80)
        
        cursor.close()
        conexion.close()
        
    except Exception as e:
        print(f"❌ Error al ejecutar migración: {e}")
        print("Verifica que:")
        print("- MySQL esté corriendo en el puerto 3307")
        print("- La base de datos 'ser_o_no_ser' exista")
        print("- Las credenciales en .env sean correctas")

if __name__ == "__main__":
    migrar_roles()
