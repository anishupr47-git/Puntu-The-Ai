from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Date
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.sql import func
from .core.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Memory(Base):
    __tablename__ = 'memories'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    text = Column(Text, nullable=False)
    embedding = Column(ARRAY(Float), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ModuleLog(Base):
    __tablename__ = 'module_logs'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    module = Column(String(50), nullable=False)
    input = Column(JSONB, nullable=True)
    output = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    title = Column(String(140), nullable=False)
    artist = Column(String(140), nullable=False)
    mood = Column(String(40), nullable=False)
    energy = Column(String(10), nullable=False)
    genre = Column(String(40), nullable=False)
    era = Column(String(10), nullable=False)
    tags = Column(ARRAY(String), nullable=False)


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    title = Column(String(140), nullable=False)
    year = Column(Integer, nullable=False)
    mood = Column(String(40), nullable=False)
    energy = Column(String(10), nullable=False)
    genre = Column(String(40), nullable=False)
    era = Column(String(10), nullable=False)
    tags = Column(ARRAY(String), nullable=False)
    synopsis = Column(Text, nullable=False)


class Club(Base):
    __tablename__ = 'clubs'

    id = Column(Integer, primary_key=True, index=True)
    league = Column(String(80), nullable=False)
    country = Column(String(80), nullable=False)
    season = Column(String(20), nullable=False)
    team = Column(String(120), nullable=False, index=True)


class NationalTeam(Base):
    __tablename__ = 'national_teams'

    id = Column(Integer, primary_key=True, index=True)
    confederation = Column(String(20), nullable=False)
    team = Column(String(120), nullable=False, index=True)


class FootballMatch(Base):
    __tablename__ = 'football_matches'

    id = Column(Integer, primary_key=True, index=True)
    season = Column(String(20), nullable=False)
    league = Column(String(80), nullable=False)
    date = Column(Date, nullable=False)
    home_team = Column(String(120), nullable=False, index=True)
    away_team = Column(String(120), nullable=False, index=True)
    home_goals = Column(Integer, nullable=False)
    away_goals = Column(Integer, nullable=False)
