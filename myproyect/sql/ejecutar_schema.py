#!/usr/bin/env python3
"""
Script para ejecutar el schema de e-commerce en la base de datos MySQL
"""
import sys
import os
from pathlib import Path

# Agregar el directorio app al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

from dotenv import load_dotenv
import pymysql

# Cargar variables de entorno
load_dotenv(Path(__file__).parent.parent / 'app' / '.env')

def ejecutar_schema():
    """Ejecuta el archivo ecommerce_schema.sql en la base de datos"""
    
    # Leer el archivo SQL
    schema_file = Path(__file__).parent / 'ecommerce_schema.sql'
    
    if not schema_file.exists():
        print(f"❌ Error: No se encontró el archivo {schema_file}")
        return False
    
    print(f"📄 Leyendo archivo: {schema_file}")
    with open(schema_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Dividir en sentencias individuales
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    
    print(f"📊 Se encontraron {len(statements)} sentencias SQL")
    
    try:
        # Conectar a la base de datos
        print("\n🔌 Conectando a MySQL...")
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'seronoser'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print(f"✅ Conectado a la base de datos '{os.getenv('DB_NAME', 'seronoser')}'")
        
        cursor = connection.cursor()
        
        # Ejecutar cada sentencia
        print("\n🚀 Ejecutando sentencias SQL...\n")
        for i, statement in enumerate(statements, 1):
            if statement:
                try:
                    cursor.execute(statement)
                    
                    # Mostrar progreso
                    if 'CREATE TABLE' in statement.upper():
                        table_name = statement.split('`')[1] if '`' in statement else 'desconocida'
                        print(f"  ✓ [{i}/{len(statements)}] Tabla creada: {table_name}")
                    elif 'DROP TABLE' in statement.upper():
                        table_name = statement.split('`')[1] if '`' in statement else 'desconocida'
                        print(f"  ✓ [{i}/{len(statements)}] Tabla eliminada: {table_name}")
                    elif 'INSERT INTO' in statement.upper():
                        table_name = statement.split('`')[1] if '`' in statement else 'desconocida'
                        print(f"  ✓ [{i}/{len(statements)}] Datos insertados en: {table_name}")
                    else:
                        print(f"  ✓ [{i}/{len(statements)}] Sentencia ejecutada")
                        
                except pymysql.Error as e:
                    print(f"  ⚠️  [{i}/{len(statements)}] Advertencia: {e}")
                    # Continuar con la siguiente sentencia
        
        # Confirmar cambios
        connection.commit()
        
        print("\n" + "="*60)
        print("✅ ¡Schema ejecutado exitosamente!")
        print("="*60)
        
        # Verificar tablas creadas
        print("\n📋 Verificando tablas creadas:")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        key = f'Tables_in_{os.getenv("DB_NAME", "seronoser")}'
        for table in tables:
            table_name = table[key]
            cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
            count = cursor.fetchone()['count']
            print(f"  ✓ {table_name}: {count} registros")
        
        cursor.close()
        connection.close()
        
        print("\n✨ Base de datos lista para e-commerce")
        return True
        
    except pymysql.Error as e:
        print(f"\n❌ Error de base de datos: {e}")
        print("\n💡 Sugerencias:")
        print("   - Verifica que MySQL esté corriendo")
        print("   - Verifica las credenciales en el archivo .env")
        print("   - Asegúrate de que la base de datos 'seronoser' exista")
        return False
    
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🎭 INSTALADOR DE SCHEMA E-COMMERCE")
    print("   Base de datos: Ser o No Ser")
    print("="*60)
    
    exito = ejecutar_schema()
    
    if exito:
        print("\n🎉 Ahora puedes:")
        print("   1. Iniciar el servidor Flask (python app/app.py)")
        print("   2. Registrarte en /registro")
        print("   3. Comprar entradas en /index o /estrenos")
        sys.exit(0)
    else:
        print("\n❌ La instalación falló. Revisa los errores arriba.")
        sys.exit(1)
