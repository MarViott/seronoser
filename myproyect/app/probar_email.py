"""
Script de prueba para verificar la configuración SMTP
Ejecuta este script para probar si el envío de emails funciona
"""

from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configurar Flask y Mail
app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

def probar_email():
    """Enviar un email de prueba"""
    
    print("\n" + "="*80)
    print("📧 PRUEBA DE CONFIGURACIÓN SMTP")
    print("="*80)
    
    # Verificar configuración
    print("\n📝 Configuración actual:")
    print(f"   Servidor: {app.config['MAIL_SERVER']}")
    print(f"   Puerto: {app.config['MAIL_PORT']}")
    print(f"   TLS: {app.config['MAIL_USE_TLS']}")
    print(f"   Usuario: {app.config['MAIL_USERNAME']}")
    print(f"   Sender: {app.config['MAIL_DEFAULT_SENDER']}")
    
    # Verificar que tenemos lo necesario
    if not app.config['MAIL_USERNAME']:
        print("\n❌ ERROR: MAIL_USERNAME no está configurado en .env")
        return False
    
    if not app.config['MAIL_PASSWORD']:
        print("\n❌ ERROR: MAIL_PASSWORD no está configurado en .env")
        return False
    
    # Solicitar email de destino
    print("\n" + "-"*80)
    email_destino = input("Ingresa el email donde quieres recibir la prueba: ").strip()
    
    if not email_destino:
        print("❌ Email inválido")
        return False
    
    print(f"\n🚀 Enviando email de prueba a {email_destino}...")
    
    try:
        with app.app_context():
            msg = Message(
                subject="🎭 Prueba de Email - Ser o No Ser",
                recipients=[email_destino],
                html="""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                  color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                        .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                        .success { background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0; }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>🎭 Ser o No Ser</h1>
                            <h2>Email de Prueba</h2>
                        </div>
                        <div class="content">
                            <div class="success">
                                <strong>✅ ¡Éxito!</strong> Tu configuración SMTP funciona correctamente.
                            </div>
                            <p>Este es un email de prueba para verificar que el sistema de correo electrónico está configurado correctamente.</p>
                            <p>Si estás viendo este mensaje, significa que:</p>
                            <ul>
                                <li>✅ Flask-Mail está instalado</li>
                                <li>✅ Las credenciales SMTP son correctas</li>
                                <li>✅ El servidor SMTP está accesible</li>
                                <li>✅ Los emails se pueden enviar sin problemas</li>
                            </ul>
                            <p>Ya puedes usar la función de <strong>recuperación de contraseña</strong> con confianza.</p>
                        </div>
                    </div>
                </body>
                </html>
                """
            )
            mail.send(msg)
        
        print("\n✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
        print("\n📬 Revisa tu bandeja de entrada:")
        print(f"   - Email: {email_destino}")
        print("   - Si no aparece, revisa SPAM o Promociones")
        print("   - Puede tardar unos segundos en llegar")
        print("\n" + "="*80)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR AL ENVIAR EMAIL:")
        print(f"\n{str(e)}")
        print("\n💡 Soluciones posibles:")
        print("   1. Verifica que usas una CONTRASEÑA DE APLICACIÓN de Gmail")
        print("   2. Revisa que MAIL_USERNAME y MAIL_PASSWORD están en .env")
        print("   3. Asegúrate de tener verificación en dos pasos activa en Gmail")
        print("   4. Copia la contraseña SIN espacios en .env")
        print("\n📚 Documentación: sql/README_EMAIL.md")
        print("="*80)
        return False

if __name__ == "__main__":
    probar_email()
