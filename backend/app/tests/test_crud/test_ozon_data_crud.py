from app import crud
from app.core.config import settings
from app.schemas.ozon_data_schema import IOzonDataCreate, IOzonDataUpdate
from app.tests.utils.user import create_random_user


async def test_update_ozon_data(client, async_session_test, superuser_token_headers):
    ozon_data = IOzonDataUpdate()
    ozon_data.client_id = "12"
    ozon_data.api_key = "122"
    user = await crud.user.get_by_email(
        db_session=async_session_test, email=settings.FIRST_SUPERUSER_EMAIL
    )
    role = await crud.ozon_data.update_credentials(
        update_params=ozon_data,
        obj_in=user.ozon_confidential,
        db_session=async_session_test,
    )
    assert role
    assert role.api_key == ozon_data.api_key


async def test_get_by_user_id(client, async_session_test, superuser_token_headers):
    user = await crud.user.get_by_email(
        db_session=async_session_test, email=settings.FIRST_SUPERUSER_EMAIL
    )
    ozon_data = await crud.ozon_data.get_by_user_id(
        id=user.id, db_session=async_session_test
    )
    assert ozon_data
    assert ozon_data.user_id == user.id


async def test_create_credential(client, async_session_test, superuser_token_headers):
    user, pswd = await create_random_user(db=async_session_test)
    od = IOzonDataCreate(api_key="12", client_id="1111")
    await crud.ozon_data.create_credentials(
        id=user.id, db_session=async_session_test, obj_in=od
    )


#     async def create_credentials(
#         self,
#         *,
#         id: UUID,
#         obj_in: IOzonDataCreate,
#         db_session: AsyncSession | None = None,
#     ) -> OzonData:
#         db_session = db_session or self.db.session
#         db_obj = OzonData.model_validate(obj_in, update={"user_id": id})
#
#         obj_out = db_obj.copy()
#         db_obj.api_key = await security.get_data_encrypt(obj_in.api_key)
#         db_session.add(db_obj)
#         await db_session.commit()
#         await db_session.refresh(db_obj)
#         return obj_out
