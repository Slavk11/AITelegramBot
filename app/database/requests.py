from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete, desc
def connection(func):
    async def inner(*args, **kwargs):
        async with async_session() as session:
            return await func(session, *args, **kwargs)
    return inner

@connection
async def set_user(session, tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


@connection
async def get_user(session, tg_id):
    return await session.scalar(select(User).where(User.tg_id == tg_id))

@connection
async def get_users(session):
    return await session.scalars(select(User))

@connection
async def delete_user(session, tg_id):
    await session.execute(
        delete(User).where(User.tg_id == tg_id)
    )
    await session.commit()

