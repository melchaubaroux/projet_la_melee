

import smtplib,ssl
from email.mime.text import MIMEText

from param import API_KEY

# Remplacez ces valeurs par celles de votre compte
GMAIL_USERNAME = "mel.chaubaroux@gmail.com"
GMAIL_APP_PASSWORD = API_KEY

def send_email(subject, body, sender, recipients):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    
    # Configuration du serveur SMTP
    smtp_server = "smtp.gmail.com"
    port = 465  # Pour SSL
    
    # Création de la connexion sécurisée
    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(GMAIL_USERNAME, GMAIL_APP_PASSWORD)
        server.send_message(msg, from_addr=sender, to_addrs=recipients)



if __name__=="__main__" : 

    # Exemple d'utilisation
    subject = "Test email from Python"
    body = "Ceci est un test d'email envoyé depuis un script Python."
    sender = "mel.chaubaroux@gmail.com"
    recipients = ["mel.chaubaroux@gmail.com"]

    # Test
    send_email(subject, body, sender, recipients)
