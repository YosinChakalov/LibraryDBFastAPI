from pydantic import BaseModel, Field, EmailStr


class PostSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Bla bla bla",
                "content": "Ble ble ble"
            }
        }


class UserSchema(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "yosin",
                "email": "yosin@example.com",
                "password": "1111"
            }
        }

class UserLoginSchema(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "yosin",
                "password": "1111"
            }
        }


class AuthorSchema(BaseModel):
    fullname: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Yosin Ghairatzoda"
            }
        }


class BookSchema(BaseModel):
    title: str
    description: str 
    author_id: int
    user_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "title": "test",
                "description": "description",
                "author_id": 1,
                "user_id": 1
            }
        }
