
from typing import Union
from datetime import datetime, timedelta

from jose import jwt

from sqlalchemy.orm import Session, aliased
from sqlalchemy import Table, Column, Text, Integer, MetaData, select, cast, String, func, literal, asc, desc

import schemas, SETTING
from models import User, Board

from fastapi import HTTPException, status
from SETTING import ACCESS_TOKEN_EXPIRE_MINUTES


def get_user_by_user_rid(db: Session, user_rid: int):
    return db.query(User).filter(User.user_rid == user_rid).first()


def get_user_by_id(db: Session, id: str):
    return db.query(User).filter(User.id == id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).seleoffset(skip).limit(limit).all()


def get_boards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Board.board_rid, Board.subject, Board.user_rid, Board.created_date, User.nickname).filter(Board.lv == 0).where(Board.user_rid == User.user_rid).order_by(desc(Board.created_date)).offset(skip).limit(limit).all()

def get_board_by_id(db :Session, board_rid: int):
    return db.query(Board.user_rid, Board.content, Board.board_rid, Board.subject, Board.created_date, User.nickname).where(Board.user_rid == User.user_rid).filter(Board.board_rid == board_rid).first()

def get_comments(db: Session, board_rid, skip: int = 0, limit: int = 100):
    return db.execute(f'WITH RECURSIVE CTS AS ( SELECT board_rid, SUBJECT, content, lv, parent_rid, CAST(board_rid as CHAR(100)) depth, 0 LEVEL, created_date, user_rid urid FROM board_tbl WHERE parent_rid = { board_rid } UNION ALL SELECT b.board_rid, b.SUBJECT, b.content, b.lv, b.parent_rid, CONCAT(c.depth, ",", b.board_rid) depth, (c.level + 1) LEVEL, c.created_date, user_rid urid FROM board_tbl b INNER JOIN CTS c ON b.parent_rid = c.board_rid ) SELECT board_rid, subject, parent_rid, content, lv, depth, LEVEL, created_date, user_rid, nickname from CTS LEFT JOIN user_tbl ON urid = user_rid ORDER BY depth').all()
    # one = select(Board.board_rid, Board.subject, Board.lv, Board.parent_rid, cast(Board.board_rid, String(100)).label("depth")).where(Board.parent_rid == board_rid)
    
    # two = select(Board.board_rid, Board.subject, Board.lv, Board.parent_rid '''func.concat(c.depth, ',', Board.board_rid''').label("depth")
    '''
    one = select(Board.board_rid, Board.subject, Board.lv, Board.parent_rid).where(Board.parent_rid == board_rid).cte(recursive=True) #, name="recursive_franchisee")
    two = select(Board.board_rid, Board.subject, Board.lv, Board.parent_rid)

    ralias = aliased(one, name="R")
    lalias = aliased(two, name="L")

    one = one.union_all(
        db.query(lalias.board_rid).join(ralias, ralias.c.board_rid == lalias.parent_rid)
    )


    r = db.query(one).all()
    return r
    print("rrrrrrrrrr", r)
    '''
    # SELECT board_rid, SUBJECT, lv, parent_rid, CAST(board_rid as CHAR(100)) depth
    # FROM board_tbl

    # st = db.query(Board, User.user_rid).join(User, Board.board_rid == User.user_rid).all()
    # return st
    # Board.user_rid, Board.content, Board.subject, Board.board_rid, Board.created_date
    
    hierarchy = db.query(
            Board, cast(Board.board_rid, String(100)).label('depth'), literal(1).label('level'))\
            .filter(Board.parent_rid == board_rid)\
            .cte(name="hierarchy", recursive=True)

    parent = aliased(hierarchy, name="p")
    children = aliased(Board, name="c")

    hierarchy = hierarchy.union_all(
                db.query(
                    children,
                    func.concat(parent.c.depth, '-', children.board_rid).label("depth"),
                    (parent.c.level + 1).label("level"))
                .filter(children.parent_rid == parent.c.board_rid))
    # .order_by(asc(hierarchy.c.depth)).all()
    result = db.query(Board, hierarchy.c.depth, hierarchy.c.level, Board.board_rid).select_entity_from(hierarchy).all()
    return result

def fake_hash_password(password: str):
    return "fakehashed" + password


def create_user(db: Session, user: schemas.UserCreate):
    db_user = User(id=user.id, password=fake_hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_board(db: Session, board: schemas.BoardCreate, user_rid: int):
    db_board = Board(**board.__dict__, user_rid=user_rid)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return {'code': 1}


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SETTING.SECRET_KEY, algorithm=SETTING.ALGORITHM)
    return encoded_jwt


def user_password_login_or_create(db: Session, user: schemas.UserCreate):
    user_db = get_user_by_id(db, user.id)
    if user_db:
        if fake_hash_password(user.password) == user_db.password:
            return [create_access_token({'user_rid': user_db.user_rid}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)), user_db.user_rid]
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="password is not correct")
    else:
        user_db = create_user(db, user)
        return [create_access_token({'user_rid': user_db.user_rid}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)), user_db.user_rid]