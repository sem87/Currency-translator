import json
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from API.db.models import *
from API.parser.parscb import get_cbr_zena
from Core.config import *
from Core.logger import logger
from data_SQL import *

app = FastAPI()
app.mount("/API/static", StaticFiles(directory="API/static"), name="static")

# -----------------------------
# Указываем путь к папке с шаблонами
templates = Jinja2Templates(directory="HTML")


# -----------------------------
@app.get("/", tags=["Главная страница ПО ВАЛЮТЕ"], summary="Начальная страница", description="Загружает главную страницу HTML")
def nachalo(request: Request):
    tabliza_zen = session.query(Zeni).first()
    okruglen = Zen(usd=tabliza_zen.usd, eur=tabliza_zen.eur, gbp=tabliza_zen.gbp, cny=tabliza_zen.cny,
                   vrema_obnow=tabliza_zen.created_at)
    return templates.TemplateResponse(
        "Obmen.html",
        {"request": request, "usd": okruglen.usd, "eur": okruglen.eur,
         "gbp": okruglen.gbp, "cny": okruglen.cny, "vrema_obnow": okruglen.vrema_obnow,
         "summa": 1.0, "ticker": "usd", "ticker_convert": "rub", "rezult": 0.0})
    # return FileResponse("HTML/Obmen.html")


# @app.get("/key", tags=["Главная страница"], summary="Секретные данные", description="Выводит секретные данные env")
# def config():
#     return load_config()


@app.get("/p", tags=["Действия с данными"], summary="Чтение данных из json", description="Читает все данные из JSON")
def s():
    try:
        js = {}
        with open('jey.json', 'r', encoding='utf-8') as file:
            jeys = json.load(file)["val"]
            for jey in jeys:
                user = User(**jey)
                js[user.login] = user.password
        return js
    except ValidationError as e:
        # print(e.errors())
        return e.errors()


@app.post("/otzivi", tags=["Действия с данными SQL"], summary="Запись ФИО и Отзыва (В SQL)",
          description="Работа с ОТЗЫВАМИ")
def otzovidef(
        name_fio: str = Form(
            ...,
            min_length=2,
            max_length=50
            # pattern="^[А-Яа-яA-Za-z]+$",  # только буквы и пробелы
            # description="Введите ваше ФИО (от 2 до 50 символов)",
        ),
        email: str = Form(..., min_length=4, max_length=50, description="Ваш ЕМАЙЛ"),
        age: int | None = Form(None),
        otziv: str | None = Form(None)):
    user = Otziv(name_fio=name_fio, otziv=otziv, email=email, age=age)
    if user.name_fio == "Aaa":
        user.name_fio = "УслоВИЕ"
    if user.otziv == None:
        user.otziv = "НЕТУ_ОТЗЫВА"
    new_user = Usersql(name_fio=user.name_fio, email=user.email, age=user.age, otziv=user.otziv)
    session.add(new_user)
    session.commit()
    logger.info(f" {user.name_fio}   Оставил отзыв")
    return f"Ваш отзыв {user.name_fio} успешно отправлен  вот он   {user}"


@app.get("/otzivi", tags=["Действия с данными SQL"], summary="ПОлучение всей таблице Отзывов (В SQL)",
         description="Работа с ОТЗЫВАМИ")
def otzovidef(request: Request):
    all_users = session.query(Usersql).all()
    dict_otziv = {}
    for all_user in all_users:
        dict_otziv[all_user.name_fio] = all_user.otziv
    return templates.TemplateResponse(
        "Otvet.html",
        {"request": request, "dict_otziv": dict_otziv})


@app.post("/parsing", tags=["Действия с данными"], summary="Парсинг цен",
          description="Парсинг цен на центробанк России")
def pars(request: Request):
    zena = get_cbr_zena()
    # Получаем первую запись из БД
    tabli = session.query(Zeni).first()
    tabli.usd = zena["usd"]
    tabli.eur = zena["eur"]
    tabli.gbp = zena["gbp"]
    tabli.cny = zena["cny"]
    tabli.created_at = datetime.now(timezone.utc)
    session.commit()
    tabliza_zen = session.query(Zeni).first()
    return templates.TemplateResponse(
        "Obmen.html",
        {"request": request, "usd": round(tabliza_zen.usd, 2), "eur": round(tabliza_zen.eur, 2),
         "gbp": round(tabliza_zen.gbp, 2), "cny": round(tabliza_zen.cny, 2), "vrema_obnow": tabliza_zen.created_at})
    # return session.query(Zeni).first()


@app.post("/convert", tags=["Действия с данными"], summary="Конвертация ВАЛЮТЫ ",
          description="Перевод одной валюты в другую")
def pars(request: Request, summa: float = Form(...),
         ticker: str = Form(...),
         ticker_convert: str = Form(...)):
    tik = Tiker(ticker=ticker, ticker_convert=ticker_convert, summa=summa)
    tabliza_zen = session.query(Zeni).first()
    din = {"usd": tabliza_zen.usd, "eur": tabliza_zen.eur, "gbp": tabliza_zen.gbp, "cny": tabliza_zen.cny}
    do = din[tik.ticker] if tik.ticker in din else 1.0
    posle = din[tik.ticker_convert] if tik.ticker_convert in din else 1.0
    rezult = tik.summa * (do / posle)
    return templates.TemplateResponse(
        "Obmen.html",
        {"request": request, "rezult": round(rezult, 2), "summa": tik.summa, "usd": round(tabliza_zen.usd, 2),
         "eur": round(tabliza_zen.eur, 2), "gbp": round(tabliza_zen.gbp, 2), "cny": round(tabliza_zen.cny, 2),
         "vrema_obnow": tabliza_zen.created_at, "ticker": tik.ticker, "ticker_convert": tik.ticker_convert})


@app.get("/sel", tags=["Действия select bnl"], summary="Простейшие операции",
         description="Действия select ОБУЧЕНИЕ")
def selec():
    firs = session.query(Usersql.age, Usersql.id, Usersql.name_fio).order_by(desc(Usersql.age))
    itog = {}
    for fir in firs:
        itog[fir[0]] = [fir[1], fir[2]]
    print(itog)
    return itog


if __name__ == "__main__":
    uvicorn.run("One:app", reload=True, use_colors=True, log_level="debug")
