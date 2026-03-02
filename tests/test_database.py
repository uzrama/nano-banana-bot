import pytest
from nano_banana_bot.models.user import User


@pytest.mark.asyncio
async def test_user_lifecycle(sql_context):
    async with sql_context as (db, uow):
        # 1. Создание пользователя
        new_user = User(name="Test User", language="ru", language_code="ru")
        await uow.commit(new_user)
        user_id = new_user.id

    async with sql_context as (db, uow):
        # 2. Получение пользователя
        user = await db.users.get(user_id)
        assert user is not None
        assert user.name == "Test User"
        assert user.language == "ru"

        # 3. Обновление пользователя
        updated_user = await db.users.update(user_id, name="Updated Name")
        assert updated_user.name == "Updated Name"

        # Проверяем, что в базе еще не обновилось (нет коммита)
        # Для этого нужно создать новую сессию через db_context
        # Но так как SQLite in-memory, нам нужно использовать ту же базу.
        # В данном тесте мы проверим обновление после коммита.
        await uow.commit()

    async with sql_context as (db, uow):
        # 4. Проверка после коммита
        user = await db.users.get(user_id)
        assert user.name == "Updated Name"

        # 5. Подсчет пользователей
        count = await db.users.count()
        assert count == 1


@pytest.mark.asyncio
async def test_session_context_rollback(sql_context):
    try:
        async with sql_context as (db, uow):
            new_user = User(name="Ghost", language="en")
            db.users.session.add(new_user)
            raise ValueError("Trigger rollback")
    except ValueError:
        pass

    async with sql_context as (db, uow):
        count = await db.users.count()
        assert count == 0
