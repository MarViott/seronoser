# Guía de Despliegue en Render

Esta guía te ayudará a desplegar tu aplicación Flask de teatro en Render.

## Requisitos Previos

1. **Cuenta en Render**: Crea una cuenta gratuita en [render.com](https://render.com)
2. **Base de datos MySQL**: Necesitarás una base de datos MySQL accesible desde internet. Opciones:
   - [PlanetScale](https://planetscale.com/) (gratuito)
   - [Railway](https://railway.app/) (MySQL incluido)
   - [FreeMySQLHosting](https://www.freemysqlhosting.net/) (gratuito)
3. **Repositorio Git**: Tu código debe estar en GitHub, GitLab o Bitbucket

## Paso 1: Preparar la Base de Datos

### Opción A: Usar PlanetScale (Recomendado)

1. Crea una cuenta en [PlanetScale](https://planetscale.com/)
2. Crea una nueva base de datos
3. Obtén las credenciales de conexión (host, usuario, password, nombre de base de datos)
4. Ejecuta el schema SQL:
   ```bash
   # Descarga el schema desde tu proyecto
   mysql -h <host> -u <user> -p<password> <database> < sql/ecommerce_schema.sql
   ```

### Opción B: Usar Railway

1. Crea una cuenta en [Railway](https://railway.app/)
2. Crea un nuevo proyecto y agrega MySQL
3. Obtén las credenciales desde el panel de Railway
4. Ejecuta el schema SQL usando un cliente MySQL

## Paso 2: Configurar Gmail para Envío de Emails

Para usar Gmail SMTP necesitas:

1. **Habilitar verificación en 2 pasos** en tu cuenta de Gmail
2. **Crear una contraseña de aplicación**:
   - Ve a tu cuenta de Google → Seguridad
   - Busca "Contraseñas de aplicaciones"
   - Genera una nueva contraseña para "Correo"
   - Guarda esta contraseña (la necesitarás como `MAIL_PASSWORD`)

## Paso 3: Subir el Código a GitHub

1. Asegúrate de que tu archivo `.env` esté en `.gitignore`
2. Sube tu código a GitHub:
   ```bash
   git add .
   git commit -m "Preparar para deploy en Render"
   git push origin main
   ```

## Paso 4: Crear el Servicio en Render

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
   - **Build Command**: `pip install -r app/requirements.txt`
   - **Start Command**: `cd app && gunicorn app:app`

4. **Plan**: Selecciona "Free" para comenzar

## Paso 5: Configurar Variables de Entorno

En la sección "Environment" de tu servicio en Render, agrega las siguientes variables:

### Variables Obligatorias:

```
SECRET_KEY=genera-una-clave-secreta-aleatoria-aqui
FLASK_ENV=production

# Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
MAIL_DEFAULT_SENDER=tu-email@gmail.com

# Base de datos
DB_HOST=tu-host-mysql
DB_USER=tu-usuario
DB_PASSWORD=tu-password
DB_NAME=ecommerce
DB_PORT=3306
```

### Generar SECRET_KEY

Puedes generar una clave secreta segura con Python:
```python
import secrets
print(secrets.token_hex(32))
```

## Paso 6: Deploy

1. Click en "Create Web Service"
2. Render comenzará a construir y desplegar tu aplicación
3. El proceso tomará algunos minutos
4. Una vez completado, recibirás una URL como: `https://teatro-app.onrender.com`

## Paso 7: Verificar el Despliegue

1. **Prueba la página principal**: Ve a tu URL de Render
2. **Prueba el login**: Intenta iniciar sesión
3. **Prueba recuperación de contraseña**:
   - Ve a `/recuperar-password`
   - Ingresa un email registrado
   - Verifica que llegue el email
   - Sigue el enlace y resetea la contraseña

## Solución de Problemas

### Error de Conexión a Base de Datos

- Verifica que las credenciales sean correctas
- Asegúrate de que tu base de datos permita conexiones desde cualquier IP
- Revisa los logs en Render: Dashboard → tu servicio → Logs

### Emails no se envían

- Verifica que uses la contraseña de aplicación de Gmail (no tu contraseña normal)
- Asegúrate de que la verificación en 2 pasos esté activa
- Revisa los logs para ver errores específicos

### La aplicación no inicia

- Revisa los logs en Render
- Verifica que todas las variables de entorno estén configuradas
- Asegúrate de que el `requirements.txt` incluya todas las dependencias

## Actualizar la Aplicación

Cada vez que hagas cambios en tu código:

1. Haz commit y push a GitHub:
   ```bash
   git add .
   git commit -m "Descripción de cambios"
   git push origin main
   ```

2. Render detectará los cambios automáticamente y volverá a desplegar

## Monitoreo

- **Logs**: Ve a tu servicio en Render → Logs para ver los registros en tiempo real
- **Métricas**: Render muestra uso de CPU y memoria
- **Health Checks**: Render verifica automáticamente que tu app esté funcionando

## Costos

- **Plan Free**: 
  - 750 horas/mes de tiempo de ejecución
  - La app se duerme después de 15 minutos de inactividad
  - Primer inicio puede ser lento (cold start)
  
- **Plan Starter ($7/mes)**:
  - App siempre activa
  - Sin cold starts
  - Mejor para producción

## Recursos Adicionales

- [Documentación de Render](https://render.com/docs)
- [Guía de Flask en Render](https://render.com/docs/deploy-flask)
- [Troubleshooting](https://render.com/docs/troubleshooting-deploys)

## Notas Importantes

1. **No incluyas archivos sensibles**: Asegúrate de que `.env` esté en `.gitignore`
2. **Backups**: Haz backups regulares de tu base de datos
3. **SSL**: Render proporciona SSL/HTTPS automáticamente
4. **Dominio personalizado**: Puedes configurar un dominio propio en los ajustes del servicio

---

¿Necesitas ayuda? Revisa los logs en Render o consulta la documentación oficial.
