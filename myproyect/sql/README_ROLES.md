# Sistema de Roles para Dashboard

## 📋 Migración de Base de Datos

Se ha agregado un sistema de roles para controlar el acceso al dashboard administrativo.

### Ejecutar Migración SQL

**IMPORTANTE**: Debes ejecutar el script `agregar_roles.sql` en tu base de datos MySQL antes de usar estas funcionalidades.

#### Opción 1: MySQL Workbench
1. Abre MySQL Workbench
2. Conecta a tu base de datos (puerto 3307)
3. Abre el archivo `sql/agregar_roles.sql`
4. Ejecuta el script (botón ⚡ o Ctrl+Shift+Enter)

#### Opción 2: phpMyAdmin
1. Abre phpMyAdmin
2. Selecciona tu base de datos
3. Ve a la pestaña "SQL"
4. Copia y pega el contenido de `sql/agregar_roles.sql`
5. Haz clic en "Continuar"

#### Opción 3: Línea de comandos
```bash
mysql -u root -h 127.0.0.1 -P 3307 -p ser_o_no_ser < sql/agregar_roles.sql
```

## 🔐 Roles Disponibles

El sistema tiene 3 roles:

### 1. **Usuario** (por defecto)
- Puede navegar el sitio
- Puede comprar entradas
- Ver sus compras
- **NO puede** acceder al dashboard

### 2. **Editor**
- Todo lo de Usuario +
- **Acceso completo al Dashboard**
- Crear, editar, eliminar y gestionar obras
- Cambiar estado de obras (Estreno/Cartelera)

### 3. **Administrador**
- Todo lo de Editor +
- Máximos privilegios
- **Acceso completo al Dashboard**
- Gestión completa del sistema

## 🚀 Asignar Roles a Usuarios

Después de ejecutar la migración, todos los usuarios existentes tendrán rol `usuario` por defecto.

### Hacer Administrador a un Usuario

```sql
-- Por ID de usuario
UPDATE usuarios_auth SET rol = 'administrador' WHERE id = 1;

-- Por email
UPDATE usuarios_auth SET rol = 'administrador' WHERE email = 'tu-email@example.com';
```

### Hacer Editor a Varios Usuarios

```sql
UPDATE usuarios_auth SET rol = 'editor' WHERE id IN (2, 3, 4);
```

### Ver Roles de Usuarios

```sql
SELECT id, nombre, apellido, email, rol FROM usuarios_auth;
```

## 🛡️ Funcionamiento del Sistema

### Decorador `@rol_requerido`

Todas las rutas del dashboard están protegidas con el decorador:

```python
@app.route('/dashboard')
@login_required
@rol_requerido('administrador', 'editor')
def dashboard():
    # Solo accesible para administradores y editores
```

### En el Header

El enlace al Dashboard solo se muestra si el usuario tiene rol apropiado:

```django
{% if current_user.puede_editar() %}
  <a href="/dashboard">Dashboard</a>
{% endif %}
```

### Métodos del Modelo User

```python
# Verificar si tiene alguno de los roles
current_user.tiene_rol('administrador', 'editor')

# Verificar si es administrador
current_user.es_admin()

# Verificar si es editor
current_user.es_editor()

# Verificar si puede editar (admin o editor)
current_user.puede_editar()
```

## 🔒 Protección de Rutas

Si un usuario sin permisos intenta acceder al dashboard:

1. Si **no está logueado**: Redirige a `/login`
2. Si **no tiene rol**: Muestra página de error 403 (Acceso Denegado)

## 📝 Registro de Nuevos Usuarios

Por defecto, todos los nuevos usuarios se registran con rol `usuario`.

Para cambiar esto, edita el formulario de registro en `app.py`:

```python
# Para hacer administrador automáticamente
User.create(..., rol='administrador')

# Para hacer editor automáticamente
User.create(..., rol='editor')
```

## ✅ Verificación

1. Ejecuta la migración SQL
2. Asigna rol a tu usuario:
   ```sql
   UPDATE usuarios_auth SET rol = 'administrador' WHERE email = 'tu-email@example.com';
   ```
3. Reinicia el servidor Flask
4. Inicia sesión
5. Verás el enlace "Dashboard" en el header
6. Accede a `/dashboard`

## 🚨 Solución de Problemas

### Error: "Unknown column 'rol'"
- No ejecutaste la migración SQL
- Ejecuta `sql/agregar_roles.sql`

### No veo el enlace al Dashboard
- Verifica tu rol:
  ```sql
  SELECT rol FROM usuarios_auth WHERE email = 'tu-email@example.com';
  ```
- Debe ser `administrador` o `editor`

### Error 403 al acceder al Dashboard
- Tu usuario tiene rol `usuario`
- Necesitas actualizar el rol a `administrador` o `editor`

## 🔄 Cambios en el Código

### Archivos Modificados:
- `app/models.py` - Agregado campo `rol` al modelo User
- `app/app.py` - Agregado decorador `@rol_requerido`
- `app/templates/defaults/header.html` - Condicional para mostrar Dashboard
- `app/templates/403.html` - Nueva página de error 403

### Archivos Nuevos:
- `sql/agregar_roles.sql` - Script de migración
- `sql/README_ROLES.md` - Esta documentación
