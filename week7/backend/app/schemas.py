from datetime import datetime

from pydantic import BaseModel, field_validator


class NoteCreate(BaseModel):
    title: str
    content: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        if not 1 <= len(v) <= 200:
            raise ValueError("title must be between 1 and 200 characters")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str) -> str:
        if len(v) < 1:
            raise ValueError("content must be at least 1 character")
        return v


class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NotePatch(BaseModel):
    title: str | None = None
    content: str | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str | None) -> str | None:
        if v is not None and not 1 <= len(v) <= 200:
            raise ValueError("title must be between 1 and 200 characters")
        return v

    @field_validator("content")
    @classmethod
    def validate_content(cls, v: str | None) -> str | None:
        if v is not None and len(v) < 1:
            raise ValueError("content must be at least 1 character")
        return v


class ActionItemCreate(BaseModel):
    description: str

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        if not 1 <= len(v) <= 1000:
            raise ValueError("description must be between 1 and 1000 characters")
        return v


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ActionItemPatch(BaseModel):
    description: str | None = None
    completed: bool | None = None

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        if v is not None and not 1 <= len(v) <= 1000:
            raise ValueError("description must be between 1 and 1000 characters")
        return v
