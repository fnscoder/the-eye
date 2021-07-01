from celery import shared_task
from celery.utils.log import get_task_logger

from events.serializers import EventSerializer

logger = get_task_logger(__name__)


@shared_task()
def create_event(data):
    """
    Validates the event data and timestamp in order to create a new event or a new error
    """
    logger.info('Validating event data')
    serializer = EventSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        logger.info(serializer.data)
        logger.info('Valid event data')
    else:
        logger.info(serializer.data)
        logger.info('Invalid event data')
