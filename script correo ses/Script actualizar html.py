import boto3
import json
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from botocore.exceptions import ClientError

# Claves (Boto3) 
AWS_ACCESS_KEY = "Ejemplo"
AWS_SECRET_KEY = "Ejemplo"

# Configuración SMTP 
SMTP_SERVER = "email-smtp.us-east-2.amazonaws.com"
PORT = 587
USER_SMTP = "Ejemplo"
PASSWORD_SMTP = "Ejemplo".strip()

REMITENTE = "no-reply@ejemplo.com"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def conectar_ses(region):
    return boto3.client(
        'ses', 
        region_name=region,
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )

def enviar_prueba_email(html_content, subject, email_destino):
    """Envía un correo real para ver el diseño a un destinatario específico"""
    print(f"\n Preparando envío de prueba para: {email_destino}...")
    msg = MIMEMultipart()
    msg["From"] = REMITENTE
    msg["To"] = email_destino
    msg["Subject"] = f"[TEST] {subject}"
    msg.attach(MIMEText(html_content, "html"))

    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP(SMTP_SERVER, PORT)
        server.starttls(context=context)
        server.login(USER_SMTP, PASSWORD_SMTP)
        server.sendmail(REMITENTE, email_destino, msg.as_string())
        server.quit()
        print(f" ¡Correo de prueba enviado con éxito a {email_destino}!")
    except Exception as e:
        print(f" Error en envío SMTP: {e}")

def borrar_plantilla():
    """Borrado seguro de plantillas"""
    print("\n--- MODO BORRADO SEGURO ---")
    nombre_borrar = input("Escriba el nombre EXACTO de la plantilla a eliminar: ")
    
    print("\n1. Virginia (us-east-1) | 2. Ohio (us-east-2)")
    reg = "us-east-1" if input("Seleccione región: ") == "1" else "us-east-2"
    
    confirmar = input(f"\n¿Seguro que quieres borrar '{nombre_borrar}'? Escribe 'SI' para confirmar: ")
    
    if confirmar == "SI":
        ses = conectar_ses(reg)
        try:
            ses.delete_template(TemplateName=nombre_borrar)
            print(f"Plantilla '{nombre_borrar}' eliminada correctamente de {reg}.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'TemplateDoesNotExist':
                print(f"Error: La plantilla '{nombre_borrar}' no existe en {reg}.")
            else:
                print(f"Error inesperado: {e}")
    else:
        print("Borrado cancelado. No has escrito 'SI' correctamente.")

def subir_actualizar():
    """Sube un HTML nuevo o actualiza uno existente"""
    print("\n--- MODO SUBIR / ACTUALIZAR ---")
    nombre_html = input("Archivo HTML (ej: index.html): ")
    nombre_plantilla = input("Nombre de la plantilla en AWS: ")
    asunto = input("Asunto (Subject): ")
    
    print("\n1. Virginia (us-east-1) | 2. Ohio (us-east-2)")
    reg = "us-east-1" if input("Seleccione región: ") == "1" else "us-east-2"
    
    html_path = os.path.join(BASE_DIR, nombre_html)

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        ses = conectar_ses(reg)
        template_data = {
            'TemplateName': nombre_plantilla,
            'SubjectPart': asunto,
            'HtmlPart': html_content,
            'TextPart': 'Favor de visualizar en HTML.'
        }

        try:
            ses.update_template(Template=template_data)
            print(f"\n Plantilla '{nombre_plantilla}' ACTUALIZADA en {reg}.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'TemplateDoesNotExist':
                ses.create_template(Template=template_data)
                print(f"\n Plantilla '{nombre_plantilla}' CREADA como nueva en {reg}.")
            else:
                raise e

        # Lógica de envio
        prueba = input("\n¿Desea enviar un correo de prueba ahora? (s/n): ")
        if prueba.lower() == 's':
            email_input = input("Ingrese el correo destino (o presione ENTER para CANCELAR): ").strip()
            
            if email_input:
                enviar_prueba_email(html_content, asunto, email_input)
            else:
                print("No se ingresó correo. Envío de prueba cancelado.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_html}' en la carpeta.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        print("\n==============================")
        print("      AWS SES MASTER TOOL")
        print("==============================")
        print("1. Subir o Actualizar Plantilla")
        print("2. Borrar Plantilla")
        print("3. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "1":
            subir_actualizar()
        elif opcion == "2":
            borrar_plantilla()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")