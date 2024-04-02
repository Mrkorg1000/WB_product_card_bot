from sqlalchemy import select
from pg_db.database import SessionClass
from pg_db.models import RequestData as DB_RD
import datetime


db = SessionClass()

# Возвращает 5 последних записей
async def get_5_latest_requests(db, user_id):
    requests = await db.execute(
        select(DB_RD).filter_by(user_id=user_id).order_by(DB_RD.request_time.desc()).limit(5)      
    )
    await db.close()
    return requests.scalars().fetchall() 


# Добавляет объект RequestData в БД

async def add_request_to_db(db, user_id, product_id):
    new_request = DB_RD(
        user_id=user_id,
        request_time=datetime.datetime.now(),
        product_id=product_id
    )
    db.add(new_request)
    await db.commit()
    await db.refresh(new_request)
    await db.close()
    return new_request




    