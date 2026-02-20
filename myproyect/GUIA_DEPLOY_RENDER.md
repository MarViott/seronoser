# Guía de Despliegue en Render

Esta guía te ayudará a desplegar tu aplicación Flask de teatro en **Render con PostgreSQL gratis permanente**.

## ¿Por qué Render?

✅ **PostgreSQL gratis** (permanente)  
✅ **Hosting Flask gratis** (permanente)  
✅ **Todo en un solo lugar**  
✅ **SSL automático**  
✅ **Despliegue automático desde GitHub**

## Requisitos Previos

1. **Cuenta en Render**: Crea una cuenta gratuita en [render.com](https://render.com)
2. **Cuenta de Gmail**: Para envío de emails (configurar contraseña de aplicación)
3. **Repositorio Git**: Tu código debe estar en GitHub, GitLab o Bitbucket

## Paso 1: Preparar Gmail para Envío de Emails

Para usar Gmail SMTP necesitas:

1. **Habilitar verificación en 2 pasos** en tu cuenta de Gmail:
   - Ve a [myaccount.google.com/security](https://myaccount.google.com/security)
   - Activa la verificación en 2 pasos

2. **Crear una contraseña de aplicación**:
   - Ve a [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Selecciona "Correo" y "Otro (nombre personalizado)"
   - Escribe "Teatro App" y genera la contraseña
   - **Guarda esta contraseña de 16 caracteres** (la necesitarás como `MAIL_PASSWORD`)

## Paso 2: Subir el Código a GitHub

1. Asegúrate de que tu archivo `.env` esté en `.gitignore`
2. Confirma que todos los cambios estén guardados
3. Sube tu código a GitHub:
   ```bash
   git add .
   git commit -m "Preparar para deploy en Render con PostgreSQL"
   git push origin main
   ```

## Paso 3: Crear la Base de Datos PostgreSQL en Render

1. **Inicia sesión en Render**: Ve a [dashboard.render.com](https://dashboard.render.com)

2. **Crear PostgreSQL Database**:
   - Click en "New +" → "PostgreSQL"
   - **Name**: `teatro-db` (o el nombre que prefieras)
   - **Database**: `teatro_ecommerce`
   - **User**: `teatro_user`
   - **Region**: Selecciona la más cercana (ej: Ohio para Latinoamérica)
   - **PostgreSQL Version**: Deja la predeterminada
   - **Plan**: Selecciona **"Free"** ✅ (Gratis permanente)
   - Click en "Create Database"

3. **Espera a que se  cree** (tarda 1-2 minutos)

4. **Ejecutar el Schema**:
   - Una vez creada, ve a la pestaña "Shell" de tu base de datos
   - Copia y pega el contenido de `sql/postgresql_schema.sql`
   - O usa un cliente PostgreSQL con las credenciales que Render te proporciona

## Paso 4: Crear el Web Service (Aplicación Flask)

1. **Inicia sesión en Render**: Ve a [dashboard.render.com](https://dashboard.render.com)

2. **Crear nuevo Web Service**:
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio de GitHub
   - Selecciona el repositorio de tu proyecto

3. **Configuración del servicio**:
   - **Name**: `teatro-app` (o el nombre que prefieras)
   - **Region**: Selecciona la más cercana
   - **Branch**: `main` (o tu rama principal)
   - **Root Directory**: `myproyect`
   - **Runtime**: `Python 3`

1. **En el Dashboard de Render**, click en "New +" → "Web Service"

2. **Conectar repositorio**:
   - Conecta tu cuenta de GitHub
   - Selecciona el repositorio de tu proyecto
   - Click en "Connect"

3. **Configuración del servicio**:
   - **Name**: `teatro-app` (o el nombre que prefieras)
   - **Region**: La misma que elegiste para la base de datos
   - **Branch**: `main` (o tu rama principal)
   - **Root Directory**: `myproyect`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r app/requirements.txt`
   - **Start Command**: `cd app && gunicorn app:app`
   - **Plan**: Selecciona **"Free"** ✅ (Gratis permanente)

4. **Antes de crear**, ve a "Advanced" y configura las variables de entorno

## Paso 5: Configurar Variables de Entorno

En la sección "Environment" (antes de crear el servicio), agrega estas variables:

### Variables Obligatorias:

1. **SECRET_KEY**: Genera una clave secreta
   ```python
   # En tu computadora, ejecuta:
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
   Copia el resultado y úsalo como valor

2. **FLASK_ENV**: `production`

3. **Configuración de Email (Gmail)**:
   - `MAIL_SERVER`: `smtp.gmail.com`
   - `MAIL_PORT`: `587`
   - `MAIL_USE_TLS`: `True`
   - `MAIL_USE_SSL`: `False`
   - `MAIL_USERNAME`: `tu-email@gmail.com`
   - `MAIL_PASSWORD`: La contraseña de aplicación que generaste en el Paso 1
   - `MAIL_DEFAULT_SENDER`: `tu-email@gmail.com` (el mismo email)

4. **Configuración de Base de Datos**:
   - Ve a tu base de datos `teatro-db` en Render
   - Copia las credenciales de conexión:
     - `DB_HOST`: El hostname interno (ej: `dpg-xxxxx-a`)
     - `DB_USER`: `teatro_user`
     - `DB_PASSWORD`: La contraseña generada por Render
     - `DB_NAME`: `teatro_ecommerce`
     - `DB_PORT`: `5432`

   **Tip**: También puedes usar `DATABASE_URL` pero nuestra app usa variables separadas.

## Paso 6: Deploy

1. Click en **"Create Web Service"**
2. Render comenzará a:
   - Clonar tu repositorio
   - Instalar dependencias (`pip install`)
   - Iniciar la aplicación con Gunicorn
3. El primer deploy toma **3-5 minutos**
4. Una vez completado, verás el estado  "Live" en verde
5. Tu URL será algo como: `https://teatro-app.onrender.com`

## Paso 7: Cargar los Datos Iniciales

1. **Ve a tu base de datos** `teatro-db` en Render
2. Click en "**Shell**" en la parte superior
3. **Ejecuta el schema** (copia y pega el archivo `sql/postgresql_schema.sql`)
   - Esto creará todas las tablas
   - Insertará las obras de ejemplo

**Alternativa**: Usar un cliente PostgreSQL externo:
   - Descarga las credenciales desde Render
   - Usa pgAdmin, DBeaver o TablePlus
   - Conecta y ejecuta el schema

## Paso 8: Verificar el Despliegue

1. **Prueba la página principal**: 
   - Ve a tu URL: `https://teatro-app.onrender.com`
   - Deberías ver la página de inicio

2. **Prueba el registro**:
   - Ve a `/registro`
   - Crea una nueva cuenta
   - Verifica que funcione

3. **Prueba recuperación de contraseña**:
   - Ve a `/recuperar-password`
   - Ingresa tu email
   - Verifica que llegue el email de recuperación
   - Sigue el enlace y resetea la contraseña
   - Inicia sesión con la nueva contraseña

4. **Prueba el dashboard** (si tienes rol de administrador):
   - Actualiza el rol de tu usuario desde la base de datos
   - Ve a `/dashboard`
   - Prueba crear/editar obras

## Solución de Problemas

### Error de Conexión a Base de Datos

```
psycopg2.OperationalError: could not connect to server
```

**Solución**:
**Solución**:
- Verifica que las credenciales de la base de datos sean correctas
- Asegúrate de usar el **hostname interno** (empieza con `dpg-`)
- El puerto debe ser `5432` (no 3306 que es de MySQL)
- Revisa los logs en Render: Dashboard → tu servicio → Logs

### Emails no se envían

```
SMTPAuthenticationError: (535, ...)
```

**Solución**:
- Verifica que uses la **contraseña de aplicación** de Gmail (16 caracteres sin espacios)
- NO uses tu contraseña normal de Gmail
- Asegúrate de que la verificación en 2 pasos esté activa
- El email en `MAIL_USERNAME` y `MAIL_DEFAULT_SENDER` debe ser el mismo

### La aplicación no inicia

```
ModuleNotFoundError: No module named 'psycopg2'
```

**Solución**:
- Verifica que `requirements.txt` incluya `psycopg2-binary==2.9.9`
- Asegúrate de que el `Build Command` sea correcto: `pip install -r app/requirements.txt`
- Revisa que la ruta sea `app/requirements.txt` (dentro de la carpeta app)

### App se queda "Building" por mucho tiempo

**Solución**:
- Espera pacientemente (el primer deploy puede tomar 5-10 minutos)
- Revisa los logs en tiempo real para ver qué está haciendo
- Si falla después de 15 minutos, revisa los logs de error

### Las imágenes de las obras no se ven

**Solución**:
- Las imágenes deben estar en `app/static/img/obras/`
- Render mantiene archivos estáticos solo si están en el repositorio Git
- Asegúrate de que las imágenes estén en Git (no en `.gitignore`)

## Actualizar la Aplicación

Cada vez que hagas cambios en tu código:

1. **Haz commit y push a GitHub**:
   ```bash
   git add .
   git commit -m "Descripción de cambios"
   git push origin main
   ```

2. **Render detecta automáticamente** los cambios y vuelve a desplegar
3. El re-deploy toma **2-3 minutos**
4. Tu app se reiniciará automáticamente

**Nota**: Los cambios son automáticos. NO necesitas hacer nada manual en Render.

## Actualizar el Schema de la Base de Datos

Si necesitas agregar tablas o cambiar el esquema:

1. **Modifica** `sql/postgresql_schema.sql`
2. **Conecta a tu base de datos** en Render (Shell o cliente externo)
3. **Ejecuta** los comandos SQL nuevos
4. **NO ejecutes el schema completo** otra vez si ya tienes datos (perderás información)

Para cambios seguros:
```sql
-- Ejemplo: Agregar una columna
ALTER TABLE obras ADD COLUMN genero VARCHAR(50);

-- Ejemplo: Crear una nueva tabla
CREATE TABLE IF NOT EXISTS comentarios (
    id SERIAL PRIMARY KEY,
    obra_id INT REFERENCES obras(id),
    usuario_id INT REFERENCES usuarios_auth(id),
    comentario TEXT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Monitoreo y Logs

### Ver Logs en Tiempo Real

1. Ve a tu servicio en Render
2. Click en "**Logs**" en el menú superior
3. Verás los logs de tu aplicación en tiempo real

### Errores Comunes en Logs

```python
Error al conectar con la base de datos: ...
```
→ Problema con credenciales de PostgreSQL

```python
SMTPAuthenticationError
```
→ Problema con configuración de Gmail

```python
ModuleNotFoundError
```
→ Falta una dependencia en `requirements.txt`

## Plan Gratuito: Limitaciones y Consejos

### Limitaciones del Plan Free:

1. **La app se duerme después de 15 minutos de inactividad**
   - Primer acceso después de dormirse: 30-60 segundos de espera (cold start)
   - Solución: Usar un servicio de "ping" como UptimeRobot (opcional)

2. **750 horas/mes de tiempo activo**
   - Equivale a ~25 horas por día
   - Más que suficiente para desarrollo/pruebas

3. **PostgreSQL Free**: 
   - 256 MB de RAM
   - 1 GB de almacenamiento
   - 90 días de retención de backups
   - Suficiente para miles de registros

### Consejos para el Plan Free:

- **Optimiza consultas**: Usa índices, limita resultados
- **Limpia datos antiguos**: No acumules millones de registros
- **Comprime imágenes**: Reduce el tamaño de archivos estáticos
- **Considera upgrade** si necesitas app 24/7 activa ($7/mes)

## Backup de la Base de Datos

### Backup Manual:

1. Ve a tu base de datos en Render
2. Click en "**Backups**"
3. Click en "**Create Backup**"
4. Render guardará un snapshot de tu base de datos (gratuito, 90 días de retención)

### Backup Programático:

```bash
# Descarga el backup usando pg_dump
pg_dump -h <hostname> -U <user> -d <database> > backup.sql

# Restaurar desde backup
psql -h <hostname> -U <user> -d <database> < backup.sql
```

## Configurar Dominio Personalizado

Si quieres usar tu propio dominio (ej: `teatro.midominio.com`):

1. Ve a tu servicio en Render
2. Click en "**Settings**"
3. En "**Custom Domain**", agrega tu dominio
4. Sigue las instrucciones para configurar los DNS
5. Render te da un SSL gratis automáticamente

## Recursos Adicionales

- **Documentación de Render**: [render.com/docs](https://render.com/docs)
- **Flask en Render**: [render.com/docs/deploy-flask](https://render.com/docs/deploy-flask)
- **PostgreSQL en Render**: [render.com/docs/databases](https://render.com/docs/databases)
- **Troubleshooting**: [render.com/docs/troubleshooting-deploys](https://render.com/docs/troubleshooting-deploys)
- **Community**: [community.render.com](https://community.render.com)

## Costos y Upgrade

### Plan Free (Actual):
- ✅ Gratis permanente
- ✅ PostgreSQL incluido  
- ⚠️  App se duerme (cold starts)
- ⚠️  750 horas/mes

### Plan Starter ($7/mes por servicio):
- ✅ App siempre activa (sin cold starts)
- ✅ Respuesta inmediata
- ✅ Mejor para producción
- ✅ Más recursos (512 MB RAM)

### Cuándo hacer upgrade:

- Cuando necesites la app disponible 24/7
- Cuando los cold starts molesten a tus usuarios
- Cuando superes los límites del plan free

## Notas Importantes

1. **No incluyas `.env`**: Asegúrate de que esté en `.gitignore`
2. **Credenciales seguras**: Nunca hagas commit de contraseñas
3. **SSL automático**: Render proporciona HTTPS gratis
4. **Backups regulares**: Haz backups de tu base de datos mensualmente
5. **Monitoreo**: Revisa logs periódicamente
6. **Actualizaciones**: Mantén dependencias actualizadas

## Checklist Final

Antes de considerar el deploy completo, verifica:

- [ ] La app carga correctamente en la URL de Render
- [ ] Puedes registrar nuevos usuarios
- [ ] El login funciona
- [ ] Puedes recuperar contraseña (llega el email)
- [ ] Las obras se muestran correctamente
- [ ] Las imágenes se ven
- [ ] El dashboard funciona (si tienes rol de admin)
- [ ] Puedes crear/editar ¡obras
- [ ] Las compras se registran
- [ ] Los logs no muestran errores críticos

---

## ¿Necesitas Ayuda?

- **Logs**: Siempre revisa los logs primero
- **Documentation**: [render.com/docs](https://render.com/docs)
- **Community**: [community.render.com](https://community.render.com)
- **Support**: Render tiene soporte por email en planes pagos

¡Tu aplicación de teatro ya está en la nube! 🎭🚀---

¿Necesitas ayuda? Revisa los logs en Render o consulta la documentación oficial.
