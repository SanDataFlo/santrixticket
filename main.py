from fastapi import FastAPI, Request, HTTPException
from fastapi.openapi.utils import get_openapi
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pydantic import BaseModel
from typing import List, Dict, Any


api_titel = "SanTrix REST Schnittstelle MVP 1.0"
api_version = "1.0"
api_summary = "REST API for WatsonAssistant"
server = "https://application-3e.1b7hlo69yoj4.eu-de.codeengine.appdomain.cloud/"


class Ticket(BaseModel):
    mail_address: str
    hardware: str
    hardware_brands: str
    tickettypID: int
    priority: str
    username: str
    telefonnummer: str
    session_history: List[Dict[str, Any]]


class Response(BaseModel):
    success: bool
    message: str


app = FastAPI()


@app.post("/create_ticket_mail/{request}", response_model=Response)
async def send_email(ticket:Ticket):
    data = await request.json()
    recipients = [data.get('mail_address')]
    subject = "SanTrix hat ein neues Ticket erstellt!"

    # Erstellen des Inhalts im futuristischen Stil
    body = """
        <!DOCTYPE html>
        <html lang="de">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>SanTrix hat ein neues Ticket erstellt!</title>
            <style>
                body {
                    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                    background-color: #1e1e1e;
                    color: #ffffff;
                    padding: 20px;
                    margin: 0;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    border-radius: 8px;
                    padding: 30px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    color: #29b6f6;
                    margin-bottom: 20px;
                    font-size: 24px;
                    font-weight: bold;
                    text-align: center;
                }
                p {
                    margin-bottom: 20px;
                    line-height: 1.6;
                    text-align: justify;
                }
                ul {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }
                li {
                    margin-bottom: 10px;
                }
                li strong {
                    font-weight: bold;
                    color: #4dd0e1;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>SanTrix hat ein neues Ticket erstellt!</h1>
                <p>Folgende Informationen wurden gemeldet:</p>
                <ul>
        """

    for key, value in data.items():
        if key != 'mail_address':
            body += f"<li><strong>{key.capitalize()}:</strong> {value}</li>"

    body += """
                </ul>
            </div>
        </body>
        </html>
        """

    # E-Mail-Inhalt erstellen
    msg = MIMEMultipart()
    msg['From'] = 'admin@SanDataRnD.onmicrosoft.com'  # Absender-E-Mail
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject

    # Anhängen des HTML-Bodys an die E-Mail
    msg.attach(MIMEText(body, 'html'))

    # SMTP-Server-Einstellungen für Microsoft 365 Outlook
    smtp_server = 'smtp.office365.com'
    smtp_port = 587  # Verwenden Sie Port 587 für TLS

    try:
        # Verbindung zum SMTP-Server herstellen
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Starten Sie TLS (Transport Layer Security) für die sichere Verbindung
        server.login('admin@SanDataRnD.onmicrosoft.com', 'Research&Dev06?')  # Anmeldung beim SMTP-Server

        # Senden der E-Mail
        server.sendmail(msg['From'], recipients, msg.as_string())
        server.quit()

        return Response(success=True, message="Mail wurde erfolgreich gesendet.")

    except Exception as e:
        return Response(success=False, message=f"Fehler beim Senden der E-Mail: {e}")


@app.get("/openapi.json")
def custom_openapi_json():
    openapi_schema = get_openapi(
        title=api_titel,
        version=api_version,
        summary=api_summary,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema