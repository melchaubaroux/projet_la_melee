import unittest
from unittest.mock import patch, MagicMock


@patch('smtplib.SMTP_SSL')  # Mock de la classe SMTP_SSL
@patch('ssl.create_default_context')  # Mock de ssl.create_default_context
@patch('email.mime.text.MIMEText')  # Mock de ssl.create_default_context
def test_send_email(mock_mime,mock_context,mock_SMTP_SSL):

    
    # Définir les valeurs des arguments
    API_KEY=MagicMock()
    subject = "Test Subject"
    body = "Test email body"
    sender = "sender@example.com"
    recipients = ["recipient@example.com"]
    smtp_server = "smtp.example.com"
    port=465

    
    mock_mime(body).return_value=MagicMock(text=body)
    mock_mime.msg['Subject'].return_value = subject
    mock_mime.msg['From'].return_value = sender
    mock_mime.msg['To'].return_value = ', '.join(recipients)

    # mock_context().return_value=MagicMock()
    context=mock_context()

    with mock_SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, API_KEY)
        server.send_message(mock_mime(body), from_addr=sender, to_addrs=recipients)

        # server.assert_called_once_with(smtp_server, port, context=context)

        server.login.assert_called_once_with(sender, API_KEY)
        
        # Vérification que la méthode send_message a bien été appelée avec le bon message
        server.send_message.assert_called_once()

    mock_SMTP_SSL.assert_called_once_with(smtp_server, port, context=context)

  

# Exécution du test
if __name__ == "__main__":
    unittest.main()
