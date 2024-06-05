from pydantic import BaseModel

from app.models.ozon_data_model import OzonDataBase
from app.utils.partial import partial_model


class IOzonDataCreate(OzonDataBase):
    pass


@partial_model
class IOzonDataUpdate(OzonDataBase):
    pass


class TypeProduct(BaseModel):
    type_name: str
    type_id: int
    disabled: bool
    children: list


class DescriptionSubCategory(BaseModel):
    description_category_id: int
    category_name: str
    disabled: bool
    children: list[TypeProduct]


class DescriptionCategory(BaseModel):
    description_category_id: int
    category_name: str
    disabled: bool
    children: list[DescriptionSubCategory]
