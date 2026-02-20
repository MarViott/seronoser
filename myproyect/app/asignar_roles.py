"""
Script para asignar roles a usuarios
Usa este script para hacer administradores o editores a usuarios específicos
"""

from db import conexionMySQL

def asignar_rol(usuario_id=None, email=None, rol='administrador'):
    """
    Asignar rol a un usuario específico
    
    Args:
        usuario_id: ID del usuario (opcional)
        email: Email del usuario (opcional)
        rol: 'administrador', 'editor', o 'usuario'
    """
    try:
        if not usuario_id and not email:
            print("❌ Debes proporcionar usuario_id o email")
            return
        
        if rol not in ['administrador', 'editor', 'usuario']:
            print("❌ Rol inválido. Usa: 'administrador', 'editor', o 'usuario'")
            return
        
        conexion = conexionMySQL()
        cursor = conexion.cursor()
        
        if usuario_id:
            cursor.execute(
                "UPDATE usuarios_auth SET rol = %s WHERE id = %s",
                (rol, usuario_id)
            )
            identifier = f"ID {usuario_id}"
        else:
            cursor.execute(
                "UPDATE usuarios_auth SET rol = %s WHERE email = %s",
                (rol, email)
            )
            identifier = f"email {email}"
        
        conexion.commit()
        
        if cursor.rowcount > 0:
            print(f"✅ Usuario {identifier} actualizado a rol '{rol}'")
        else:
            print(f"⚠️  No se encontró usuario con {identifier}")
        
        cursor.close()
        conexion.close()
        
    except Exception as e:
        print(f"❌ Error al asignar rol: {e}")

def hacer_admin_primer_usuario():
    """Hacer administrador al primer usuario registrado"""
    try:
        conexion = conexionMySQL()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id, nombre, email FROM usuarios_auth ORDER BY id LIMIT 1")
        usuario = cursor.fetchone()
        
        if usuario:
            cursor.execute("UPDATE usuarios_auth SET rol = 'administrador' WHERE id = %s", (usuario['id'],))
            conexion.commit()
            print(f"✅ Usuario '{usuario['nombre']}' ({usuario['email']}) es ahora ADMINISTRADOR")
        else:
            print("⚠️  No hay usuarios en la base de datos")
        
        cursor.close()
        conexion.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def listar_usuarios():
    """Mostrar todos los usuarios con sus roles"""
    try:
        conexion = conexionMySQL()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id, nombre, apellido, email, rol FROM usuarios_auth ORDER BY id")
        usuarios = cursor.fetchall()
        
        if usuarios:
            print()
            print("👥 USUARIOS Y SUS ROLES")
            print("=" * 90)
            print(f"{'ID':<5} {'Nombre':<25} {'Email':<35} {'Rol':<15}")
            print("-" * 90)
            for u in usuarios:
                nombre_completo = f"{u['nombre']} {u['apellido'] or ''}".strip()
                rol_emoji = {
                    'administrador': '👑',
                    'editor': '✏️',
                    'usuario': '👤'
                }.get(u['rol'], '❓')
                print(f"{u['id']:<5} {nombre_completo:<25} {u['email']:<35} {rol_emoji} {u['rol']:<15}")
            print("=" * 90)
        else:
            print("No hay usuarios registrados")
        
        cursor.close()
        conexion.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🔐 GESTIÓN DE ROLES")
    print()
    
    # Hacer administrador al primer usuario
    hacer_admin_primer_usuario()
    
    # Listar todos los usuarios
    listar_usuarios()
    
    print()
    print("💡 Para asignar roles manualmente, usa:")
    print("   - asignar_rol(usuario_id=2, rol='editor')")
    print("   - asignar_rol(email='user@example.com', rol='administrador')")
