import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))


def require_env(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def optional_env(name, default):
    value = os.environ.get(name)
    if value is None or not value.strip():
        return default
    return value.strip()


def env_bool(name, default):
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    value = raw.strip().lower()
    if value in ("1", "true", "yes", "on"):
        return True
    if value in ("0", "false", "no", "off"):
        return False
    raise SystemExit(f"{name} must be true or false, got {raw!r}")


sender_email = require_env("SENDER_EMAIL")
receiver_email = require_env("RECEIVER_EMAIL")
password = require_env("SMTP_PASSWORD")
smtp_host = optional_env("SMTP_HOST", "smtp.gmail.com")
smtp_port_text = optional_env("SMTP_PORT", "465")
use_ssl = env_bool("SMTP_USE_SSL", True)

try:
    smtp_port = int(smtp_port_text)
except ValueError:
    raise SystemExit(f"SMTP_PORT must be an integer, got {smtp_port_text!r}")
if not 1 <= smtp_port <= 65535:
    raise SystemExit(f"SMTP_PORT must be between 1 and 65535, got {smtp_port}")

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
"""
html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="https://github.com/dpradeep42">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)

if use_ssl:
    # Implicit TLS, same as Gmail on port 465.
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
else:
    # Plain SMTP for a local debugging server. Log in only when it advertises AUTH.
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        if server.has_extn("auth"):
            server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
