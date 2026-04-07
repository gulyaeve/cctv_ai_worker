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
    ...



async def main():
    test_dict = {
        "id": 9759,
        "date": "2026-04-06",
        "camera_id": 40,
    }
    # await app.run()
    schedule: ScheduleScheme = ScheduleScheme.model_validate(test_dict)
    test_output = await run_task(schedule)
    print(test_output)


if __name__ == "__main__":
    asyncio.run(main())
