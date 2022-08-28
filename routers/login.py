from datetime import timedelta

from fastapi import Depends, HTTPException, Request, status, APIRouter
from sqlalchemy.orm import Session

import schemas
from dependencies import get_db
from services import user_password_login_or_create

import requests

router = APIRouter()


@router.post("/password", name = '패스워드 회원가입 또는 로그인', tags=['로그인'], response_model=schemas.Token)
def login_for_access_token(item: schemas.UserCreate, db: Session = Depends(get_db)):

    ret = user_password_login_or_create(db, item)

    return {"user_rid": ret[1], "access_token": ret[0]}