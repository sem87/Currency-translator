from datetime import datetime, timedelta

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, ValidationError


# from typing import Optional

class Zen(BaseModel):
    usd: float = Field(default=None, dg=25, title="usd", description="Значение usd из ЦБ", examples="777")
    eur: float = Field(default=None, dg=25, title="eur", description="Значение eur из ЦБ", examples="555")
    gbp: float = Field(default=None, dg=2, title="gbp", description="Значение gbp из ЦБ", examples="111")
    cny: float = Field(default=None, dg=2, title="cny", description="Значение cny из ЦБ", examples="1")
    vrema_obnow: datetime = Field(default=None)

    @field_validator('usd', 'eur', 'gbp', 'cny')
    @classmethod
    def round_zen(cls, v):
        v = round(v, 2)
        return v

    @field_validator('vrema_obnow')
    @classmethod
    def round_time(cls, val):
        val = (val + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
        return val


class User(BaseModel):
    id: int = Field(default="Без id", gt=0)
    name: str = Field(default=None, min_length=1, max_length=100)
    o_sebe: str = Field(default="Ни слова о себе", min_length=1, max_length=100)
    friends: list[int] = Field(default=None)
    login: str
    password: str

    @field_validator('login',mode='before')
    def norm_log(cls, v):
        if v == 123:
            raise ValueError(f"Ошибка {v} не строка!!!!!")
        return v

    @field_validator('name', mode='before')
    def normal_name(cls, v):
        if v is None or v == "":
            return None
        return ' '.join(word.capitalize() for word in v.strip().lower().split())

    @field_validator('friends', mode='before')
    def about_friends(cls, v):
        if v is not int:
            return v == [1, 2, 45]
        return v

    @field_validator('o_sebe')
    def text_o_sebe(cls, v):
        return v.lower()


class Otziv(BaseModel):
    name_fio: str
    email: EmailStr
    age: int | None = None
    otziv: str | None = None

    @field_validator('name_fio', mode='before')
    def normalize_name(cls, v):
        """Приводит ФИО к формату: каждое слово с заглавной буквы"""
        if v is None or v == "":
            return None
        return ' '.join(word.capitalize() for word in v.strip().lower().split())

    @field_validator('age')
    def age_validator(cls, values):
        if values < 0:
            values = 0
        elif values > 130:
            values = 555
        return values


class Tiker(BaseModel):
    summa: float | None = 0.0
    ticker: str | None = None
    ticker_convert: str | None = None

    @field_validator('ticker', 'ticker_convert', mode='before')
    def normalize_tiker(cls, value):
        return value.lower()


class Books(BaseModel):
    title: str | None = None
    autor: str | None = None
