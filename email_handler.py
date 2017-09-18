import smtplib
from email.mime.text import MIMEText
import config

sent_from = config.gmail_email
gmail_password = config.gmail_pass
to = config.receiver_list   
text_subtype = 'plain'

def alert_email(error): 
    subject = '[ERROR] I FAILED'  
    body = 'Hey!\n\n I have failed!!!\n\n-----------------------------\n\n'
    footer = "\n\n-----------------------------\n\n\n<3,\n\n Patches_the_Bot\n"
    message = body + error + footer 
    
    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sent_from, gmail_password)

        msg = MIMEText(message, text_subtype)
        msg['Subject'] = subject
        msg['From']   = sent_from

        server.sendmail(sent_from, to, msg.as_string())
        server.close()
    except Exception as e:
        sys.exit( "mail failed; %s" % str(e) )

def success_email(logged_events): 
    subject = '[INFO] Success'  
    body = 'Hey!\n\n I have succeeded.\n\n-----------------------------\n\n'
    footer = "\n\n-----------------------------\n\n\n<3,\n\n Patches_the_Bot\n"
    info = ""
    if len(logged_events) > 0:
        for event in logged_events:
            info = info + event + "\n\n"
    else: 
        info = "No new posts."
    message = body + info + footer 
    
    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sent_from, gmail_password)

        msg = MIMEText(message, text_subtype)
        msg['Subject'] = subject
        msg['From']   = sent_from

        server.sendmail(sent_from, to, msg.as_string())
        server.close()
    except Exception as e:
        sys.exit( "mail failed; %s" % str(e) )