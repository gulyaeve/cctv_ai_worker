import asyncio
import logging
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from app.schemas import ScheduleScheme
from app.settings import settings
from app.worker import run_task



# Настройка логирования
logging.basicConfig(level=logging.INFO)


broker = RabbitBroker(url=settings.rabbitmq_url)
app = FastStream(broker)




@broker.subscriber(settings.QUEUE_NAME)
async def ai_request_handler(schedule: ScheduleScheme):
    try:
        run_task(schedule)
    except Exception as e:
        logging.warning(f"{e}")


async def main():
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
