"""
Script automático para probar SMTP sin input del usuario
"""
from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'False') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

print("="*80)
print("📧 DIAGNÓSTICO DE CONFIGURACIÓN SMTP")
print("="*80)
print(f"\n✓ Servidor: {app.config['MAIL_SERVER']}")
print(f"✓ Puerto: {app.config['MAIL_PORT']}")
print(f"✓ TLS: {app.config['MAIL_USE_TLS']}")
print(f"✓ SSL: {app.config['MAIL_USE_SSL']}")
print(f"✓ Username: {app.config['MAIL_USERNAME']}")
print(f"✓ Password: {'*' * len(app.config['MAIL_PASSWORD']) if app.config['MAIL_PASSWORD'] else '❌ VACÍA'}")
print(f"✓ Sender: {app.config['MAIL_DEFAULT_SENDER']}")

if not app.config['MAIL_USERNAME']:
    print("\n❌ ERROR: MAIL_USERNAME está vacío")
    exit(1)

if not app.config['MAIL_PASSWORD']:
    print("\n❌ ERROR: MAIL_PASSWORD está vacío")
    exit(1)

print(f"\n🚀 Enviando email de prueba a {app.config['MAIL_USERNAME']}...")

try:
    with app.app_context():
        msg = Message(
            subject="✅ Test SMTP - Ser o No Ser",
            recipients=[app.config['MAIL_USERNAME']],
            body="Si recibes este email, la configuración SMTP funciona correctamente."
        )
        mail.send(msg)
    
    print("\n✅ ¡EMAIL ENVIADO EXITOSAMENTE!")
    print(f"✓ Revisa tu bandeja: {app.config['MAIL_USERNAME']}")
    print("✓ Si no aparece, revisa SPAM")
    print("="*80)
    
except Exception as e:
    print("\n❌ ERROR AL ENVIAR EMAIL:")
    print(f"\nTipo de error: {type(e).__name__}")
    print(f"Mensaje: {str(e)}")
    
    error_msg = str(e).lower()
    
    print("\n💡 DIAGNÓSTICO:")
    if "username and password not accepted" in error_msg or "authentication failed" in error_msg:
        print("   • La contraseña es incorrecta o no es una contraseña de aplicación")
        print("   • Soluciones:")
        print("     1. Ve a https://myaccount.google.com/apppasswords")
        print("     2. Genera una NUEVA contraseña de aplicación")
        print("     3. Cópiala SIN espacios en .env")
        print("     4. Asegúrate de tener verificación en 2 pasos activa")
    
    elif "smtp auth" in error_msg:
        print("   • Gmail bloqueó el acceso")
        print("   • Usa una contraseña de aplicación en lugar de tu contraseña normal")
    
    elif "connection" in error_msg or "timeout" in error_msg:
        print("   • No se puede conectar al servidor SMTP")
        print("   • Verifica tu conexión a internet")
        print("   • El firewall puede estar bloqueando el puerto 587")
    
    elif "ssl" in error_msg or "tls" in error_msg:
        print("   • Problema con SSL/TLS")
        print("   • Intenta cambiar el puerto a 465 y usar SSL")
    
    else:
        print("   • Error desconocido")
        print("   • Lee el mensaje de error arriba para más detalles")
    
    print("\n📚 Documentación completa: sql/README_EMAIL.md")
    print("="*80)
    exit(1)
