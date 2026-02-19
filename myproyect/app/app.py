from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datauser import *  # Importamos la base de datos Json
from controller_db import *  # Importamos la base de datos MySQL
from models import (User, obtener_obras, crear_orden, obtener_ordenes_usuario,
                    crear_token_recuperacion, validar_token_recuperacion, resetear_password)
from dotenv import load_dotenv
from datetime import datetime
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-change-me')

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(int(user_id))

# Manejadores de errores
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

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
    title = "Quienes Somos"
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
            # En producción, aquí enviarías un email
            # Por ahora, mostramos el link en consola
            reset_url = f"{request.url_root}resetear-password/{token}"
            print("\n" + "="*80)
            print("🔑 LINK DE RECUPERACIÓN DE CONTRASEÑA")
            print("="*80)
            print(f"\nEmail: {email}")
            print(f"Link: {reset_url}")
            print(f"\nEste link expira en 1 hora")
            print("="*80 + "\n")
            
            flash('Si el email está registrado, recibirás un link de recuperación. Revisa la consola del servidor.', 'success')
        else:
            # No revelar si el email existe o no por seguridad
            flash('Si el email está registrado, recibirás un link de recuperación. Revisa la consola del servidor.', 'success')
        
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


if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') == 'development')
    