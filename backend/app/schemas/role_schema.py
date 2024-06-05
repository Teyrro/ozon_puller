from enum import Enum
from uuid import UUID

from app.models.role_model import RoleBase
from app.utils.partial import partial_model


class IRoleCreate(RoleBase):
    pass


# All these fields are optional
@partial_model
class IRoleUpdate(RoleBase):
    pass


class IRoleRead(RoleBase):
    id: UUID


class IRoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    user = "user"
