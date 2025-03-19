import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import os


class EmailAgent:
    def __init__(self):
        self.SENDER_MAIL = os.environ.get("SENDER_MAIL")
        self.SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD")
        self.success_image = None
        self.succes_audio = None

    def get_recipient_emails(self):
        emails = ["kabirrajsingh10@gmail.com", "ddruk2018@gmail.com"]
        return emails
    
    def send_email_with_attachments(self, sender_email, sender_password, bcc_emails, subject, body_text, image_path, audio_path, video_path):
        # Create the base message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = sender_email  # Can use a placeholder or your own email
        msg['Subject'] = subject
        msg['Bcc'] = ", ".join(bcc_emails)  # ALL recipients will be here

        # Add text body
        msg.attach(MIMEText(body_text, 'plain'))

        # Attach image
        if os.path.exists(image_path):
            with open(image_path, 'rb') as img_file:
                img = MIMEImage(img_file.read())
                img.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(image_path)}"')
                msg.attach(img)
                self.success_image = img
        else:
            if self.success_image:
                msg.attach(self.success_image)

        # Attach audio
        if os.path.exists(audio_path):
            with open(audio_path, 'rb') as audio_file:
                audio = MIMEAudio(audio_file.read())
                audio.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(audio_path)}"')
                msg.attach(audio)
                self.succes_audio = audio
        else:
            if self.succes_audio:
                msg.attach(self.succes_audio)

        # Attach video
        if os.path.exists(video_path):
            with open(video_path, 'rb') as video_file:
                video = MIMEBase('application', 'octet-stream')
                video.set_payload(video_file.read())
                encoders.encode_base64(video)
                video.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(video_path)}"')
                msg.attach(video)

        # Connect to SMTP server and send
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()
            print(f"✅ Email sent successfully to BCC list: {', '.join(bcc_emails)}")
        except Exception as e:
            print(f"❌ Failed to send email: {e}")


    def run(self, script_result):
        mails = list(set(script_result.get('emails', ["ddruk2018@gmail.com"])))

        for i, script in enumerate(script_result['top'][:2]):
            base_path = f"assets/{script_result['bucket_id']}/top/{script['month']}_{script['age_group']}_{script['region']}_top_{i}"
            image_path = f"{base_path}.png"
            audio_path = f"{base_path}.wav"
            video_path = f"{base_path}.mp4"

            self.send_email_with_attachments(
                sender_email=self.SENDER_MAIL,
                sender_password=self.SENDER_PASSWORD,
                bcc_emails=mails,
                subject=f"Advertisement for {script['month']} - {script['age_group']} - {script['region']}",
                body_text=f"{script['title']}. {script['body']}.",
                image_path=image_path,
                audio_path=audio_path,
                video_path=video_path
            )

        for i, script in enumerate(script_result['bottom'][:2]):
            base_path = f"assets/{script_result['bucket_id']}/bottom/{script['month']}_{script['age_group']}_{script['region']}_bottom_{i}"
            image_path = f"{base_path}.png"
            audio_path = f"{base_path}.wav"
            video_path = f"{base_path}.mp4"

            self.send_email_with_attachments(
                sender_email=self.SENDER_MAIL,
                sender_password=self.SENDER_PASSWORD,
                bcc_emails=mails,
                subject=f"Advertisement for {script['month']} - {script['age_group']} - {script['region']}",
                body_text=f"{script['title']}. {script['body']}.",
                image_path=image_path,
                audio_path=audio_path,
                video_path=video_path
            )

        script_result['email_sent'] = True
        self.success_image = None
        self.succes_audio = None
        return script_result



EMAIL_AGENT = EmailAgent()