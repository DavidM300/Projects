import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- DATOS EXACTOS DE TUS CAPTURAS ---
SMTP_SERVER = "email-smtp.us-east-2.amazonaws.com"
PORT = 587
# Tu SMTP user name de la imagen
USER_SMTP = "AKIAQFPED56WRHEADD3Y" 
# Tu SMTP password de la imagen (la limpiamos de posibles espacios al pegar)
PASSWORD_SMTP = "BEmHNR45TrSVwDx8FIo/1TZRzUaPmIqMWxigxhS2eDHC".strip()

REMITENTE = "no-reply@mobilesmart.city"
DESTINATARIO = "dmartinezr@mobilesmart.city"

def probar_conexion_pango():
    print(f"Conectando a {SMTP_SERVER}...")
    
    # Creamos el mensaje
    msg = MIMEMultipart()
    msg["From"] = REMITENTE
    msg["To"] = DESTINATARIO
    msg["Subject"] = "Validación SMTP Pango"
    msg.attach(MIMEText("Si recibes esto, las credenciales de la imagen funcionan.", "plain"))

    try:
        # Configuración de seguridad obligatoria para AWS
        context = ssl.create_default_context()
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls(context=context) # Inicia cifrado
        
        print("Intentando login con las claves de la imagen...")
        server.login(USER_SMTP, PASSWORD_SMTP)
        
        print("Enviando correo de prueba...")
        server.sendmail(REMITENTE, DESTINATARIO, msg.as_string())
        server.quit()
        
        print("✅ ¡ÉXITO! Las credenciales son válidas para Pango.")
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Error 535: Las credenciales son incorrectas.")
        print("Nota: Asegúrate de que esa contraseña se generó en la sección 'SMTP Settings' de SES y no en IAM directamente.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    probar_conexion_pango()