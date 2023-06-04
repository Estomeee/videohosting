from sqlalchemy import Table, Column, Integer, String, MetaData

from src.main import metadata

md = MetaData()

user_table = Table(
    "user_account",
    md,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

user_table2 = Table(
    "user_account2",
    md,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)
