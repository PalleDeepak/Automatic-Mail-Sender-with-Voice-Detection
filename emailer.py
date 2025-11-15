import smtplib, ssl, email.utils
from email.mime.text import MIMEText

def send_email(cfg, to_addr, subject, body):
    host = cfg.get("smtp_host")
    port = int(cfg.get("smtp_port", 465))
    username = cfg.get("username")
    password = cfg.get("password")
    if not all([host, port, username, password]):
        return False, "SMTP config incomplete"

    # try to normalize recipient if spoken like 'alice at example dot com'
    to_addr = to_addr.replace(" ", "").replace("..", ".")
    msg = MIMEText(body, "plain", "utf-8")
    msg["To"] = to_addr
    msg["From"] = username
    msg["Subject"] = subject
    msg["Date"] = email.utils.formatdate(localtime=True)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, [to_addr], msg.as_string())
        return True, None
    except Exception as e:
        return False, str(e)
