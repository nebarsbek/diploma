from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
import os

# Настройки для Gmail (бесплатно)
# MAIL_USERNAME - ваш gmail
# MAIL_PASSWORD - пароль приложения (не от аккаунта!)
# MAIL_FROM - то, что увидит пользователь (например, no-reply@pizza-delivery.com)

conf = ConnectionConfig(
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "akyl.cher@gmail.com"),
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "xcai gyjw chym covt"),
    MAIL_FROM = os.getenv("MAIL_FROM", "no-reply@pizza-delivery.com"),
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_verification_email(email: EmailStr, token: str):
    # Ссылка ведет на фронтенд
    verify_url = f"http://localhost:5173/verify-email?token={token}"
    
    html = f"""
    <h3>Подтвердите свой Email</h3>
    <p>Спасибо за регистрацию! Пожалуйста, нажмите на кнопку ниже для активации аккаунта:</p>
    <a style="padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;" href="{verify_url}">Подтвердить Email</a>
    <p>Если вы не регистрировались, просто проигнорируйте это письмо.</p>
    """

    message = MessageSchema(
        subject="Подтверждение регистрации Pizza Delivery",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)

async def send_reset_password_email(email: EmailStr, token: str):
    reset_url = f"http://localhost:5173/reset-password?token={token}"
    
    html = f"""
    <h3>Сброс пароля</h3>
    <p>Вы запросили сброс пароля. Нажмите на кнопку ниже, чтобы задать новый пароль:</p>
    <a style="padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px;" href="{reset_url}">Сбросить пароль</a>
    <p>Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.</p>
    """

    message = MessageSchema(
        subject="Сброс пароля Pizza Delivery",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    fm = FastMail(conf)
    await fm.send_message(message)