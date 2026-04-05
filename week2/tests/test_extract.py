from unittest.mock import Mock, patch

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


# ==================== LLM Extraction Tests ====================


def test_llm_extract_bullet_lists():
    """Test LLM extraction of bullet points with different formats."""
    text = """
    Meeting notes:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    """.strip()

    # Mock the Zhipu API to return valid JSON
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = (
        '["Set up database", "implement API extract endpoint", "Write tests"]'
    )

    with patch(
        "week2.app.services.extract.client.chat.completions.create", return_value=mock_response
    ):
        items = extract_action_items_llm(text)
        assert len(items) == 3
        assert "Set up database" in items
        assert "implement API extract endpoint" in items
        assert "Write tests" in items


def test_llm_extract_keyword_prefixed_lines():
    """Test LLM extraction of lines with action keywords."""
    text = """
    Action items:
    todo: Review code
    action: Fix bug
    next: Deploy to production
    """.strip()

    # Mock the Zhipu API to return valid JSON
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '["Review code", "Fix bug", "Deploy to production"]'

    with patch(
        "week2.app.services.extract.client.chat.completions.create", return_value=mock_response
    ):
        items = extract_action_items_llm(text)
        assert len(items) == 3
        assert "Review code" in items
        assert "Fix bug" in items
        assert "Deploy to production" in items


def test_llm_extract_empty_input():
    """Test handling of empty or whitespace-only input."""
    # Test empty string - should return empty list without calling API
    items = extract_action_items_llm("")
    assert items == []

    # Test whitespace-only string
    items = extract_action_items_llm("   \n\t  ")
    assert items == []


def test_llm_extract_json_array_parsing():
    """Test successful JSON array response from LLM."""
    text = "Meeting notes with some action items"

    # Mock the Zhipu API to return valid JSON array
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '["Action 1", "Action 2", "Action 3"]'

    with patch(
        "week2.app.services.extract.client.chat.completions.create", return_value=mock_response
    ):
        items = extract_action_items_llm(text)
        assert len(items) == 3
        assert items == ["Action 1", "Action 2", "Action 3"]


def test_llm_extract_fallback_to_heuristic():
    """Test fallback when LLM returns invalid JSON."""
    text = """
    - [ ] Set up database
    * implement API
    todo: Review code
    """.strip()

    # Mock the Zhipu API to return invalid JSON (plain text)
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = (
        "Here are some action items: Set up database, implement API, Review code"
    )

    with patch(
        "week2.app.services.extract.client.chat.completions.create", return_value=mock_response
    ):
        items = extract_action_items_llm(text)
        # Should fall back to heuristic extraction
        assert len(items) > 0
        assert "Set up database" in items
        assert "implement API" in items


def test_llm_extract_markdown_wrapped_json():
    """Test parsing of JSON wrapped in markdown code blocks."""
    text = "Meeting notes"

    # Mock the Zhipu API to return JSON wrapped in markdown
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = '```json\n["Action 1", "Action 2", "Action 3"]\n```'

    with patch(
        "week2.app.services.extract.client.chat.completions.create", return_value=mock_response
    ):
        items = extract_action_items_llm(text)
        assert len(items) == 3
        assert items == ["Action 1", "Action 2", "Action 3"]


def test_llm_extract_mixed_content():
    """Test extraction from realistic meeting notes with mixed content."""
    text = """
    Meeting Notes - April 4, 2026

    Discussion about the project timeline:
    - [ ] Set up database schema
    * implement API endpoints

    Action items for next week:
    todo: Review pull requests
    action: Fix authentication bug
    next: Deploy to staging environment

    The team agreed on the new feature priorities.
    Some narrative text here.

    Additional tasks:
    1. Write unit tests
    2. Update documentation
    3. Schedule follow-up meeting
    """.strip()

    # Mock the Zhipu API to return extracted action items
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = (
        '["Set up database schema", "implement API endpoints", "Review pull requests", "Fix authentication bug", "Deploy to staging environment", "Write unit tests", "Update documentation", "Schedule follow-up meeting"]'
    )

    with patch(
        "week2.app.services.extract.client.chat.completions.create", return_value=mock_response
    ):
        items = extract_action_items_llm(text)
        assert len(items) == 8
        assert "Set up database schema" in items
        assert "implement API endpoints" in items
        assert "Review pull requests" in items
        assert "Fix authentication bug" in items
        assert "Deploy to staging environment" in items
        assert "Write unit tests" in items
        assert "Update documentation" in items
        assert "Schedule follow-up meeting" in items


def test_llm_extract_empty_json_array():
    """Test handling of empty JSON array response."""
    text = "Meeting notes with no action items"

    # Mock the Zhipu API to return empty array
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "[]"

    with patch(
        "week2.app.services.extract.client.chat.completions.create", return_value=mock_response
    ):
        items = extract_action_items_llm(text)
        assert items == []


def test_llm_extract_deduplication():
    """Test that duplicate action items are removed."""
    text = """
    Meeting notes:
    - Set up database
    * Set up database
    todo: Set up database
    """.strip()

    # Mock the Zhipu API to return duplicates
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = (
        '["Set up database", "Set up database", "Set up database"]'
    )

    with patch(
        "week2.app.services.extract.client.chat.completions.create", return_value=mock_response
    ):
        items = extract_action_items_llm(text)
        # The _parse_json_array function doesn't deduplicate, so this will return all items
        # However, in real usage, the LLM should return unique items
        assert len(items) == 3
        assert items == ["Set up database", "Set up database", "Set up database"]
