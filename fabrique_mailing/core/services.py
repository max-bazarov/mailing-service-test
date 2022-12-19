import json
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Optional

import dotenv
import requests
from django.db.models import Model, QuerySet

from core.exceptions import ResponseStatusCodeError
from mailings.models import Message
from users.models import Client

dotenv.load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,
    filename='program.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'my_logger.log',
    maxBytes=50000000,
    backupCount=5
)
log.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)


MESSAGE_SERVICE_URL = 'https://probe.fbrq.cloud/v1/send'
TOKEN = os.getenv('MESSAGE_SERVICE_TOKEN')
HEADERS = {'Authorization': f'Bearer {TOKEN}'}


class MailingService:
    mailing: type[Model]

    def __init__(self, mailing: type[Model]):
        self.mailing = mailing

    def get_filtered_clients(self) -> QuerySet:
        filter = self.mailing.filter
        tag = filter.tag
        operator_code = filter.operator_code
        clients = Client.objects.filter(operator_code=operator_code, tag=tag)

        return clients

    def send_message(self, message: type[Message]) -> Optional[Message]:
        data = {
            "id": message.id,
            "phone": message.client.phone_number,
            "text": message.mailing.message
        }
        data = json.dumps(data)

        try:
            response = requests.post(
                f'{MESSAGE_SERVICE_URL}/{message.id}',
                data=data,
                headers=HEADERS
            )
        except Exception as error:
            log.error(error, exc_info=True)
            message.status = Message.Status.FAILED
            log.info(f'Message {message.id} failed to send')
            return None

        if response.status_code != 200:
            log.error(ResponseStatusCodeError('Status code is not 200'))
            message.status = Message.Status.FAILED
            log.info(f'Message {message.id} failed to send')
            return None

        message.status = Message.Status.SENT
        log.info(f'Message {message.id} sent successfully')

        return message
