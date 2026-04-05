from __future__ import annotations

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from ..exceptions import NotFoundError
from ..repositories import NoteRepository
from ..schemas import CreateNoteRequest, NoteResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notes", tags=["notes"])


def get_note_repository() -> NoteRepository:
    """Dependency for getting NoteRepository instance."""
    return NoteRepository()


@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_note_endpoint(
    request: CreateNoteRequest,
    note_repo: NoteRepository = Depends(get_note_repository),
) -> NoteResponse:
    """Create a new note.

    Args:
        request: Create note request with content.
        note_repo: Note repository for database operations.

    Returns:
        NoteResponse: Response with created note data.
    """
    try:
        logger.info("Creating new note")
        note_id = note_repo.create(request.content)
        note = note_repo.get_by_id(note_id)

        if note is None:
            raise NotFoundError("note", note_id)

        logger.info(f"Created note with ID {note_id}")
        return NoteResponse(
            id=note.id, content=note.content, created_at=note.created_at.isoformat()
        )
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    except Exception as e:
        logger.error(f"Error creating note: {e}")
        raise


@router.get("/{note_id}", response_model=NoteResponse, status_code=status.HTTP_200_OK)
def get_note_endpoint(
    note_id: int,
    note_repo: NoteRepository = Depends(get_note_repository),
) -> NoteResponse:
    """Get a note by ID.

    Args:
        note_id: ID of the note to retrieve.
        note_repo: Note repository for database operations.

    Returns:
        NoteResponse: Response with note data.
    """
    try:
        logger.info(f"Retrieving note with ID {note_id}")
        note = note_repo.get_by_id(note_id)

        if note is None:
            raise NotFoundError("note", note_id)

        logger.info(f"Retrieved note with ID {note_id}")
        return NoteResponse(
            id=note.id, content=note.content, created_at=note.created_at.isoformat()
        )
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    except Exception as e:
        logger.error(f"Error retrieving note: {e}")
        raise


@router.get("", response_model=List[NoteResponse], status_code=status.HTTP_200_OK)
def list_notes_endpoint(
    note_repo: NoteRepository = Depends(get_note_repository),
) -> list[NoteResponse]:
    """List all notes.

    Args:
        note_repo: Note repository for database operations.

    Returns:
        List[NoteResponse]: List of notes ordered by creation time descending.
    """
    try:
        logger.info("Listing all notes")
        notes = note_repo.list_all()

        return [
            NoteResponse(id=note.id, content=note.content, created_at=note.created_at.isoformat())
            for note in notes
        ]
    except Exception as e:
        logger.error(f"Error listing notes: {e}")
        raise
