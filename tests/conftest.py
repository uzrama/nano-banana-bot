import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy import func, DateTime, Integer, BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from nano_banana_bot.models.base import Base
from nano_banana_bot.database.alchemy.context import AlchemySessionContext


@pytest.fixture(scope="session", autouse=True)
def fix_sqlite_compatibility():
    # 1. Fix type_annotation_map for SQLite
    # SQLite's BigInteger does not support AUTOINCREMENT the way Integer does.
    # Therefore, we replace BigInteger and DateTime(timezone=True)
    for type_hint, sql_type in Base.registry.type_annotation_map.items():
        if isinstance(sql_type, DateTime) and sql_type.timezone:
            Base.registry.type_annotation_map[type_hint] = DateTime(timezone=False)
        if isinstance(sql_type, BigInteger):
            Base.registry.type_annotation_map[type_hint] = Integer()

    # 2. Fix server_default in already created columns
    for table in Base.metadata.tables.values():
        for column in table.columns:
            # Fix timezone
            if column.server_default is not None and hasattr(column.server_default, "arg"):
                arg = str(column.server_default.arg)
                if "timezone" in arg.lower():
                    column.server_default.arg = func.now()

            # Replace BigInteger with Integer for primary keys in SQLite
            if column.primary_key and isinstance(column.type, BigInteger):
                column.type = Integer()


@pytest_asyncio.fixture
async def engine(fix_sqlite_compatibility):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session_pool(engine):
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest_asyncio.fixture
async def sql_context(session_pool):
    return AlchemySessionContext(session_pool)


@pytest_asyncio.fixture
async def session(session_pool):
    async with session_pool() as session:
        yield session


@pytest.fixture
def mock_redis():
    mock = AsyncMock()
    mock.get = AsyncMock(return_value=None)
    mock.set = AsyncMock()
    mock.setex = AsyncMock()
    mock.delete = AsyncMock()
    return mock


@pytest.fixture
def mock_app_config():
    return MagicMock()
