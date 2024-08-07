import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from logger_config import logger
import os  

class EmailSender:
    """
    A class to handle sending emails using SMTP.

    Attributes:
        smtp_server (str): The SMTP server address.
        smtp_port (int): The SMTP server port.
        email (str): The sender's email address.
        password (str): The sender's email password.
        session (smtplib.SMTP, optional): The SMTP session object.
    """

    def __init__(self, smtp_server=None, smtp_port=None, email=None, password=None):
        """
        Initializes the EmailSender with SMTP server details and credentials.
        
        If parameters are not provided, it will use environment variables.

        Args:
            smtp_server (str, optional): The SMTP server address.
            smtp_port (int, optional): The SMTP server port.
            email (str, optional): The sender's email address.
            password (str, optional): The sender's email password.
        """
        self.smtp_server = smtp_server or os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = smtp_port or int(os.getenv('SMTP_PORT', 587))
        self.email = email or os.getenv('EMAIL', 'odsi.debate@gmail.com')
        self.password = password or os.getenv('PASSWORD', 'your_password_here')
        self.session = None
    
    def login(self):
        """
        Logs in to the SMTP server using the provided credentials.
        
        Establishes a connection to the SMTP server, starts TLS encryption,
        and logs in with the provided email and password.
        """
        try:
            self.session = smtplib.SMTP(self.smtp_server, self.smtp_port)
            self.session.starttls()
            self.session.login(self.email, self.password)
            logger.info("Login successful.")
        except Exception as e:
            logger.error(f"Login failed: {e}")

    def send_email(self, recipient, subject, body):
        """
        Sends an email to the specified recipient.

        Args:
            recipient (str): The recipient's email address.
            subject (str): The subject of the email.
            body (str): The body of the email.
        
        Raises:
            Warning: If the method is called without logging in first.
        """
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
        """
        Logs out from the SMTP server.

        Closes the SMTP session, ending the connection to the server.
        
        Raises:
            Warning: If there is no active session to logout.
        """
        if self.session:
            self.session.quit()
            logger.info("Logout successful.")
        else:
            logger.warning("No active session to logout.")
