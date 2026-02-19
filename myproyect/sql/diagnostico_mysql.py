#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la conexión a MySQL
"""
import pymysql

print("="*60)
print("🔍 DIAGNÓSTICO DE CONEXIÓN A MYSQL")
print("="*60)

# Probar diferentes puertos comunes de XAMPP
puertos = [3306, 3307, 3308]
usuarios = ['root', 'admin']
passwords = ['', 'root', 'admin']

conexion_exitosa = False
config_correcta = {}

for puerto in puertos:
    for usuario in usuarios:
        for password in passwords:
            try:
                print(f"\n🔌 Probando: {usuario}@localhost:{puerto} (password={'***' if password else 'vacía'})")
                
                connection = pymysql.connect(
                    host='localhost',
                    port=puerto,
                    user=usuario,
                    password=password,
                    charset='utf8mb4'
                )
                
                cursor = connection.cursor()
                cursor.execute("SELECT VERSION()")
                version = cursor.fetchone()[0]
                
                print(f"   ✅ ¡CONEXIÓN EXITOSA!")
                print(f"   📌 MySQL versión: {version}")
                
                # Listar bases de datos
                cursor.execute("SHOW DATABASES")
                databases = [db[0] for db in cursor.fetchall()]
                print(f"   📊 Bases de datos encontradas: {', '.join(databases)}")
                
                # Verificar si existe 'seronoser'
                if 'seronoser' in databases:
                    print(f"   ✨ La base de datos 'seronoser' YA EXISTE")
                else:
                    print(f"   ⚠️  La base de datos 'seronoser' NO EXISTE (necesita crearse)")
                
                config_correcta = {
                    'host': 'localhost',
                    'port': puerto,
                    'user': usuario,
                    'password': password,
                    'databases': databases
                }
                
                conexion_exitosa = True
                cursor.close()
                connection.close()
                break
                
            except pymysql.Error as e:
                print(f"   ❌ Error: {e}")
                continue
        
        if conexion_exitosa:
            break
    
    if conexion_exitosa:
        break

print("\n" + "="*60)

if conexion_exitosa:
    print("✅ CONFIGURACIÓN ENCONTRADA")
    print("="*60)
    print(f"\nConexión exitosa con:")
    print(f"  Host: {config_correcta['host']}")
    print(f"  Puerto: {config_correcta['port']}")
    print(f"  Usuario: {config_correcta['user']}")
    print(f"  Password: {'(vacía)' if not config_correcta['password'] else '***'}")
    
    print(f"\n📝 Crear archivo .env con estos valores:")
    print("-" * 60)
    print(f"DB_HOST={config_correcta['host']}")
    print(f"DB_PORT={config_correcta['port']}")
    print(f"DB_USER={config_correcta['user']}")
    print(f"DB_PASSWORD={config_correcta['password']}")
    print(f"DB_NAME=seronoser")
    print(f"FLASK_APP=app.py")
    print(f"FLASK_ENV=development")
    print(f"SECRET_KEY=cambiar-en-produccion-por-clave-aleatoria")
    print("-" * 60)
    
    if 'seronoser' not in config_correcta['databases']:
        print(f"\n⚠️  ACCIÓN REQUERIDA:")
        print(f"   La base de datos 'seronoser' no existe.")
        print(f"   Opciones:")
        print(f"   1. Crearla desde phpMyAdmin (http://localhost/phpmyadmin)")
        print(f"   2. Crear automáticamente (presiona Enter para continuar)")
        
        crear = input("\n¿Deseas crear la base de datos 'seronoser' ahora? (s/n): ")
        
        if crear.lower() in ['s', 'si', 'y', 'yes', '']:
            try:
                connection = pymysql.connect(
                    host=config_correcta['host'],
                    port=config_correcta['port'],
                    user=config_correcta['user'],
                    password=config_correcta['password'],
                    charset='utf8mb4'
                )
                cursor = connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS seronoser CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                connection.commit()
                cursor.close()
                connection.close()
                print("   ✅ Base de datos 'seronoser' creada exitosamente")
            except Exception as e:
                print(f"   ❌ Error al crear base de datos: {e}")
    
else:
    print("❌ NO SE PUDO CONECTAR A MYSQL")
    print("="*60)
    print("\n💡 Sugerencias:")
    print("   1. Verifica que MySQL esté corriendo en XAMPP")
    print("   2. Abre el Panel de Control de XAMPP")
    print("   3. Inicia el servicio MySQL")
    print("   4. Vuelve a ejecutar este script")
