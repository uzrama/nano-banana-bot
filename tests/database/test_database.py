import pytest
from nano_banana_bot.models.user import User


@pytest.mark.asyncio
async def test_user_lifecycle(sql_context):
    async with sql_context as (db, uow):
        # 1. Create a user
        new_user = User(name="Test User", language="ru", language_code="ru")
        await uow.commit(new_user)
        user_id = new_user.id

    async with sql_context as (db, uow):
        # 2. Get a user
        user = await db.users.get(user_id)
        assert user is not None
        assert user.name == "Test User"
        assert user.language == "ru"

        # 3. Update a user
        updated_user = await db.users.update(user_id, name="Updated Name")
        assert updated_user.name == "Updated Name"

        # Check that the database has not been updated yet (no commit)
        # To do this, we need to create a new session via db_context
        # But since SQLite is in-memory, we need to use the same database.
        # In this test, we verify the update after a commit.
        await uow.commit()

    async with sql_context as (db, uow):
        # 4. Verify after commit
        user = await db.users.get(user_id)
        assert user.name == "Updated Name"

        # 5. Count users
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
