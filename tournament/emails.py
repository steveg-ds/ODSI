import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logger_config import logger

class EmailSender:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587, email='odsi.debate@gmail.com', password='hybb dhaj gyxh xrue'):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.session = None
    
    def login(self):
        try:
            self.session = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.session.starttls()
            self.session.login(self.email, self.password)
            logger.info("Login successful.")
        except Exception as e:
            logger.error(f"Login failed: {e}")

    def send_email(self, recipient, subject, body):
        if not self.session:
            logger.warning("Please login first.")
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(body, 'plain'))

            self.session.sendmail(self.email, recipient, msg.as_string())
            logger.info(f"Email sent to {recipient}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    def logout(self):
        if self.session:
            self.session.quit()
            logger.info("Logout successful.")
        else:
            logger.warning("No active session to logout.")