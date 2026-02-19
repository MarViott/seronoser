from flask import Flask, render_template, request, redirect, flash, url_for
from datauser import *  # Importamos la base de datos Json
from controller_db import *  # Importamos la base de datos MySQL
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key-change-me')

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
    return render_template('index.html', title=title)

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
    return render_template('estrenos.html', title=title)

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

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_ENV') == 'development')
    