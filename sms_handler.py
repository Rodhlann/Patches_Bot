from twilio.rest import Client
import config
import logging 

def alert_sms(error):
    header = "-\n\n-----------------\n\n" 
    footer = "\n\n-----------------\n\n" 
    info = "Error received:\n" + error
    send(header + info + footer) 

def success_sms(logged_events):
    header = "-\n\n-----------------\n\n" 
    footer = "\n\n-----------------\n\n" 
    info = "New posts:\n"
    if len(logged_events) > 0:
        for event in logged_events:
            info = info + event + "\n\n"
    else: 
        info = "No new posts."
    send(header + info + footer) 

def send(message):
    try: 
        client = Client(config.account_sid, config.auth_token)
        message = client.messages.create(
            to=config.sms_to, 
            from_=config.sms_from,
            body=message)
    except Exception as e: 
        logging.error("SMS error:\n" + str(e))