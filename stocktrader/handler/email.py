import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

def send_json_email(csv_input, email_list, ticker):
    print("send email is running")
    csv = open('current.csv')
    #json_string = json.dumps(json_input, indent=4)
    
    with get_connection(  
              host=settings.EMAIL_HOST, 
        port=settings.EMAIL_PORT,  
       username=settings.EMAIL_HOST_USER,  
       password=settings.EMAIL_HOST_PASSWORD,  
        use_tls=settings.EMAIL_USE_TLS 
        ) as connection:  
            recipient_list = email_list 
            subject = 'update for stock: ' + ticker
            email_from = settings.EMAIL_HOST_USER  
            message = "test csv"
            print(type(recipient_list)) 
            mail = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
            mail.attach(csv.name, csv.read())
            mail.send()