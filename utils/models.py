from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from .db import Base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, Float


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True)
    email = Column(String)
    name = Column(String)
    picture = Column(String)


class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    title = Column(Text)
    url = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    author = Column(String)
    score = Column(Integer)
    url = Column(Text)
    comments = Column(Integer)


class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Cache(Base):
    __tablename__ = "cache"

    key = Column(String, primary_key=True)
    value = Column(Text)
    expires = Column(Float)