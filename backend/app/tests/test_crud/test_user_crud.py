from app import crud
from app.schemas.role_schema import IRoleEnum
from app.schemas.user_schema import IUserCreate, IUserUpdate, IUserUpdateMe
from app.tests.utils.user import create_random_user


async def test_active_user(client, async_session_test, superuser_token_headers):
    user, pswd = await create_random_user(db=async_session_test)
    user_out = await crud.user.get_by_id_active(
        id=user.id, db_session=async_session_test
    )
    assert user_out.is_active == user.is_active


async def get_by_email(client, async_session_test):
    user, pswd = await create_random_user(db=async_session_test)
    user_out = await crud.user.get_by_email(
        email=user.email, db_session=async_session_test
    )
    assert user_out.email == user.email


async def test_update_user_me(client, async_session_test):
    user, pswd = await create_random_user(db=async_session_test)
    user_in = IUserUpdateMe()
    user_in.name = "chachacha"
    user_out = await crud.user.update_user_me(
        obj_in=user, user=user, db_session=async_session_test
    )
    assert user_out.email == user.email


async def test_update_from_admin_role(client, async_session_test):
    user, pswd = await create_random_user(db=async_session_test)
    user_in = IUserUpdate()
    user_in.password = "123"
    user_in.name = "chachacha"

    user_out = await crud.user.update_from_admin_role(
        obj_in=user_in, user=user, db_session=async_session_test
    )
    assert user_out != user_in.password
    assert user_out.name == "chachacha"


async def test_create_with_role(client, async_session_test):
    user, pswd = await create_random_user(db=async_session_test)
    role = await crud.role.get_role_by_name(
        name=IRoleEnum.manager, db_session=async_session_test
    )
    user_in = IUserCreate(
        name="chachacha",
        surname="chichichi",
        is_active=False,
        email="email@chachacha.com",
        role_id=role.id,
        password="123",
    )
    user_out = await crud.user.create_with_role(
        obj_in=user_in, db_session=async_session_test
    )
    assert user_out.role != user_in.password
    assert user_out.name == user_in.name


async def test_authenticate(client, async_session_test):
    user, pswd = await create_random_user(db=async_session_test)
    user = await crud.user.authenticate(
        email=user.email, password=pswd, db_session=async_session_test
    )
    assert user


async def test_remove(client, async_session_test):
    user, pswd = await create_random_user(db=async_session_test)
    user = await crud.user.remove(id=user.id, db_session=async_session_test)
    assert user


async def test_get_admin_id(client, async_session_test):
    id = await crud.user.get_admin_id(db_session=async_session_test)
    assert id


async def test_get_all_id(client, async_session_test):
    ids = await crud.user.get_all_id(db_session=async_session_test)
    assert ids
