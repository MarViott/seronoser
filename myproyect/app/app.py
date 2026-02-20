from flask import Flask, render_template, request, redirect, flash, url_for, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from functools import wraps
from datauser import *  # Importamos la base de datos Json
from controller_db import *  # Importamos la base de datos MySQL
from models import (User, obtener_obras, obtener_obra_por_id, crear_orden, obtener_ordenes_usuario,
                    crear_token_recuperacion, validar_token_recuperacion, resetear_password,
                    contar_obras, obtener_obras_paginadas, crear_obra, actualizar_obra, 
                    eliminar_obra, alternar_estreno)
from dotenv import load_dotenv
from datetime import datetime
import os
import math

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-change-me')

# Configuración de subida de archivos
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'img', 'obras')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear carpeta de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuración de Flask-Mail (SMTP)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

# Decorador para verificar roles
def rol_requerido(*roles):
    """
    Decorador para restringir acceso basado en roles de usuario.
    Uso: @rol_requerido('administrador', 'editor')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debes iniciar sesión para acceder a esta página', 'warning')
                return redirect(url_for('login'))
            
            if not current_user.tiene_rol(*roles):
                flash('No tienes permisos para acceder a esta página', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Manejadores de errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Ruta principal
@app.route('/')
def home():
    return redirect('/index')

@app.route('/index')
def dataindex():
    title = "Cartelera"
    obras = obtener_obras(solo_estrenos=False)
    return render_template('index.html', title=title, obras=obras)

@app.route('/contacto')
def datacontacto():
    title = "Contacto"
    return render_template('contacto.html', title=title)

@app.route('/persona')
def datapersona():
    usuarios = obtener_usuarios()
    title = "Persona"
    return render_template('persona.html', title=title, usuarios=usuarios)

@app.route('/criticas')
def datacriticas():
    title = "Criticas"
    return render_template('criticas.html', title=title)

@app.route('/estrenos')
def dataestrenos():
    title = "Estrenos"
    estrenos = obtener_obras(solo_estrenos=True)
    return render_template('estrenos.html', title=title, obras=estrenos)

@app.route('/quienes-somos')
def dataquienesSomos():
    title = "Sobre mí"
    return render_template('quienes-somos.html', title=title)

@app.route('/comunidad')
def dataComunidad():
    usuarios = obtener_usuarios()
    title = "Comunidad"    
    return render_template('comunidad.html', title=title, usuarios=usuarios)

# insert
# 1) cargar el form
@app.route("/comunidad/cargar_usuario")
def insertComunidad():
    title = "Nuevo Usuario"
    return render_template("form_guardar_usuario.html", title=title)

# 2) enviar los datos del form, por POST
@app.route("/comunidad/guardar_nuevo_usuario", methods=['POST'])
def newUser_Comunidad():
    try:
        nombre_user = request.form.get('nombre', '').strip()
        email_user = request.form.get('email', '').strip()
        ocupacion_user = request.form.get('ocupacion', '').strip()
        
        if not nombre_user or not email_user or not ocupacion_user:
            flash('Todos los campos son obligatorios', 'error')
            return redirect("/comunidad/cargar_usuario")
        
        if cargar_nuevo_usuario(nombre_user, email_user, ocupacion_user):
            flash('Usuario creado exitosamente', 'success')
        else:
            flash('Error al crear usuario', 'error')
            
    except Exception as e:
        print(f"Error en newUser_Comunidad: {e}")
        flash('Error al procesar la solicitud', 'error')
    
    return redirect("/comunidad")
    
# update
@app.route("/comunidad/editar_usuario/<int:id>")
def editar_usuario(id):
    try:
        title = "Editar Usuario"
        usuario = obtener_usuario_por_id(id)
        
        if not usuario:
            flash('Usuario no encontrado', 'error')
            return redirect("/comunidad")
        
        # Si db.py está configurado con DictCursor, usuario es un dict
        # Si no, es una tupla
        return render_template("form_editar_usuario.html", title=title, usuario=usuario)
    except Exception as e:
        print(f"Error en editar_usuario: {e}")
        flash('Error al cargar usuario', 'error')
        return redirect("/comunidad")

@app.route("/comunidad/update_usuario", methods=['POST'])
def update_usuario():
    try:
        id_edit = request.form.get('id')
        nombre_edit = request.form.get('nombre', '').strip()
        email_edit = request.form.get('email', '').strip()
        ocupacion_edit = request.form.get('ocupacion', '').strip()
        
        if not all([id_edit, nombre_edit, email_edit, ocupacion_edit]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect(f"/comunidad/editar_usuario/{id_edit}")
        
        if actualizar_usuario(nombre_edit, email_edit, ocupacion_edit, id_edit):
            flash('Usuario actualizado exitosamente', 'success')
        else:
            flash('Error al actualizar usuario', 'error')
            
    except Exception as e:
        print(f"Error en update_usuario: {e}")
        flash('Error al procesar la solicitud', 'error')
    
    return redirect("/comunidad")

# delete
@app.route('/comunidad/borrar_usuario/<int:id>')
def delete_usuario(id):
    try:
        if eliminar_usuario(id):
            flash('Usuario eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar usuario', 'error')
    except Exception as e:
        print(f"Error en delete_usuario: {e}")
        flash('Error al procesar la solicitud', 'error')
    
    return redirect("/comunidad")
# ===== RUTAS DE AUTENTICACIÓN =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('Email y contraseña son obligatorios', 'error')
            return redirect('/login')
        
        user = User.get_by_email(email)
        
        if user and user.verify_password(password):
            login_user(user, remember=remember)
            flash(f'Bienvenido/a {user.nombre}!', 'success')
            
            # Redirigir a la página solicitada o a index
            next_page = request.args.get('next')
            return redirect(next_page if next_page else '/index')
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    title = "Iniciar Sesión"
    return render_template('login.html', title=title)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect('/index')
    
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        email = request.form.get('email', '').strip()
        telefono = request.form.get('telefono', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validaciones
        if not all([nombre, apellido, email, password, password_confirm]):
            flash('Todos los campos son obligatorios', 'error')
            return redirect('/registro')
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'error')
            return redirect('/registro')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return redirect('/registro')
        
        # Verificar si el email ya existe
        if User.get_by_email(email):
            flash('Este email ya está registrado', 'error')
            return redirect('/registro')
        
        # Crear usuario (orden correcto: nombre, apellido, email, password, telefono)
        user = User.create(nombre, apellido, email, password, telefono)
        
        if user:
            login_user(user)
            flash(f'Registro exitoso! Bienvenido/a {nombre}!', 'success')
            return redirect('/index')
        else:
            flash('Error al crear la cuenta. Intenta nuevamente', 'error')
    
    title = "Registro"
    return render_template('registro.html', title=title)

@app.route('/logout')
@login_required
def logout():
    nombre = current_user.nombre
    logout_user()
    flash(f'Hasta pronto, {nombre}!', 'success')
    return redirect('/index')

# ===== RUTAS DE RECUPERACIÓN DE CONTRASEÑA =====
@app.route('/recuperar-password', methods=['GET', 'POST'])
def recuperar_password():
    if current_user.is_authenticated:
        return redirect('/index')
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('El email es obligatorio', 'error')
            return redirect('/recuperar-password')
        
        # Crear token (siempre mostramos mensaje de éxito por seguridad)
        token = crear_token_recuperacion(email)
        
        if token:
            reset_url = f"{request.url_root}resetear-password/{token}"
            
            # Intentar enviar email
            try:
                msg = Message(
                    subject="Recuperación de Contraseña - Ser o No Ser",
                    recipients=[email],
                    html=f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                      color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                            .button {{ display: inline-block; padding: 15px 30px; background: #667eea; 
                                     color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
                            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h1>🎭 Ser o No Ser</h1>
                                <h2>Recuperación de Contraseña</h2>
                            </div>
                            <div class="content">
                                <p>Hola,</p>
                                <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta.</p>
                                <p>Haz clic en el siguiente botón para crear una nueva contraseña:</p>
                                <center>
                                    <a href="{reset_url}" class="button">Restablecer Contraseña</a>
                                </center>
                                <p>O copia y pega este enlace en tu navegador:</p>
                                <p style="background: #e9ecef; padding: 10px; border-radius: 5px; word-break: break-all;">
                                    {reset_url}
                                </p>
                                <div class="warning">
                                    <strong>⚠️ Importante:</strong> Este enlace expira en <strong>1 hora</strong>.
                                </div>
                                <p>Si no solicitaste este cambio, puedes ignorar este email de forma segura.</p>
                            </div>
                            <div class="footer">
                                <p>© 2026 Ser o No Ser - Teatro en Vivo</p>
                                <p>Este es un correo automático, por favor no respondas a este mensaje.</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                )
                mail.send(msg)
                flash('Te hemos enviado un email con instrucciones para recuperar tu contraseña.', 'success')
            except Exception as e:
                print(f"Error al enviar email: {e}")
                # Si falla el email, mostrar el link en consola como respaldo
                print("\n" + "="*80)
                print("🔑 LINK DE RECUPERACIÓN DE CONTRASEÑA (Error al enviar email)")
                print("="*80)
                print(f"\nEmail: {email}")
                print(f"Link: {reset_url}")
                print(f"\nEste link expira en 1 hora")
                print(f"\nError: {e}")
                print("="*80 + "\n")
                flash('Hubo un problema al enviar el email. Verifica la configuración SMTP en .env', 'warning')
        else:
            # No revelar si el email existe o no por seguridad
            flash('Si el email está registrado, recibirás instrucciones para recuperar tu contraseña.', 'success')
        
        return redirect('/login')
    
    title = "Recuperar Contraseña"
    return render_template('recuperar-password.html', title=title)

@app.route('/resetear-password/<token>', methods=['GET', 'POST'])
def resetear_password_view(token):
    if current_user.is_authenticated:
        return redirect('/index')
    
    # Validar token
    token_data = validar_token_recuperacion(token)
    
    if not token_data:
        flash('El link de recuperación es inválido o ha expirado', 'error')
        return redirect('/login')
    
    if request.method == 'POST':
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        if not password or not password_confirm:
            flash('Todos los campos son obligatorios', 'error')
            return redirect(f'/resetear-password/{token}')
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'error')
            return redirect(f'/resetear-password/{token}')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return redirect(f'/resetear-password/{token}')
        
        # Resetear contraseña
        if resetear_password(token, password):
            flash('¡Contraseña actualizada exitosamente! Ahora puedes iniciar sesión', 'success')
            return redirect('/login')
        else:
            flash('Error al actualizar la contraseña. Intenta nuevamente', 'error')
            return redirect(f'/resetear-password/{token}')
    
    title = "Nueva Contraseña"
    return render_template('resetear-password.html', title=title, token=token)

# ===== RUTAS DE E-COMMERCE =====
@app.route('/comprar/<int:obra_id>')
@login_required
def comprar(obra_id):
    obras = obtener_obras(solo_estrenos=False)
    obra = next((o for o in obras if o['id'] == obra_id), None)
    
    if not obra:
        flash('Obra no encontrada', 'error')
        return redirect('/index')
    
    title = f"Comprar - {obra['titulo']}"
    return render_template('comprar.html', title=title, obra=obra, now=datetime.now())

@app.route('/procesar-compra', methods=['POST'])
@login_required
def procesar_compra():
    try:
        obra_id = int(request.form.get('obra_id'))
        cantidad = int(request.form.get('cantidad'))
        fecha_funcion = request.form.get('fecha_funcion')
        
        if cantidad < 1 or cantidad > 10:
            flash('La cantidad debe estar entre 1 y 10', 'error')
            return redirect(f'/comprar/{obra_id}')
        
        # Obtener precio de la obra
        obras = obtener_obras(solo_estrenos=False)
        obra = next((o for o in obras if o['id'] == obra_id), None)
        
        if not obra:
            flash('Obra no encontrada', 'error')
            return redirect('/index')
        
        precio_total = obra['precio'] * cantidad
        
        # Crear orden
        orden_id = crear_orden(
            usuario_id=current_user.id,
            obra_id=obra_id,
            cantidad=cantidad,
            precio_unitario=obra['precio'],
            precio_total=precio_total,
            fecha_funcion=fecha_funcion
        )
        
        if orden_id:
            flash(f'¡Compra realizada con éxito! Número de orden: {orden_id}', 'success')
            return redirect('/mis-compras')
        else:
            flash('Error al procesar la compra. Intenta nuevamente', 'error')
            return redirect(f'/comprar/{obra_id}')
            
    except Exception as e:
        print(f"Error en procesar_compra: {e}")
        flash('Error al procesar la compra', 'error')
        return redirect('/index')

@app.route('/mis-compras')
@login_required
def mis_compras():
    title = "Mis Compras"
    ordenes = obtener_ordenes_usuario(current_user.id)
    return render_template('mis-compras.html', title=title, ordenes=ordenes)


# ========== DASHBOARD ADMINISTRATIVO ==========

def archivo_permitido(filename):
    """Verifica si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/dashboard')
@login_required
@rol_requerido('administrador', 'editor')
def dashboard():
    """Dashboard principal para gestión de obras"""
    title = "Dashboard - Gestión de Obras"
    
    # Obtener parámetros de paginación y filtro
    pagina = request.args.get('pagina', 1, type=int)
    filtro = request.args.get('filtro', None)  # None, 'estrenos', 'cartelera'
    por_pagina = 6
    
    # Obtener obras paginadas
    obras = obtener_obras_paginadas(pagina, por_pagina, filtro)
    total_obras = contar_obras(filtro)
    total_paginas = math.ceil(total_obras / por_pagina)
    
    return render_template('dashboard.html', 
                         title=title, 
                         obras=obras,
                         pagina_actual=pagina,
                         total_paginas=total_paginas,
                         filtro=filtro)


@app.route('/dashboard/nueva-obra', methods=['GET', 'POST'])
@login_required
@rol_requerido('administrador', 'editor')
def nueva_obra():
    """Crear nueva obra"""
    title = "Nueva Obra"
    
    if request.method == 'POST':
        try:
            # Procesar imagen
            imagen_nombre = None
            if 'imagen' in request.files:
                archivo = request.files['imagen']
                if archivo and archivo.filename and archivo_permitido(archivo.filename):
                    filename = secure_filename(archivo.filename)
                    # Agregar timestamp para evitar duplicados
                    nombre, ext = os.path.splitext(filename)
                    filename = f"{nombre}_{int(datetime.now().timestamp())}{ext}"
                    archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    imagen_nombre = filename
            
            # Crear obra
            obra_id = crear_obra(
                titulo=request.form.get('titulo'),
                autor=request.form.get('autor'),
                director=request.form.get('director'),
                descripcion=request.form.get('descripcion'),
                imagen=imagen_nombre,
                precio=float(request.form.get('precio', 0)),
                fecha_estreno=request.form.get('fecha_estreno') or None,
                teatro=request.form.get('teatro'),
                duracion=int(request.form.get('duracion', 0)) if request.form.get('duracion') else None,
                es_estreno=bool(request.form.get('es_estreno'))
            )
            
            flash(f'Obra "{request.form.get("titulo")}" creada exitosamente', 'success')
            return redirect('/dashboard')
            
        except Exception as e:
            print(f"Error al crear obra: {e}")
            flash('Error al crear la obra', 'error')
    
    return render_template('form-obra.html', title=title, obra=None)


@app.route('/dashboard/editar/<int:obra_id>', methods=['GET', 'POST'])
@login_required
@rol_requerido('administrador', 'editor')
def editar_obra(obra_id):
    """Editar obra existente"""
    obra = obtener_obra_por_id(obra_id)
    
    if not obra:
        flash('Obra no encontrada', 'error')
        return redirect('/dashboard')
    
    title = f"Editar: {obra['titulo']}"
    
    if request.method == 'POST':
        try:
            # Procesar nueva imagen si se subió
            imagen_nombre = obra['imagen']  # Mantener imagen actual por defecto
            if 'imagen' in request.files:
                archivo = request.files['imagen']
                if archivo and archivo.filename and archivo_permitido(archivo.filename):
                    # Eliminar imagen anterior si existe
                    if obra['imagen']:
                        ruta_anterior = os.path.join(app.config['UPLOAD_FOLDER'], obra['imagen'])
                        if os.path.exists(ruta_anterior):
                            os.remove(ruta_anterior)
                    
                    # Guardar nueva imagen
                    filename = secure_filename(archivo.filename)
                    nombre, ext = os.path.splitext(filename)
                    filename = f"{nombre}_{int(datetime.now().timestamp())}{ext}"
                    archivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    imagen_nombre = filename
            
            # Actualizar obra
            actualizar_obra(
                obra_id=obra_id,
                titulo=request.form.get('titulo'),
                autor=request.form.get('autor'),
                director=request.form.get('director'),
                descripcion=request.form.get('descripcion'),
                imagen=imagen_nombre,
                precio=float(request.form.get('precio', 0)),
                fecha_estreno=request.form.get('fecha_estreno') or None,
                teatro=request.form.get('teatro'),
                duracion=int(request.form.get('duracion', 0)) if request.form.get('duracion') else None,
                es_estreno=bool(request.form.get('es_estreno'))
            )
            
            flash(f'Obra "{request.form.get("titulo")}" actualizada exitosamente', 'success')
            return redirect('/dashboard')
            
        except Exception as e:
            print(f"Error al actualizar obra: {e}")
            flash('Error al actualizar la obra', 'error')
    
    return render_template('form-obra.html', title=title, obra=obra)


@app.route('/dashboard/eliminar/<int:obra_id>')
@login_required
@rol_requerido('administrador', 'editor')
def eliminar_obra_route(obra_id):
    """Eliminar obra (soft delete)"""
    try:
        obra = obtener_obra_por_id(obra_id)
        if obra:
            eliminar_obra(obra_id)
            flash(f'Obra "{obra["titulo"]}" eliminada exitosamente', 'success')
        else:
            flash('Obra no encontrada', 'error')
    except Exception as e:
        print(f"Error al eliminar obra: {e}")
        flash('Error al eliminar la obra', 'error')
    
    return redirect('/dashboard')


@app.route('/dashboard/alternar-estreno/<int:obra_id>')
@login_required
@rol_requerido('administrador', 'editor')
def alternar_estreno_route(obra_id):
    """Alternar estado de estreno de una obra"""
    try:
        obra = obtener_obra_por_id(obra_id)
        if obra:
            alternar_estreno(obra_id)
            nuevo_estado = "estreno" if not obra['es_estreno'] else "cartelera"
            flash(f'Obra "{obra["titulo"]}" movida a {nuevo_estado}', 'success')
        else:
            flash('Obra no encontrada', 'error')
    except Exception as e:
        print(f"Error al alternar estreno: {e}")
        flash('Error al cambiar estado de la obra', 'error')
    
    return redirect('/dashboard')


if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') == 'development')
    