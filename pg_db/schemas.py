from pydantic import BaseModel
import datetime


class SchemaBase(BaseModel):
    user_id: str
    request_time: datetime.datetime
    product_id: str

    class Config:
        orm_mode = True