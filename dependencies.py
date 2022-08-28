from typing import List

from fastapi import Depends, HTTPException, status, WebSocket
from jose import JWTError, jwt
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer

from sqlalchemy.orm import Session

import schemas
from database import SessionLocal
from models import User
from SETTING import SECRET_KEY, ALGORITHM
from services import get_user_by_user_rid


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="token", authorizationUrl="authorization")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_rid: str = payload.get("user_rid")
        if user_rid is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_rid=user_rid)
    except JWTError:
        raise credentials_exception
    print(token_data.user_rid)
    user = get_user_by_user_rid(db, token_data.user_rid)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_deleted:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def anything(self):
        for connection in self.active_connections:
            try:
                pass
            except:
                pass

manager = ConnectionManager()

def get_connection():
    return manager