"""
email_tools.py provides utility functions for sending emails in the Eprice backend.

Features:
- Asynchronous email sending using FastAPI-Mail.
- Configures SMTP connection using environment variables from the secrets configuration.
- Sends verification emails with a code and a direct verification link for user registration and authentication flows.

Dependencies:
- fastapi_mail for asynchronous email delivery.
- config.secrets for SMTP credentials and configuration.

Intended Usage:
- Used by authentication and user management services to send verification codes to users.
- Can be extended for other email-related utilities as needed.
"""

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config.secrets import (
    MAIL_USERNAME,
    MAIL_FROM,
    MAIL_PORT,
    MAIL_SERVER,
    MAIL_FROM_NAME,
    MAIL_PASSWORD
)


conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_FROM_NAME=MAIL_FROM_NAME,
    MAIL_STARTTLS=True,      # Add this line
    MAIL_SSL_TLS=False       # And this line (set to True if your SMTP requires SSL/TLS)
)

async def send_email_async(email_to: str, verification_code: str):
    '''
    Send an email asynchronously with a verification code and a link to verify the email address.

    Args:
        email_to (str): The recipient's email address.
        verification_code (str): The verification code to be sent in the email.
    '''

    subject = 'Verify your email address'
    body = f'''
    <html>
        <body style="font-family: Arial, sans-serif; text-align: center;">
            <h1>Verify your email address</h1>
            <p>Use the code below to verify your email address:</p>
            <div style="display: inline-block; margin: 20px auto; padding: 16px 32px; background: #f3f3f3; border-radius: 8px; font-size: 2em; font-weight: bold; color: #333;">
                {verification_code}
            </div>
            <p>Or click the link below to verify directly:</p>
            <a href="http://localhost:5173/auth/verify?email={email_to}&code={verification_code}"
               style="display: inline-block; margin-top: 16px; padding: 12px 24px; background: #2563eb; color: #fff; text-decoration: none; border-radius: 6px; font-size: 1.1em;">
                Verify Email
            </a>
        </body>
    </html>
    '''
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype='html',
    )
    
    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')
