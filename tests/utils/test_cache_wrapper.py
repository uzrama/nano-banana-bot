import pytest
from unittest.mock import AsyncMock, MagicMock
from pydantic import BaseModel

from nano_banana_bot.database.redis.cache_wrapper import redis_cache
from nano_banana_bot.utils import mjson


class DummySchema(BaseModel):
    id: int
    name: str


class DummyService:
    def __init__(self, redis_client):
        self.redis = redis_client

    @redis_cache(prefix="dummy_get", ttl=60)
    async def get_dummy(self, item_id: int) -> DummySchema | None:
        # This is the actual function. It should only be called if there is no cache.
        if item_id == 1:
            return DummySchema(id=1, name="Real Data")
        return None

    @redis_cache(ttl=30)
    async def get_without_prefix(self, item_id: int, extra: str) -> DummySchema:
        return DummySchema(id=item_id, name=extra)


@pytest.fixture
def mock_redis_client():
    mock = AsyncMock()
    return mock


@pytest.fixture
def dummy_service(mock_redis_client):
    return DummyService(redis_client=mock_redis_client)


@pytest.mark.asyncio
async def test_redis_cache_miss_saves_to_redis(dummy_service, mock_redis_client):
    # Simulate Cache Miss (nothing in the cache)
    mock_redis_client.get.return_value = None

    # Call the method
    result = await dummy_service.get_dummy(1)

    # Check that the function was executed (returned real data)
    assert result is not None
    assert result.id == 1
    assert result.name == "Real Data"

    # Check that Redis attempted to get the key
    mock_redis_client.get.assert_called_once_with("cache:dummy_get:1")

    # Check that the result was saved in Redis
    # dump_python serializes the schema to a dictionary, and mjson encodes it to a string
    expected_json = mjson.encode({"id": 1, "name": "Real Data"})
    mock_redis_client.setex.assert_called_once_with("cache:dummy_get:1", 60, expected_json)


@pytest.mark.asyncio
async def test_redis_cache_hit_returns_from_redis(dummy_service, mock_redis_client):
    # Simulate Cache Hit (data exists in the cache)
    # Simulate a byte string typically returned by aioredis
    cached_data = mjson.encode({"id": 2, "name": "Cached Data"}).encode("utf-8")
    mock_redis_client.get.return_value = cached_data

    # We request item_id=2. If the actual get_dummy function was called,
    # it would return None (according to our implementation above).
    result = await dummy_service.get_dummy(2)

    # Check that data was taken exactly from the cache
    assert result is not None
    assert result.id == 2
    assert result.name == "Cached Data"

    # Check that the cache was read
    mock_redis_client.get.assert_called_once_with("cache:dummy_get:2")

    # Check that there were NO new records in Redis (setex was not called)
    mock_redis_client.setex.assert_not_called()


@pytest.mark.asyncio
async def test_redis_cache_miss_with_none_result(dummy_service, mock_redis_client):
    # Simulate Cache Miss
    mock_redis_client.get.return_value = None

    # Request a non-existent ID, the actual function will return None
    result = await dummy_service.get_dummy(99)

    assert result is None

    # Check that None was also saved in the cache (to avoid Cache Stampede)
    expected_json = mjson.encode(None)
    mock_redis_client.setex.assert_called_once_with("cache:dummy_get:99", 60, expected_json)


@pytest.mark.asyncio
async def test_redis_cache_key_generation_without_prefix(dummy_service, mock_redis_client):
    mock_redis_client.get.return_value = None

    await dummy_service.get_without_prefix(item_id=5, extra="test")

    # Check that the key was generated correctly (without a prefix, the function's __name__ is used)
    # cache:function_name:arg1:kwargs
    mock_redis_client.get.assert_called_once_with("cache:get_without_prefix:5:test")
