from typing import List, Union

from pydantic import BaseModel


class BoardLookup(BaseModel):
    board_rid: int


class BoardCreate(BaseModel):
    lv: int
    parent_rid: int
    subject: str
    content: str



class Board(BaseModel):
    name: str
    board_rid: int
    user_rid: int

    class Config:
        orm_mode = True


class BoardList(BaseModel):
    board_rid: int
    subject: str
    user_rid: str


class UserCreate(BaseModel):
    id: str
    password: str


class User(BaseModel):
    user_rid: int
    is_deleted: bool
    boards: List[Board] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    user_rid: int
    access_token: str


class TokenData(BaseModel):
    user_rid: Union[str, None] = None