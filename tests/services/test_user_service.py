import pytest
from unittest.mock import MagicMock
from aiogram.types import User as AiogramUser
from nano_banana_bot.services.crud.user import UserService
from nano_banana_bot.schemas.user import UserScheme


@pytest.fixture
def user_service(session_pool, mock_redis, mock_app_config):
    return UserService(session_pool=session_pool, redis=mock_redis, config=mock_app_config)


@pytest.fixture
def mock_i18n():
    mock = MagicMock()
    mock.available_locales = ["en", "ru"]
    return mock


@pytest.mark.asyncio
async def test_create_user(user_service, mock_i18n, mock_redis):
    aiogram_user = AiogramUser(id=123, is_bot=False, first_name="Test", last_name="User", language_code="ru")

    user_scheme = await user_service.create(aiogram_user, mock_i18n)

    assert user_scheme.id == 123
    assert user_scheme.name == "Test User"
    assert user_scheme.language == "ru"

    # Verify it was added to DB
    db_user = await user_service.get(123)
    assert db_user is not None
    assert db_user.name == "Test User"

    # Verify cache was cleared
    assert mock_redis.delete.called


@pytest.mark.asyncio
async def test_get_user_not_found(user_service):
    user = await user_service.get(999)
    assert user is None


@pytest.mark.asyncio
async def test_update_user(user_service, mock_i18n, mock_redis):
    # First create
    aiogram_user = AiogramUser(id=456, is_bot=False, first_name="Original", language_code="en")
    await user_service.create(aiogram_user, mock_i18n)

    # Then update
    user_scheme = await user_service.get(456)
    updated_scheme = await user_service.update(user_scheme, name="New Name")

    assert updated_scheme.name == "New Name"

    # Verify in DB
    db_user = await user_service.get(456)
    assert db_user.name == "New Name"

    # Verify cache was cleared (at least twice: once in create, once in update)
    assert mock_redis.delete.call_count >= 2


@pytest.mark.asyncio
async def test_count_users(user_service, mock_i18n):
    initial_count = await user_service.count()

    aiogram_user = AiogramUser(id=789, is_bot=False, first_name="Counter", language_code="en")
    await user_service.create(aiogram_user, mock_i18n)

    new_count = await user_service.count()
    assert new_count == initial_count + 1
