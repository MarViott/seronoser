# 🔑 PASOS PARA CONFIGURAR RECUPERACIÓN DE CONTRASEÑA

## ✅ Estado Actual

**Base de datos**: ✅ Ya está creada (tabla `password_reset_tokens`)  
**Formspree**: ❌ NO es necesario (solo para formularios estáticos HTML)  
**Flask-Mail**: ✅ Ya instalado  
**Problema**: ⚠️ No configuraste las credenciales SMTP en `.env`

---

## 🚀 SOLUCIÓN RÁPIDA (5 minutos)

### Paso 1: Obtener Contraseña de Aplicación de Gmail

1. Abre: https://myaccount.google.com/security
2. Busca **"Verificación en dos pasos"** → Actívala si no está activa
3. Vuelve a Seguridad y busca **"Contraseñas de aplicaciones"**
4. Haz clic en **"Contraseñas de aplicaciones"**
5. Selecciona:
   - App: **Correo**
   - Dispositivo: **Otro** (pon: "Ser o No Ser")
6. Haz clic en **Generar**
7. Google mostrará algo como: `abcd efgh ijkl mnop`
8. **Cópiala** (sin espacios): `abcdefghijklmnop`

### Paso 2: Configurar .env

Abre el archivo: `app/.env`

Busca estas líneas:

```bash
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-de-aplicacion
```

Reemplaza con:

```bash
MAIL_USERNAME=marisaviotti@gmail.com
MAIL_PASSWORD=abcdefghijklmnop
```

(Usa tu contraseña de aplicación real, esa es solo un ejemplo)

También cambia:

```bash
MAIL_DEFAULT_SENDER=marisaviotti@gmail.com
```

### Paso 3: Guardar y Cerrar

Guarda el archivo `.env`

### Paso 4: Probar Configuración (OPCIONAL pero recomendado)

```bash
cd app
python probar_email.py
```

Te pedirá un email de prueba. Ingresa tu email y presiona Enter.

Si funciona, verás: ✅ ¡EMAIL ENVIADO EXITOSAMENTE!

### Paso 5: Iniciar el Servidor

```bash
cd app
python app.py
```

---

## 🧪 Probar Recuperación de Contraseña

1. Ve a: http://127.0.0.1:5000/recuperar-password
2. Ingresa: `marisaviotti@gmail.com`
3. Haz clic en **"Enviar link de recuperación"**
4. Revisa tu bandeja de entrada (puede tardar 10-30 segundos)
5. **Si no aparece**, revisa **SPAM** o **Promociones**
6. Haz clic en el botón **"Restablecer Contraseña"** del email
7. Ingresa tu nueva contraseña
8. ¡Listo! Ya puedes iniciar sesión con la nueva contraseña

---

## 🐛 Si No Llega el Email

### Opción A: Revisar Consola del Servidor

Si hay un error de configuración SMTP, el sistema automáticamente:
- Imprime el link en la **consola** del servidor Flask
- Puedes copiar ese link y pegarlo en tu navegador

Busca en la consola algo como:

```
🔑 LINK DE RECUPERACIÓN DE CONTRASEÑA (Error al enviar email)
================================================================================
Email: marisaviotti@gmail.com
Link: http://127.0.0.1:5000/resetear-password/abc123...
```

### Opción B: Verificar Configuración

Ejecuta:

```bash
cd app
python probar_email.py
```

Te dirá exactamente qué está mal.

---

## ❓ Preguntas Frecuentes

### ¿Por qué no usar Formspree?

Formspree es para **formularios de contacto** en sitios web estáticos (HTML puro).

**NO sirve para**:
- Recuperación de contraseñas ❌
- Envío programático de emails ❌
- Sistemas dinámicos con Flask ❌

**SÍ sirve para**:
- Formulario "Contáctanos" en páginas estáticas ✅
- Landing pages sin backend ✅

### ¿La base de datos ya está creada?

**SÍ**, la tabla `password_reset_tokens` ya fue creada. Solo falta configurar el **envío de emails**.

### ¿Es seguro poner mi contraseña en .env?

**SÍ**, siempre que:
1. Uses una **contraseña de aplicación** (no tu contraseña real de Gmail)
2. NO subas `.env` a GitHub (ya está en `.gitignore`)
3. La contraseña de aplicación se puede **revocar** en cualquier momento

### ¿Qué pasa si no configuro el email?

El sistema seguirá funcionando, pero:
- El link de recuperación solo aparecerá en la **consola del servidor**
- Los usuarios no recibirán emails
- Tendrás que copiar manualmente el link y enviárselos

---

## 📚 Documentación Completa

- **Configuración detallada**: `sql/README_EMAIL.md`
- **Archivo de ejemplo**: `app/.env.example`
- **Script de prueba**: `app/probar_email.py`

---

## 🎯 Resumen en 3 Pasos

1. **Obtener contraseña de aplicación de Gmail** (https://myaccount.google.com/apppasswords)
2. **Editar `app/.env`** con tu email y contraseña de aplicación
3. **Reiniciar servidor**: `python app.py`

¡Listo! Los emails deberían llegar ahora. 📧✨
