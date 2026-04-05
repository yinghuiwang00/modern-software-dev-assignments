from __future__ import annotations

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from ..exceptions import NotFoundError, ServiceError
from ..repositories import ActionItemRepository, NoteRepository
from ..schemas import (
    ActionItemResponse,
    ExtractItemResponse,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
    MarkDoneResponse,
)
from ..services.extract import extract_action_items, extract_action_items_llm

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/action-items", tags=["action-items"])


def get_note_repository() -> NoteRepository:
    """Dependency for getting NoteRepository instance."""
    return NoteRepository()


def get_action_item_repository() -> ActionItemRepository:
    """Dependency for getting ActionItemRepository instance."""
    return ActionItemRepository()


@router.post("/extract", response_model=ExtractResponse, status_code=status.HTTP_200_OK)
def extract_action_items_endpoint(
    request: ExtractRequest,
    action_item_repo: ActionItemRepository = Depends(get_action_item_repository),
    note_repo: NoteRepository = Depends(get_note_repository),
) -> ExtractResponse:
    """Extract action items from note text.

    Args:
        request: Extract request with text, save_note, and use_llm flags.
        action_item_repo: Action item repository for database operations.
        note_repo: Note repository for saving notes.

    Returns:
        ExtractResponse: Response with note ID and extracted action items.
    """
    try:
        logger.info(f"Extracting action items from text (LLM: {request.use_llm})")

        # Save note if requested
        note_id: int | None = None
        if request.save_note:
            note_id = note_repo.create(request.text)
            logger.info(f"Saved note with ID {note_id}")

        # Extract action items
        try:
            if request.use_llm:
                items = extract_action_items_llm(request.text)
            else:
                items = extract_action_items(request.text)
        except Exception as e:
            logger.error(f"Failed to extract action items: {e}")
            raise ServiceError(f"Failed to extract action items: {str(e)}")

        # Save action items to database
        if items:
            item_ids = action_item_repo.create_many(items, note_id=note_id)
            logger.info(f"Created {len(item_ids)} action items")

        # Build response
        item_responses = [
            ExtractItemResponse(id=item_id, text=item_text)
            for item_id, item_text in zip(item_ids if items else [], items)
        ]

        return ExtractResponse(note_id=note_id, items=item_responses)
    except Exception as e:
        logger.error(f"Error in extract endpoint: {e}")
        raise


@router.post("/extract-llm", response_model=ExtractResponse, status_code=status.HTTP_200_OK)
def extract_action_items_llm_endpoint(
    request: ExtractRequest,
    action_item_repo: ActionItemRepository = Depends(get_action_item_repository),
    note_repo: NoteRepository = Depends(get_note_repository),
) -> ExtractResponse:
    """Extract action items from note text using LLM (dedicated endpoint).

    This endpoint always uses LLM-powered extraction for better separation of concerns.

    Args:
        request: Extract request with text and save_note flags.
        action_item_repo: Action item repository for database operations.
        note_repo: Note repository for saving notes.

    Returns:
        ExtractResponse: Response with note ID and extracted action items.
    """
    try:
        logger.info("Extracting action items from text using LLM (dedicated endpoint)")

        # Save note if requested
        note_id: int | None = None
        if request.save_note:
            note_id = note_repo.create(request.text)
            logger.info(f"Saved note with ID {note_id}")

        # Extract action items using LLM
        try:
            items = extract_action_items_llm(request.text)
        except Exception as e:
            logger.error(f"Failed to extract action items with LLM: {e}")
            raise ServiceError(f"Failed to extract action items with LLM: {str(e)}")

        # Save action items to database
        if items:
            item_ids = action_item_repo.create_many(items, note_id=note_id)
            logger.info(f"Created {len(item_ids)} action items")

        # Build response
        item_responses = [
            ExtractItemResponse(id=item_id, text=item_text)
            for item_id, item_text in zip(item_ids if items else [], items)
        ]

        return ExtractResponse(note_id=note_id, items=item_responses)
    except Exception as e:
        logger.error(f"Error in LLM extract endpoint: {e}")
        raise


@router.get("", response_model=List[ActionItemResponse], status_code=status.HTTP_200_OK)
def list_action_items_endpoint(
    note_id: int | None = None,
    action_item_repo: ActionItemRepository = Depends(get_action_item_repository),
) -> list[ActionItemResponse]:
    """List all action items, optionally filtered by note ID.

    Args:
        note_id: Optional note ID to filter action items.
        action_item_repo: Action item repository for database operations.

    Returns:
        List[ActionItemResponse]: List of action items.
    """
    try:
        logger.info(f"Listing action items (note_id: {note_id})")
        items = action_item_repo.list_all(note_id=note_id)

        return [
            ActionItemResponse(
                id=item.id,
                note_id=item.note_id,
                text=item.text,
                done=item.done,
                created_at=item.created_at.isoformat(),
            )
            for item in items
        ]
    except Exception as e:
        logger.error(f"Error listing action items: {e}")
        raise


@router.post(
    "/{action_item_id}/done", response_model=MarkDoneResponse, status_code=status.HTTP_200_OK
)
def mark_action_item_done_endpoint(
    action_item_id: int,
    request: MarkDoneRequest,
    action_item_repo: ActionItemRepository = Depends(get_action_item_repository),
) -> MarkDoneResponse:
    """Mark an action item as done or not done.

    Args:
        action_item_id: ID of the action item to update.
        request: Mark done request with done flag.
        action_item_repo: Action item repository for database operations.

    Returns:
        MarkDoneResponse: Response with action item ID and done status.
    """
    try:
        logger.info(f"Marking action item {action_item_id} as done={request.done}")
        updated = action_item_repo.update_done_status(action_item_id, request.done)

        if not updated:
            logger.warning(f"Action item {action_item_id} not found")
            raise NotFoundError("action_item", action_item_id)

        return MarkDoneResponse(id=action_item_id, done=request.done)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Action item not found")
    except Exception as e:
        logger.error(f"Error marking action item done: {e}")
        raise
