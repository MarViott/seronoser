import psycopg2

# Cadena de conexión de Render
connection_string = "postgresql://teatro_user:kcHLipl6VFODTowYlR7iJkq4eKv1HmWZ@dpg-d6cbhsp5pdvs738tsjr0-a.oregon-postgres.render.com/teatro_ecommerce"

try:
    # Conectar a la base de datos
    print("Conectando a la base de datos...")
    conn = psycopg2.connect(connection_string)
    cursor = conn.cursor()
    
    # Leer el archivo SQL
    print("Leyendo schema SQL...")
    with open('sql/postgresql_schema.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    # Ejecutar el schema
    print("Ejecutando schema...")
    cursor.execute(sql)
    conn.commit()
    
    print("✅ Schema ejecutado exitosamente!")
    print("✅ Tablas creadas: usuarios_auth, obras, ordenes, orden_detalles, password_reset_tokens, usuarios")
    print("✅ Datos de ejemplo insertados")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
