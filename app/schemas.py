from pydantic import BaseModel
from datetime import date


class ScheduleScheme(BaseModel):
    id: int
    date: date
    camera_id: int