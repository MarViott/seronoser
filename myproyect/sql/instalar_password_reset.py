#!/usr/bin/env python3
"""
Script para agregar la tabla de tokens de recuperación de contraseña
"""
import sys
import os
from pathlib import Path

# Agregar el directorio app al path
sys.path.insert(0, str(Path(__file__).parent.parent / 'app'))

from dotenv import load_dotenv
import pymysql

# Cargar variables de entorno
load_dotenv(Path(__file__).parent.parent / 'app' / '.env')

def crear_tabla_reset_tokens():
    """Crea la tabla password_reset_tokens"""
    
    print("="*60)
    print("🔑 INSTALADOR TABLA PASSWORD RESET")
    print("="*60)
    
    try:
        # Conectar a la base de datos
        print("\n🔌 Conectando a MySQL...")
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '3306')),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'seronoser'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print(f"✅ Conectado a '{os.getenv('DB_NAME', 'seronoser')}'")
        
        cursor = connection.cursor()
        
        # Leer el archivo SQL
        schema_file = Path(__file__).parent / 'password_reset_table.sql'
        
        print(f"\n📄 Leyendo: {schema_file.name}")
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Ejecutar
        print("🚀 Creando tabla password_reset_tokens...")
        cursor.execute(sql_content)
        connection.commit()
        
        print("✅ Tabla creada exitosamente")
        
        # Verificar
        cursor.execute("SHOW TABLES LIKE 'password_reset_tokens'")
        if cursor.fetchone():
            print("\n✨ Verificación: tabla 'password_reset_tokens' existe")
        
        cursor.close()
        connection.close()
        
        print("\n" + "="*60)
        print("✅ INSTALACIÓN COMPLETADA")
        print("="*60)
        print("\n🎉 Sistema de recuperación de contraseña listo")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exito = crear_tabla_reset_tokens()
    sys.exit(0 if exito else 1)
