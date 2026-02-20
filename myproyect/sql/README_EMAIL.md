# Configuración de Envío de Emails

## 📧 Sistema de Recuperación de Contraseña

El sistema ahora envía **emails reales** para la recuperación de contraseñas usando **Flask-Mail** con SMTP.

## 🚀 Configuración Rápida (Gmail)

### Paso 1: Instalar Flask-Mail

```bash
cd app
pip install -r requirements.txt
```

Esto instalará `Flask-Mail==0.9.1`

### Paso 2: Obtener Contraseña de Aplicación de Gmail

**IMPORTANTE**: No uses tu contraseña normal de Gmail. Necesitas una **contraseña de aplicación**.

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. En el menú izquierdo, selecciona **Seguridad**
3. Busca **"Verificación en dos pasos"** y actívala si no está activa
4. Una vez activada, busca **"Contraseñas de aplicaciones"**
5. Genera una nueva contraseña de aplicación:
   - Selecciona app: **Correo**
   - Selecciona dispositivo: **Otro (nombre personalizado)**
   - Escribe: "Ser o No Ser Teatro"
   - Haz clic en **Generar**
6. Google te mostrará una contraseña de 16 caracteres (ej: `abcd efgh ijkl mnop`)
7. Cópiala (sin espacios)

### Paso 3: Configurar .env

Edita el archivo `app/.env` y reemplaza estos valores:

```bash
# Email Configuration (SMTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=marisaviotti@gmail.com  # Tu email de Gmail
MAIL_PASSWORD=abcdefghijklmnop        # La contraseña de aplicación (SIN espacios)
MAIL_DEFAULT_SENDER=marisaviotti@gmail.com
```

### Paso 4: Reiniciar el Servidor

```bash
cd app
python app.py
```

## ✅ Probar la Recuperación de Contraseña

1. Ve a http://127.0.0.1:5000/recuperar-password
2. Ingresa tu email registrado
3. Haz clic en "Enviar link de recuperación"
4. **Revisa tu bandeja de entrada** (puede tardar unos segundos)
5. Si no aparece, revisa **SPAM** o **Promociones**
6. Haz clic en el enlace del email
7. Ingresa tu nueva contraseña

## 🔧 Otros Proveedores de Email

### Outlook/Hotmail

```bash
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@outlook.com
MAIL_PASSWORD=tu-contraseña
```

### Yahoo Mail

```bash
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@yahoo.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
```

### SendGrid (Recomendado para producción)

```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=tu-api-key-de-sendgrid
```

## 🐛 Solución de Problemas

### Error: "Username and Password not accepted"

**Causa**: Contraseña incorrecta o no es una contraseña de aplicación

**Solución**:
- Verifica que usas una **contraseña de aplicación**, no tu contraseña normal
- Copia la contraseña SIN espacios en `.env`
- Asegúrate de tener activada la verificación en dos pasos en Gmail

### Error: "SMTPAuthenticationError"

**Causa**: Gmail bloqueó el acceso

**Solución**:
1. Ve a https://myaccount.google.com/lesssecureapps
2. Activa "Permitir aplicaciones menos seguras" (solo si no usas contraseña de aplicación)
3. **MEJOR**: Usa contraseña de aplicación en lugar de activar esta opción

### No llega el email

**Posibles causas**:

1. **Revisa SPAM**: Gmail puede enviar el email a spam la primera vez
2. **Email mal escrito**: Verifica que el email esté registrado correctamente
3. **Servidor SMTP caído**: Intenta más tarde
4. **Firewall**: Puede estar bloqueando el puerto 587

**Debug**:
- Revisa la **consola del servidor** Flask
- Si hay error, aparecerá el link ahí como respaldo
- El link también se imprime en consola si falla el envío

### Error: "SMTP server connection lost"

```bash
# Cambia a puerto 465 con SSL
MAIL_PORT=465
MAIL_USE_TLS=False
MAIL_USE_SSL=True
```

## 📝 Formato del Email

El email que se envía incluye:

- ✉️ Asunto: "Recuperación de Contraseña - Ser o No Ser"
- 🎨 HTML con diseño profesional
- 🔗 Botón para restablecer contraseña
- ⏱️ Enlace alternativo (por si el botón no funciona)
- ⚠️ Advertencia: el link expira en 1 hora
- 🔒 Nota de seguridad

## 🔐 Seguridad

- ✅ Token único de 32 caracteres
- ✅ Expira en 1 hora
- ✅ Un solo uso (se marca como usado)
- ✅ No revela si el email existe o no
- ✅ Contraseñas hasheadas con bcrypt

## 📊 Flujo Completo

```
Usuario olvida contraseña
    ↓
Ingresa email en /recuperar-password
    ↓
Sistema genera token único
    ↓
Guarda token en base de datos
    ↓
Envía email con link: /resetear-password/{token}
    ↓
Usuario hace clic en el link
    ↓
Sistema verifica token (válido y no expirado)
    ↓
Usuario ingresa nueva contraseña
    ↓
Sistema actualiza contraseña y marca token como usado
    ↓
Redirige a login
```

## 🚫 Formspree NO es necesario

**Formspree** es para formularios de contacto estáticos (HTML puro), no para:
- Envío programático de emails
- Recuperación de contraseñas
- Confirmaciones de registro
- Notificaciones automáticas

Para esto, usamos **Flask-Mail** con SMTP.

## 💡 Consejos de Producción

1. **Usa SendGrid o Mailgun**: Mejor deliverability que Gmail
2. **Configura SPF/DKIM**: Para evitar que los emails caigan en spam
3. **Monitorea envíos**: Usa servicios con analytics
4. **Rate limiting**: Limita intentos de recuperación por IP
5. **Templates mejorados**: Usa plantillas Jinja2 para emails

## 📞 Soporte

Si necesitas ayuda:
1. Revisa los **logs de la consola** del servidor Flask
2. Verifica las **variables de entorno** en `.env`
3. Prueba con **otro email** para descartar problemas con el proveedor
