#!/usr/bin/env python3
"""
Instalador automático completo del e-commerce
Crea la base de datos y ejecuta el schema
"""
import pymysql
from pathlib import Path

print("="*60)
print("🎭 INSTALACIÓN AUTOMÁTICA E-COMMERCE")
print("   Ser o No Ser - Sistema de Tickets")
print("="*60)

# Configuración detectada
CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': '',
    'database': 'seronoser'
}

try:
    # Paso 1: Crear archivo .env
    print("\n📝 Creando archivo .env...")
    env_content = f"""# Database Configuration
DB_HOST={CONFIG['host']}
DB_PORT={CONFIG['port']}
DB_USER={CONFIG['user']}
DB_PASSWORD={CONFIG['password']}
DB_NAME={CONFIG['database']}

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=5f9a8c3d7b2e1a6f4c8b9d3e7a2c5f8b1d4e7a3c6f9b2d5e8a1c4f7b3d6e9a2c5f8
"""
    
    env_path = Path(__file__).parent.parent / 'app' / '.env'
    env_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"   ✅ Archivo .env creado en: {env_path}")
    
    # Paso 2: Conectar a MySQL
    print(f"\n🔌 Conectando a MySQL en puerto {CONFIG['port']}...")
    connection = pymysql.connect(
        host=CONFIG['host'],
        port=CONFIG['port'],
        user=CONFIG['user'],
        password=CONFIG['password'],
        charset='utf8mb4'
    )
    cursor = connection.cursor()
    print("   ✅ Conectado exitosamente")
    
    # Paso 3: Crear base de datos
    print(f"\n🗄️  Creando base de datos '{CONFIG['database']}'...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {CONFIG['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    connection.commit()
    print(f"   ✅ Base de datos '{CONFIG['database']}' lista")
    
    # Paso 4: Usar la base de datos
    cursor.execute(f"USE {CONFIG['database']}")
    
    # Paso 5: Leer y ejecutar schema
    schema_file = Path(__file__).parent / 'ecommerce_schema.sql'
    print(f"\n📄 Leyendo schema: {schema_file.name}")
    
    with open(schema_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Dividir en sentencias
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    print(f"   📊 {len(statements)} sentencias SQL encontradas")
    
    # Ejecutar sentencias
    print(f"\n🚀 Ejecutando schema...\n")
    for i, statement in enumerate(statements, 1):
        if statement:
            try:
                cursor.execute(statement)
                
                if 'CREATE TABLE' in statement.upper():
                    table_name = statement.split('`')[1] if '`' in statement else 'desconocida'
                    print(f"   ✓ [{i}/{len(statements)}] Tabla creada: {table_name}")
                elif 'DROP TABLE' in statement.upper():
                    table_name = statement.split('`')[1] if '`' in statement else 'desconocida'
                    print(f"   ✓ [{i}/{len(statements)}] Tabla eliminada: {table_name}")
                elif 'INSERT INTO' in statement.upper():
                    table_name = statement.split('`')[1] if '`' in statement else 'desconocida'
                    print(f"   ✓ [{i}/{len(statements)}] Datos insertados en: {table_name}")
                else:
                    print(f"   ✓ [{i}/{len(statements)}] Sentencia ejecutada")
                    
            except pymysql.Error as e:
                print(f"   ⚠️  [{i}/{len(statements)}] Advertencia: {e}")
    
    connection.commit()
    
    # Verificar tablas
    print(f"\n📋 Verificando instalación:")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
        count = cursor.fetchone()[0]
        print(f"   ✓ {table_name}: {count} registros")
    
    cursor.close()
    connection.close()
    
    print("\n" + "="*60)
    print("✅ ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
    print("="*60)
    print("\n🎉 El sistema de e-commerce está listo")
    print("\nPróximos pasos:")
    print("   1. Inicia el servidor: python app/app.py")
    print("   2. Abre: http://localhost:5000")
    print("   3. Regístrate en: http://localhost:5000/registro")
    print("   4. ¡Compra entradas!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
