import asyncio

from sqlalchemy import (URL, Boolean, Column, DateTime, Float, ForeignKey, Integer, MetaData, String, Table,
                        create_engine, text,)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker


metadata_obj = MetaData()
workers_table = Table("workers", metadata_obj,
                      Column("id", Integer, primary_key=True),
                      Column("username", String),
                      Column("id", String),
                      )


