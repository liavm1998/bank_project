import ssl
import smtplib
from email.message import EmailMessage

def send_mail_to(receiver):
    """
    my own email sender
    TODO improve running time to slow
    """
    sender = 'bitsmtp5922@gmail.com'
    password = 'garbdvzafjqoihkb'
    subject = 'invitation'
    body = """we are glad to invite you to our bit banking service
    \n follow th link : \"http://127.0.0.1:8000/api/register/\""""
    message = EmailMessage()
    message['From'] = sender
    message['to'] = receiver
    message['subject'] = subject
    message.set_content(body)

    context = ssl.create_default_context()
    try :
        with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
            smtp.login(sender,password)
            smtp.sendmail(sender,receiver,message.as_string())
    except smtplib.SMTPResponseException as err:
        raise err
