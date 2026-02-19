# Instrucciones para Configurar E-Commerce

## Paso 1: Aplicar el Schema de Base de Datos

Necesitas ejecutar el archivo `ecommerce_schema.sql` en tu base de datos MySQL. Hay varias formas de hacerlo:

### Opción A: Usando MySQL Workbench (Recomendado)
1. Abre MySQL Workbench
2. Conéctate a tu servidor local (localhost)
3. Haz clic en `File` → `Open SQL Script`
4. Selecciona el archivo `ecommerce_schema.sql`
5. Asegúrate de que la base de datos `seronoser` esté seleccionada
6. Haz clic en el icono del rayo ⚡ para ejecutar todo el script

### Opción B: Usando phpMyAdmin
1. Abre phpMyAdmin en tu navegador
2. Selecciona la base de datos `seronoser` en el panel izquierdo
3. Ve a la pestaña `SQL`
4. Copia y pega el contenido del archivo `ecommerce_schema.sql`
5. Haz clic en `Ejecutar` o `Go`

### Opción C: Usando línea de comandos MySQL
Si tienes MySQL en el PATH de Windows:
```bash
mysql -u root -p seronoser < sql/ecommerce_schema.sql
```

## Paso 2: Verificar las Tablas Creadas

Después de ejecutar el script, verifica que se crearon estas tablas:
- `usuarios_auth` - Usuarios registrados con autenticación
- `obras` - Catálogo de obras de teatro
- `ordenes` - Órdenes de compra
- `orden_detalles` - Detalles de cada orden

El script también insertará 6 obras de ejemplo (Hamlet, Un tranvía llamado deseo, Muerte de un viajante, etc.)

## Paso 3: Configurar Variables de Entorno

Asegúrate de que tu archivo `.env` esté configurado correctamente:

```env
# Database Configuration
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_contraseña_aqui
DB_NAME=seronoser

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=clave-secreta-aleatoria-larga-para-produccion
```

**Importante:** Cambia `SECRET_KEY` por una clave aleatoria única. Puedes generarla con Python:
```python
import secrets
print(secrets.token_hex(32))
```

## Paso 4: Reiniciar el Servidor Flask

Si el servidor Flask está corriendo, reinícialo para que cargue los nuevos cambios:
1. Detén el servidor (Ctrl+C en la terminal)
2. Ejecuta de nuevo: `python app/app.py`

## Flujo de E-Commerce Implementado

### Para Usuarios:
1. **Registro**: `/registro` - Crear cuenta nueva
2. **Login**: `/login` - Iniciar sesión
3. **Explorar**: `/index` o `/estrenos` - Ver cartelera
4. **Comprar**: Click en "Comprar Entradas" (requiere estar logueado)
5. **Checkout**: Seleccionar cantidad y fecha de función
6. **Mis Compras**: `/mis-compras` - Ver historial de órdenes

### Nuevas Rutas Disponibles:
- `GET /login` - Formulario de inicio de sesión
- `POST /login` - Procesar login
- `GET /registro` - Formulario de registro
- `POST /registro` - Procesar registro
- `GET /logout` - Cerrar sesión
- `GET /comprar/<obra_id>` - Página de checkout (requiere login)
- `POST /procesar-compra` - Procesar la compra
- `GET /mis-compras` - Ver historial de compras (requiere login)

## Características Implementadas

✅ **Autenticación de Usuarios**
- Registro con hash de contraseñas (werkzeug.security)
- Login con sesión persistente (Flask-Login)
- Protección de rutas con `@login_required`

✅ **Carrito de Compras**
- Selección de cantidad (1-10 entradas)
- Selección de fecha de función
- Cálculo automático de totales

✅ **Historial de Órdenes**
- Vista de compras realizadas
- Detalles de cada orden
- Estado de la orden (pendiente, confirmada, cancelada)

✅ **Seguridad**
- Contraseñas hasheadas (no se guardan en texto plano)
- Variables sensibles en archivo .env
- Validación de formularios en cliente y servidor

## Datos de Prueba

El schema incluye 6 obras de ejemplo:
1. **Hamlet** - William Shakespeare ($15,000)
2. **Un tranvía llamado deseo** - Tennessee Williams ($12,000)
3. **Muerte de un viajante** - Arthur Miller ($13,500)
4. **Acompañamiento** - Carlos Gorostiza ($10,000)
5. **Mi hijo el doctor** - Florencio Sánchez ($9,500)
6. **El campeón de la muerte** - Roberto Arlt ($11,000)

## Solución de Problemas

### Error: "No module named 'flask_login'"
```bash
pip install Flask-Login==0.6.3
```

### Error: "Table 'usuarios_auth' doesn't exist"
Ejecuta el archivo `ecommerce_schema.sql` siguiendo el Paso 1

### Error de Conexión a Base de Datos
Verifica que:
- El servidor MySQL esté corriendo
- Las credenciales en `.env` sean correctas
- La base de datos `seronoser` exista

### Las imágenes no se muestran
Las obras de ejemplo esperan las siguientes imágenes en `app/static/img/`:
- hamlet.jpg
- tranvia.jpg
- viajante.jpg
- acompanamiento.jpg
- miHijo.jpg
- campeon.jpg

Puedes agregar tus propias imágenes o modificar los nombres en la base de datos.
