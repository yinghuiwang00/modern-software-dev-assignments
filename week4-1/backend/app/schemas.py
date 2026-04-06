from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteRead(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    description: str


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool

    class Config:
        from_attributes = True


class ExtractResponse(BaseModel):
    note_id: int
    note_content: str
    extracted_items: list[dict]


class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
