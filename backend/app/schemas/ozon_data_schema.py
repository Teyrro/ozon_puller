from uuid import UUID

from app.models.ozon_data_model import OzonDataBase, OzonDataWithUserID
from app.utils.partial import partial_model


class IOzonDataCreate(OzonDataBase):
    pass


@partial_model
class IOzonDataUpdate(OzonDataBase):
    pass


class IOzonDataRead(OzonDataWithUserID):
    id: UUID


@partial_model
class IOzonDataUpdateWithId(OzonDataBase):
    pass
