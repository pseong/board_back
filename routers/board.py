from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

import schemas
from dependencies import get_db, get_current_active_user
from services import create_board, get_boards, get_comments, get_board_by_id
from models import User

router = APIRouter()

@router.post("/create", name = '개인 게시글 생성', tags=['게시글'],
            description='생성된 게시글 반환')
def create_board_for_user(board: schemas.BoardCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return create_board(db=db, board=board, user_rid=current_user.user_rid)


@router.get("", name = '모든 게시글', tags=['게시글'],
            description='모든 게시글 반환')
def read_boards(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    boards = get_boards(db, skip=skip, limit=limit)

    return boards


@router.post("/detail", name = '특정 게시글 댓글', tags=['게시글'],
            description='특정 게시글 댓글 반환')
def read_boards(item: schemas.BoardLookup, skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    board = get_board_by_id(db, item.board_rid)
    comments = get_comments(db, item.board_rid, skip=skip, limit=limit)
    return { 'board': board, 'comments': comments }