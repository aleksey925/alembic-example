import asyncio
import os
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()


def build_pg_dsn(user: str, password: str, host: str, dbname: str) -> str:
    return f'postgresql+psycopg://{user}:{password}@{host}:5432/{dbname}'


class Warehouse(Base):  # type: ignore
    __tablename__ = 'warehouse'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    address: Mapped[str]


async def add_warehouse(name: str, address: str, conn: AsyncConnection) -> None:
    await conn.execute(insert(Warehouse), [{'name': name, 'address': address}])


async def get_warehouses(conn: AsyncConnection) -> list[dict[str, Any]]:
    query = select(Warehouse)
    return [dict(i._mapping) for i in await conn.execute(query)]


async def main() -> None:
    load_dotenv()
    pg_dsn = build_pg_dsn(
        user=os.environ['PG_USER'],
        password=os.environ['PG_PASSWORD'],
        host=os.environ['PG_HOST'],
        dbname=os.environ['PG_DB'],
    )
    engine = create_async_engine(pg_dsn)
    try:
        async with engine.begin() as conn:
            await add_warehouse('Warehouse 1', 'Address 1', conn)
            await add_warehouse('Warehouse 2', 'Address 2', conn)
            warehouses = await get_warehouses(conn)
            print(warehouses)
    finally:
        await engine.dispose()


if __name__ == '__main__':
    asyncio.run(main())
