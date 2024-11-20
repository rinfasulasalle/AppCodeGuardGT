from email.message import EmailMessage
import smtplib

class SmtpSenderEmail:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=465):
        """
        Inicializa la clase con la configuración del servidor SMTP.
        :param smtp_server: Dirección del servidor SMTP (por defecto Gmail)
        :param smtp_port: Puerto del servidor SMTP (por defecto 465)
        """
        self.remitente = "codeguardbot@gmail.com"  # Remitente fijo
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, destinatario, mensaje, archivo_ruta):
        """
        Envía el correo con el archivo adjunto.
        :param destinatario: Dirección de correo del destinatario
        :param mensaje: Contenido del mensaje
        :param archivo_ruta: Ruta del archivo a adjuntar (.pdf o .md)
        """
        # Crear el mensaje de correo
        email = EmailMessage()
        email['From'] = self.remitente
        email['To'] = destinatario
        email['Subject'] = 'REPORTE DE PLAGIO GENERADO CON IA GEMINI'
        email.set_content(mensaje)

        # Adjuntar el archivo
        try:
            with open(archivo_ruta, "rb") as archivo:
                contenido_archivo = archivo.read()
                tipo_archivo = 'pdf' if archivo_ruta.endswith('.pdf') else 'markdown'
                email.add_attachment(
                    contenido_archivo,
                    maintype='application',
                    subtype=tipo_archivo,
                    filename=archivo_ruta.split('/')[-1]  # Nombre del archivo
                )
        except FileNotFoundError:
            print(f"Error: El archivo {archivo_ruta} no se encuentra.")
            return False

        # Enviar el correo
        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
                smtp.login(self.remitente, 'ertw usvy gmoi cxdq')  # Cambia por tu app password real
                smtp.sendmail(self.remitente, destinatario, email.as_string())
                print("Correo enviado correctamente.")
                return True
        except smtplib.SMTPException as e:
            print(f"Error al enviar el correo: {e}")
            return False
 