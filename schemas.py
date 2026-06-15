from pydantic import BaseModel


class EntryCreate(BaseModel):
    content: str


class EntryResponse(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
