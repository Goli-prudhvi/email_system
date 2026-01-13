# email_sender.py
import smtplib
import socket
from email.mime.text import MIMEText
from typing import Optional

from config import get_smtp_config

SMTP_HOST = "smtp.gmail.com"
# SMTP_PORT = 465
SMTP_PORT = 587
SMTP_TIMEOUT = 60  # seconds


class EmailSendError(Exception):
    pass


def send_email(
    to: str,
    subject: str,
    body: str,
    *,
    raise_on_failure: bool = False
) -> bool:
    """
    Sends an email safely.
    Returns True if sent, False if failed.
    """
    smtp_email, smtp_password = get_smtp_config()
    if not to or not subject or not body:
        msg = "Invalid email payload (to/subject/body)"
        if raise_on_failure:
            raise EmailSendError(msg)
        print(f"❌ {msg}")
        return False

    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["From"] = smtp_email      # ✅ CHANGED
        msg["To"] = to
        msg["Subject"] = subject

        with smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT,
            timeout=SMTP_TIMEOUT
        ) as server:
            server.login(smtp_email, smtp_password)  # ✅ CHANGED
            server.send_message(msg)

        print(f"✅ Email sent to {to}")
        return True

    except smtplib.SMTPAuthenticationError:
        error = "SMTP authentication failed (check email/password or app password)"
    except smtplib.SMTPRecipientsRefused:
        error = f"Recipient address rejected: {to}"
    except smtplib.SMTPServerDisconnected:
        error = "SMTP server disconnected unexpectedly"
    except socket.timeout:
        error = "SMTP connection timed out"
    except smtplib.SMTPException as e:
        error = f"SMTP error: {e}"
    except Exception as e:
        error = f"Unexpected error while sending email: {e}"

    print(f"❌ {error}")

    if raise_on_failure:
        raise EmailSendError(error)

    return False



# # email_sender.py
# import socket

# # 🔥 Force IPv4 only (fixes Gmail SMTP on Railway / cloud)
# _original_getaddrinfo = socket.getaddrinfo

# def ipv4_only_getaddrinfo(*args, **kwargs):
#     return [
#         addr for addr in _original_getaddrinfo(*args, **kwargs)
#         if addr[0] == socket.AF_INET
#     ]

# socket.getaddrinfo = ipv4_only_getaddrinfo



# import smtplib
# from email.mime.text import MIMEText
# from typing import Optional

# from config import get_smtp_config
# # SMTP_HOST = "smtp.gmail.com"
# # SMTP_PORT = 587          # ✅ FIX
# # SMTP_TIMEOUT = 20
# SMTP_HOST = "74.125.133.109"
# SMTP_PORT = 587
# SMTP_TIMEOUT = 120

# class EmailSendError(Exception):
#     pass


# def send_email(
#     to: str,
#     subject: str,
#     body: str,
#     *,
#     raise_on_failure: bool = False
# ) -> bool:

#     smtp_email, smtp_password = get_smtp_config()

#     if not to or not subject or not body:
#         msg = "Invalid email payload (to/subject/body)"
#         if raise_on_failure:
#             raise EmailSendError(msg)
#         print(f"❌ {msg}")
#         return False

#     try:
#         msg = MIMEText(body, "plain", "utf-8")
#         msg["From"] = smtp_email
#         msg["To"] = to
#         msg["Subject"] = subject

#         with smtplib.SMTP(
#             SMTP_HOST,
#             SMTP_PORT,
#             timeout=SMTP_TIMEOUT
#         ) as server:
#             server.ehlo()
#             server.starttls()          # ✅ REQUIRED
#             server.ehlo()
#             server.login(smtp_email, smtp_password)
#             server.send_message(msg)

#         print(f"✅ Email sent to {to}")
#         return True

#     except smtplib.SMTPAuthenticationError:
#         error = "SMTP authentication failed (check Gmail app password)"
#     except smtplib.SMTPRecipientsRefused:
#         error = f"Recipient address rejected: {to}"
#     except smtplib.SMTPServerDisconnected:
#         error = "SMTP server disconnected unexpectedly"
#     except socket.timeout:
#         error = "SMTP connection timed out"
#     except smtplib.SMTPException as e:
#         error = f"SMTP error: {e}"
#     except Exception as e:
#         error = f"Unexpected error while sending email: {e}"

#     print(f"❌ {error}")

#     if raise_on_failure:
#         raise EmailSendError(error)

#     return False
