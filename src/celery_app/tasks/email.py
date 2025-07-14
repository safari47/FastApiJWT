import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from loguru import logger

from ...config import settings
from ..app import celery


class SmtpEmailBackend:

    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        from_email: str,
        use_tls: bool = False,
        username: str | None = None,
        password: str | None = None,
    ) -> None:
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.from_email = from_email
        self.use_tls = use_tls
        self.username = username
        self.password = password

    def send_email(
        self,
        recipient: str,
        subject: str,
        body: str,
        is_html: bool = False,
    ) -> None:
        msg = MIMEMultipart()
        msg["From"] = self.from_email
        msg["To"] = recipient
        msg["Subject"] = subject

        # Добавление контента письма в зависимости от типа
        if is_html:
            msg.attach(MIMEText(body, "html"))
        else:
            msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            if self.use_tls:
                server.starttls()

            if self.username and self.password:
                server.login(self.username, self.password)

            server.send_message(
                msg=msg,
            )


@celery.task
def send_verification_email(email: str, user_id: int):
    """
    Отправляет email для подтверждения регистрации
    """
    logger.info(f"Отправка письма для активации аккаунта на {email}")
    base_url = settings.BASE_URL
    activation_link = f"{base_url}/auth/activate?id={user_id}"

    # HTML шаблон письма
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Подтверждение регистрации</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
            }}
            .container {{
                padding: 20px;
                background-color: #f9f9f9;
                border-radius: 8px;
            }}
            .header {{
                text-align: center;
                padding: 20px 0;
                background-color: #4a6baf;
                color: white;
                border-radius: 5px 5px 0 0;
            }}
            .content {{
                padding: 20px;
                background-color: white;
                border-radius: 0 0 5px 5px;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #4a6baf;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #666;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Добро пожаловать!</h1>
            </div>
            <div class="content">
                <p>Здравствуйте!</p>
                <p>Благодарим за регистрацию на нашем сайте. Чтобы активировать вашу учетную запись, пожалуйста, нажмите на кнопку ниже:</p>
                
                <div style="text-align: center;">
                    <a href="{activation_link}" class="button">Активировать аккаунт</a>
                </div>
                
                <p>Если кнопка не работает, скопируйте эту ссылку в браузер:</p>
                <p style="word-break: break-all; font-size: 12px;">{activation_link}</p>
                
                <p>Если вы не регистрировались на нашем сайте, просто игнорируйте это сообщение.</p>
                
                <p>С уважением,<br>Команда поддержки</p>
            </div>
            <div class="footer">
                &copy; 2025 Ваша Компания. Все права защищены.
            </div>
        </div>
    </body>
    </html>
    """

    # Настройки SMTP сервера для MailDev в Docker
    email_backend = SmtpEmailBackend(
        smtp_server="maildev",  # Используем имя сервиса из docker-compose
        smtp_port=1025,  # Порт SMTP в maildev
        from_email="noreply@yourapp.com",
        use_tls=False,
    )

    # Отправка email
    try:
        email_backend.send_email(
            recipient=email,
            subject="Подтверждение регистрации",
            body=html_content,
            is_html=True,
        )
        logger.info(f"Письмо для активации успешно отправлено на {email}")
        return {"status": "success", "email": email}
    except Exception as e:
        logger.error(f"Ошибка отправки письма: {e}")
        return {"status": "error", "message": str(e)}
