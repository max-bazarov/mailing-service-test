import logging
from logging.handlers import RotatingFileHandler

from celery import shared_task

from core.services import MailingService
from mailings.models import Mailing, Message
from users.models import Client

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


@shared_task()
def start_mailing(mailing_id: int) -> None:
    mailing = Mailing.objects.get(id=mailing_id)
    mailing_service = MailingService(mailing)
    clients = mailing_service.get_filtered_clients()

    for client in clients:
        add_message_to_queue.delay(client.id, mailing.id)


@shared_task(default_retry_delay=30, max_retries=None)
def add_message_to_queue(client_id: int,
                         mailing_id: int) -> None:

    client = Client.objects.get(id=client_id)
    mailing = Mailing.objects.get(id=mailing_id)
    mailing_service = MailingService(mailing)
    message, _ = Message.objects.get_or_create(
            mailing=mailing,
            client=client
    )
    message.status = Message.Status.NOT_SENT
    log.info(f'Add message to queue: {message.id}')

    result = mailing_service.send_message(message)

    if not result:
        add_message_to_queue.retry()
