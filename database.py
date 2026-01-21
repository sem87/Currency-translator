import asyncio

from sqlalchemy import URL, Boolean, Column, DateTime, Float, ForeignKey, Integer, String, create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker


# from config import settings


# engine = create_engine(url='sqlite:///./books.db')  # , echo=True
# # Для PostgreSQL: 'postgresql://user:password@localhost/dbname'
# # Для MySQL: 'mysql+pymysql://user:password@localhost/dbname'
# with engine.connect() as conn:
#     res = conn.execute(text("SELECT * FROM book")).all()
#     for stroka in res:
#         print(f"{stroka[0]}    {stroka[1]}   {stroka[2]}")
#     # print(res.all())
#     conn.commit()


async_engine = create_async_engine(url='sqlite+aiosqlite:///books.db')  # , echo=True
async def start():
    async with async_engine.connect() as conn:
        res =await conn.execute(text("SELECT * FROM book"))
        print(res.all())

asyncio.run(start())
