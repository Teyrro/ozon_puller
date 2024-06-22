from app import crud
from app.schemas.role_schema import IRoleEnum
from app.tests.utils.user import create_random_user


async def test_get_role_by_name(client, async_session_test, superuser_token_headers):
    role = await crud.role.get_role_by_name(
        name=IRoleEnum.user, db_session=async_session_test
    )
    assert role


async def test_add_role_to_user(client, async_session_test, superuser_token_headers):
    role = await crud.role.get_role_by_name(
        name=IRoleEnum.manager, db_session=async_session_test
    )
    user, pswd = await create_random_user(db=async_session_test)
    role = await crud.role.add_role_to_user(
        db_session=async_session_test, role_id=role.id, user=user
    )
    assert role
