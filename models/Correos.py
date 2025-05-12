import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os, dotenv
import ssl

def enviar_correo(destinatario, asunto, mensaje, nombre_proyecto):
    ssl._create_default_https_context = ssl._create_unverified_context
    
    html_message = f"""
<html>
  <head>
    <style>
      body {{
        margin: 0;
        padding: 0;
        background-color: #f1f1f1;
        font-family: 'Helvetica Neue', sans-serif;
      }}
      .container {{
        max-width: 600px;
        margin: 30px auto;
        background-color: #fff;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      }}
      .header {{
        background: linear-gradient(90deg, #007bff, #00c6ff);
        color: white;
        padding: 30px 20px;
        text-align: center;
      }}
      .header img {{
        max-height: 50px;
        margin-bottom: 10px;
      }}
      .content {{
        padding: 30px;
        color: #333;
        font-size: 16px;
        line-height: 1.6;
      }}
      .button {{
        display: inline-block;
        margin-top: 20px;
        padding: 12px 25px;
        background: linear-gradient(90deg, #007bff, #00c6ff);
        color: white;
        text-decoration: none;
        border-radius: 8px;
        font-weight: bold;
      }}
      .footer {{
        text-align: center;
        font-size: 12px;
        color: #aaa;
        padding: 20px;
        background-color: #fafafa;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>Invitación a CodeShare</h1>
      </div>
      <div class="content">
        <p>Hola,</p>
        <p>Has sido invitado a colaborar en el proyecto <strong>{nombre_proyecto}</strong> en <strong>CodeShare</strong>.</p>
        <p style="margin-top: 30px;">{mensaje}</p>
      </div>
      <div class="footer">
        © 2025 CodeShare. Todos los derechos reservados · Guatemala, GTM
      </div>
    </div>
  </body>
</html>
"""
    email = Mail(
        from_email='rudyoxlajrudy@gmail.com',
        to_emails=destinatario,
        subject=asunto,
        plain_text_content=mensaje,
        html_content=html_message
    )
    try:
        dotenv.load_dotenv()
        apiKey = os.environ.get("SENDGRID_API_KEY")
        
        sg = SendGridAPIClient(api_key=apiKey)
        response = sg.send(email)
        print(f"Status: {response.status_code}")
    except Exception as e:
        print(f"Error al enviar: {e}")