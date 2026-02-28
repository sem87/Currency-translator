# ________________________
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, Form, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_session, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, mapped_column

from API.db.models import Books


engine = create_async_engine('sqlite+aiosqlite:///books.db')
new_session = async_sessionmaker(engine, expire_on_commit=False)

app = FastAPI()


async def get_session():
    async with new_session() as session:
        yield session


# books = [{"id": 1, "title": "Супер книга", "autor": "Тяпкин Валерьян"},
#          {"id": 2, "title": "Бабл гам в голове", "autor": "Свой Собственный"}]

SessionDep = Annotated[AsyncSession, Depends(get_session)]


class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    autor: Mapped[str]


@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"сообщение": "Все отлично создалось"}


# @app.get("/books/{id}", summary="Получить книгу по id", tags=["ВСЕ Книги"],
#          description="Полное описание определенной книги", responses={
#         200: {"description": "OK"},
#         404: {"description": "Not Found"}}
#          )
# def read(id: int):
#     for book in books:
#         if book["id"] == id:
#             return book
#     raise HTTPException(status_code=404, detail="НЕ нашли книжку")
#
#
# @app.post("/books", summary="Добавить КНИГУ", tags=["ВСЕ Книги"],
#           description="Добавим книгу в BOOKS")
# async def creat(book: Books):
#     books.append({"id": len(books) + 1, "title": book.title, "autor": book.autor})
#     # raise HTTPException(status_code=404, detail="НЕ СМОГЛИ ДОБАВИТЬ КНИГУ")
#     return books


class BookAddSchema(BaseModel):
    title: str
    autor: str


class BookSchema(BookAddSchema):
    id: int


@app.get("/books")
async def get_books(data: Books, session: SessionDep):
    await session.commit()
    return session


@app.post("/books", summary="Добавить КНИГУ", tags=["ВСЕ Книги"], description="Добавим книгу в BOOKS")
async def add_books(data: Books, session: SessionDep):
    new_book = BookModel(title=data.title, autor=data.autor)
    session.add(new_book)
    await session.commit()
    return {"сообщение": "Все отлично создалось"}


@app.get("/b", summary="Другая", tags=["ВСЕ РУЧКИ"])
def read():
    return "Это вторая ручка"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, use_colors=True, log_level="debug")
