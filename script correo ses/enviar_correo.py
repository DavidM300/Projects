import boto3
import json
from botocore.exceptions import ClientError

def enviar():
    # Usamos la región de Ohio donde está tu plantilla
    ses = boto3.client('ses', region_name='us-east-2')

    try:
        response = ses.send_templated_email(
            Source='no-reply@mobilesmart.city',
            Destination={
                'ToAddresses': ['dmartinezr@mobilesmart.city']
            },
            Template='ARGUS_Notification',
            # AQUÍ ESTABA EL FALLO: Usamos "email_message" que es lo que pide tu HTML
            TemplateData=json.dumps({
                "email_message": "¡Hola Daniel! Esta es la prueba definitiva con la variable correcta de la plantilla."
            })
        )
        print(f"✅ ¡MENSAJE ENVIADO!")
        print(f"ID: {response['MessageId']}")
        print("Revisa tu bandeja de entrada ahora.")

    except ClientError as e:
        print(f"❌ Error de AWS SES: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    enviar()
