from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware

import SETTING
SETTING.init()

from routers import login, user, board, wsocket
from database import Base, engine

def include_router(app):
    app.include_router(login.router, prefix='/login')
    app.include_router(user.router, prefix='/users')
    app.include_router(board.router, prefix='/boards')

def start_application():
    app = FastAPI()
    include_router(app)
    Base.metadata.create_all(bind=engine)
    origins = [
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app

app = start_application()