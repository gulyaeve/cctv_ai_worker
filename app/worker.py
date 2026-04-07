import docker

from app.schemas import ScheduleScheme


client = docker.from_env()
# Define the GPU request
gpu_request = docker.types.DeviceRequest(
    count=-1,           # -1 is equivalent to 'all'
    capabilities=[['gpu']] # Requests the 'gpu' capability
)


async def run_task(schedule: ScheduleScheme):
    container = client.containers.run(
        image="video-ai",
        # command=["echo hello world"],
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
    print(container)




# docker run --rm --gpus all -v /mnt/records/2026-03-26/7952_4.mkv:/app/videos/7952_4.mkv -v /home/admin/video_ai/output:/app/output  -v /home/admin/video_ai/models:/app/models video-ai
