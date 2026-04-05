"""Pydantic schemas for API contracts and data models."""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


# ==================== Database Models ====================

class Note(BaseModel):
    """Database model for a note."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    created_at: datetime


class ActionItem(BaseModel):
    """Database model for an action item."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: datetime


# ==================== Request Schemas ====================

class ExtractRequest(BaseModel):
    """Request schema for extracting action items."""

    text: str = Field(..., min_length=1, description="Note text to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save the note")
    use_llm: bool = Field(default=False, description="Whether to use LLM for extraction")


class CreateNoteRequest(BaseModel):
    """Request schema for creating a note."""

    content: str = Field(..., min_length=1, description="Content of the note")


class MarkDoneRequest(BaseModel):
    """Request schema for marking an action item as done."""

    done: bool = Field(default=True, description="Whether the action item is done")


# ==================== Response Schemas ====================

class ExtractItemResponse(BaseModel):
    """Response schema for a single extracted action item."""

    id: int = Field(..., description="ID of the action item")
    text: str = Field(..., description="Text of the action item")


class ExtractResponse(BaseModel):
    """Response schema for action item extraction."""

    note_id: Optional[int] = Field(default=None, description="ID of the saved note, if any")
    items: List[ExtractItemResponse] = Field(default_factory=list, description="Extracted action items")


class NoteResponse(BaseModel):
    """Response schema for a note."""

    id: int = Field(..., description="ID of the note")
    content: str = Field(..., description="Content of the note")
    created_at: str = Field(..., description="Creation timestamp of the note")


class ActionItemResponse(BaseModel):
    """Response schema for an action item."""

    id: int = Field(..., description="ID of the action item")
    note_id: Optional[int] = Field(default=None, description="ID of the associated note")
    text: str = Field(..., description="Text of the action item")
    done: bool = Field(default=False, description="Whether the action item is done")
    created_at: str = Field(..., description="Creation timestamp of the action item")


class MarkDoneResponse(BaseModel):
    """Response schema for marking an action item as done."""

    id: int = Field(..., description="ID of the action item")
    done: bool = Field(..., description="Whether the action item is done")
