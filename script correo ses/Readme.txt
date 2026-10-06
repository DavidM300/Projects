Este programa administra las plantillas de correo, (creación, actualización y borrado) e integra una comprobación inmediata vía SMTP para validar el renderizado del diseño en buzones de correo reales sin salir de la terminal.

-Características detecta automáticamente si una plantilla existe para actualizarla (`update_template`) o crearla desde cero (`create_template`) mediante la captura de excepciones de la API de AWS.
-Selección entre regiones de AWS (`us-east-1` en Virginia y `us-east-2` en Ohio).
-Envío opcional tras la subida para poder comprobar la compatibilidad del código HTML/CSS en clientes de correo reales, como Gmail, Outlook.
-Confirmación doble para así poder evitar las eliminaciones accidentales en los entornos de producción.
-Carga aislada de claves API y parámetros SMTP mediante variables de entorno (`python-dotenv`).

Tecnologías y Librerías

- Lenguaje: Python 3
- SDK de AWS: boto3 
- Networking & Correo:** `smtplib`, `ssl`, `email.mime`
