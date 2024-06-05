from typing import Any

from fastapi import HTTPException, status


class UserSelfDeleteException(HTTPException):
    def __init__(
        self,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Users can not delete theirselfs.",
            headers=headers,
        )
