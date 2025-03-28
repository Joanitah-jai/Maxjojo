import os
import africastalking
from dotenv import load_dotenv

load_dotenv()
def send_sms(message: str, recipients: list):

    username = os.environ.get('username_for_sms')   
    api_key = os.environ.get('api_key')    
    africastalking.initialize(username, api_key)

    sms = africastalking.SMS
    try:
        response = sms.send(message, recipients)
        # print("SMS sent successfully:", response)
        # return response
    except Exception as e:
        print("Error sending SMS:", e)
        return None