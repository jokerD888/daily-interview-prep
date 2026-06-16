from pydantic import BaseModel
from datetime import datetime


class MaterialResponse(BaseModel):
    id: int
    title: str
    file_type: str
    status: str
    card_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}
