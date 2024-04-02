from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class RequestData(Base):
    __tablename__ = 'request_data'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    request_time = Column(DateTime, default=func.now())
    product_id = Column(Integer)