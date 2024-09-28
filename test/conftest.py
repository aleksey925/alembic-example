import asyncio
import os
from pathlib import Path
from typing import AsyncGenerator, Generator

import pytest
from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncConnection, create_async_engine
from sqlalchemy_utils import drop_database, create_database, database_exists

from main import build_pg_dsn

load_dotenv()
os.environ['PG_DB'] = f"{os.environ['PG_DB']}_test"
PG_DSN = build_pg_dsn(
    user=os.environ['PG_USER'],
    password=os.environ['PG_PASSWORD'],
    host=os.environ['PG_HOST'],
    dbname=os.environ['PG_DB'],
)
ROOT_DIR = Path(__file__).parent.parent


@pytest.fixture(scope='session')
def project_root() -> Path:
    return ROOT_DIR


@pytest.fixture(scope='session')
def setup_pg(project_root: Path) -> Generator[None, None, None]:
    if database_exists(PG_DSN):
        drop_database(PG_DSN)
    create_database(PG_DSN)

    curr_work_dir = os.getcwd()
    os.chdir(project_root)
    alembic_cfg = Config(str(ROOT_DIR / 'alembic.ini'))
    command.upgrade(alembic_cfg, 'head')
    os.chdir(curr_work_dir)

    yield

    drop_database(PG_DSN)


@pytest.fixture(scope='session')
def pg_engine() -> Generator[AsyncEngine, None, None]:
    engine = create_async_engine(PG_DSN)
    yield engine
    asyncio.run(engine.dispose())


@pytest.fixture
async def pg_conn(setup_pg: None, pg_engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    async with pg_engine.begin() as conn:
        yield conn
        await conn.rollback()
