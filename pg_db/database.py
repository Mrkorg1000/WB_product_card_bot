import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()

db_host = os.getenv("PG_DB_HOST")
db_port = os.getenv("PG_DB_PORT")
db_name = os.getenv("PG_DB_NAME")
db_user = os.getenv("PG_DB_USER")
db_pass = os.getenv("PG_DB_PASS")


PG_DB_URL = (
        f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    ) 

  
engine = create_async_engine(PG_DB_URL, echo=True)


SessionClass = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    