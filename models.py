from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import DateTime

import datetime

class User(Base):
    __tablename__ = "user_tbl"

    user_rid = Column(Integer, primary_key=True, index=True)
    id = Column(String(100), index=True, unique=True, nullable=False)
    password = Column(String(100), index=True, nullable=False)
    nickname = Column(String(100), default="", nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    boards = relationship("Board", back_populates="owner")


class Board(Base):
    __tablename__ = "board_tbl"

    board_rid = Column(Integer, primary_key=True, index=True, nullable=False)
    user_rid = Column(Integer, ForeignKey("user_tbl.user_rid"))
    parent_rid = Column(Integer, ForeignKey("board_tbl.board_rid"), default=None)
    subject = Column(String(100), nullable=False)
    content = Column(Text, default="", nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    lv = Column(Integer, default=0, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now, nullable=False)

    owner = relationship("User", back_populates="boards")