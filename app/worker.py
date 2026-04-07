import logging

import docker
import httpx

from app.settings import settings
from app.schemas import ScheduleScheme


docker_client = docker.from_env()
# Define the GPU request
gpu_request = docker.types.DeviceRequest(
    count=-1,           # -1 is equivalent to 'all'
    capabilities=[['gpu']] # Requests the 'gpu' capability
)


def run_task(schedule: ScheduleScheme) -> str:
    container = docker_client.containers.run(
        image="video-ai",
        detach=False,
        volumes={
            f'/mnt/records/{schedule.date}/{schedule.id}_{schedule.camera_id}.mkv': {'bind': f'/app/videos/{schedule.id}_{schedule.camera_id}.mkv', 'mode': 'rw'},
            '/home/admin/video_ai/output': {'bind': '/app/output', 'mode': 'rw'},
            '/home/admin/video_ai/models': {'bind': '/app/models', 'mode': 'ro'},
        },
        remove=True,
        device_requests=[gpu_request],
        stdout=True,
        stderr=True,
    )
    print(str(container))
    with open(f"/home/admin/video_ai/output/{schedule.id}_{schedule.camera_id}/summary.txt") as file:
        summary = file.read()
    data = {
        "summary": summary,
        "event": schedule.id,
        "camera_id": schedule.camera_id
    }
    headers = {
        "Authorization": f"Bearer {settings.TOKEN_BEARER}",
        "Content-Type": "application/json"
    }
    with httpx.Client(verify=False, headers=headers) as client:
        response = client.post(settings.BACKEND_URL, json=data)
        logging.info(response.json())




# docker run --rm --gpus all -v /mnt/records/2026-03-26/7952_4.mkv:/app/videos/7952_4.mkv -v /home/admin/video_ai/output:/app/output  -v /home/admin/video_ai/models:/app/models video-ai
