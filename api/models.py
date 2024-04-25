import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, constr, field_validator
from starlette import status

LETTER_MATCH_PATTERN = re.compile(r'^[а-яА-Яa-zA-Z\-]+$')


class TunedModel(BaseModel):
	"""tells pydantic to convert even non dict obj to json"""

	model_config = ConfigDict(from_attributes=True)


class ShowUser(TunedModel):
	user_id: uuid.UUID
	name: str
	surname: str
	email: EmailStr
	is_active: bool


class UserCreate(BaseModel):
	name: str
	surname: str
	email: EmailStr

	@field_validator('name')
	@classmethod
	def validate_name(cls, value):
		if not LETTER_MATCH_PATTERN.match(value):
			raise HTTPException(
				status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
				detail='Name should contains only letters, numbers',
			)
		return value

	@field_validator('surname')
	@classmethod
	def validate_surname(cls, value):
		if not LETTER_MATCH_PATTERN.match(value):
			raise HTTPException(
				status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
				detail='Surname should contains only letters, numbers',
			)
		return value


class DeleteUserResponse(BaseModel):
	deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
	updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
	name: constr(min_length=1) | None = None
	surname: constr(min_length=1) | None = None
	email: EmailStr | None = None

	@field_validator('name')
	@classmethod
	def validate_name(cls, value):
		if not LETTER_MATCH_PATTERN.match(value):
			raise HTTPException(status_code=422, detail='Name should contains only letters')
		return value

	@field_validator('surname')
	@classmethod
	def validate_surname(cls, value):
		if not LETTER_MATCH_PATTERN.match(value):
			raise HTTPException(status_code=422, detail='Surname should contains only letters')
		return value
