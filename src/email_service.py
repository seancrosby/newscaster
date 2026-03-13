import os
import yagmail

class EmailService:
    def __init__(self, user: str, password: str, host: str = "smtp.gmail.com", port: int = 587):
        self.user = user
        # Initialize yagmail with the provided user and password
        # In some cases, yagmail might look in keyring. For cron, passing password explicitly is easier.
        self.yag = yagmail.SMTP(user=user, password=password, host=host, port=port)
    
    def send_brief(self, recipient_email: str, subject: str, content: str):
        try:
            # We'll send the brief as HTML or plain text depending on what we want.
            # Gemini typically gives Markdown. Yagmail can handle simple Markdown/HTML conversion.
            # For simplicity, we'll treat it as Markdown or convert to HTML.
            
            # Simple header/footer
            html_content = f"""
            <html>
                <body>
                    <div style="font-family: Arial, sans-serif; line-height: 1.6;">
                        {content.replace('\n', '<br>')}
                    </div>
                </body>
            </html>
            """
            
            self.yag.send(
                to=recipient_email,
                subject=subject,
                contents=html_content
            )
            print(f"Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            print(f"Failed to send email to {recipient_email}: {e}")
            return False
