import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailService:
    def __init__(self, user: str, password: str, host: str = "smtp.gmail.com", port: int = 587):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        # Use SENDER_EMAIL if provided, otherwise fallback to the login user
        self.sender = os.environ.get("SENDER_EMAIL", self.user)
        
    def send_brief(self, recipient_email: str, subject: str, content: str):
        try:
            # Check if we should use TLS (default to True for port 587)
            smtp_use_tls = os.environ.get("SMTP_USE_TLS", "True" if self.port == 587 else "False").lower() == "true"
            
            # Create the message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender
            message["To"] = recipient_email
            
            # Create HTML version
            # We add <br> but keep original newlines to prevent SMTP "Line too long" errors
            formatted_content = content.replace('\n', '<br>\n')
            html = f"""
            <html>
                <body>
                    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
                        {formatted_content}
                    </div>
                </body>
            </html>
            """
            
            part = MIMEText(html, "html")
            message.attach(part)
            
            # Connect and send
            with smtplib.SMTP(self.host, self.port) as server:
                if smtp_use_tls:
                    server.starttls()
                
                # Only login if password is not "password" (our mock default)
                if self.password and self.password != "password":
                    server.login(self.user, self.password)
                
                server.sendmail(self.user, recipient_email, message.as_string())
                
            print(f"Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")
            return False
