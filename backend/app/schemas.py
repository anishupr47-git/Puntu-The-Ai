from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Any, Optional


class EntryCreate(BaseModel):
    user_id: Optional[int] = None
    content: str = Field(..., min_length=1)


class EntryOut(BaseModel):
    id: int
    user_id: Optional[int]
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MemoryCreate(BaseModel):
    user_id: Optional[int] = None
    text: str = Field(..., min_length=1)


class MemoryOut(BaseModel):
    id: int
    user_id: Optional[int]
    text: str
    embedding: list[float]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MemorySearch(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(5, ge=1, le=20)


class ModuleLogCreate(BaseModel):
    user_id: Optional[int] = None
    module: str = Field(..., min_length=1)
    input: Optional[dict[str, Any]] = None
    output: Optional[dict[str, Any]] = None


class SongOut(BaseModel):
    id: int
    code: str
    title: str
    artist: str
    mood: str
    energy: str
    genre: str
    era: str
    tags: list[str]

    model_config = ConfigDict(from_attributes=True)


class MovieOut(BaseModel):
    id: int
    code: str
    title: str
    year: int
    mood: str
    energy: str
    genre: str
    era: str
    tags: list[str]
    synopsis: str

    model_config = ConfigDict(from_attributes=True)


class AgentRequest(BaseModel):
    message: str = Field(..., min_length=1)
    skill: Optional[str] = None
    mode: Optional[str] = None
    context: Optional[dict[str, Any]] = None
    user_id: Optional[int] = None


class AgentResponse(BaseModel):
    skill: str
    result: Any


class LLMRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    system: Optional[str] = None
    temperature: float = Field(0.6, ge=0.0, le=2.0)


class LLMWarmRequest(BaseModel):
    prompt: str = Field('Hello')


class FootballRequest(BaseModel):
    home_team: str = Field(..., min_length=1)
    away_team: str = Field(..., min_length=1)
