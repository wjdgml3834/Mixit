import logging
import os
from dotenv import load_dotenv
import azure.functions as func
from twilio.rest import Client

load_dotenv()

def main(inputRequest: func.ServiceBusMessage):
    message = inputRequest.get_body().decode('utf-8')
    phoneNumber, textMessage = message.split(';')

    # 환경 변수에서 Twilio 설정 불러오기
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    token = os.getenv('TWILIO_AUTH_TOKEN')
    messaging_service_sid = os.getenv('TWILIO_MESSAGING_SERVICE_SID')

    client = Client(account_sid, token)

    client.messages.create(
        messaging_service_sid=messaging_service_sid,
        body=textMessage,
        to=phoneNumber
    )
