import asyncio
import logging
import httpx
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
        summary = await run_task(schedule)
        data = {
            "summary": summary,
            "event": schedule.id,
            "camera_id": schedule.camera_id
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.BACKEND_URL, json=data)
            logging.info(response.json())
    except Exception as e:
        logging.warning(f"{e}")


async def main():
    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
