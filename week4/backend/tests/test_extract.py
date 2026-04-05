from backend.app.services.extract import (
    extract_action_items,
    extract_action_items_with_tags,
    extract_tags,
)


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "TODO: write tests" in items
    assert "Ship it!" in items


def test_extract_tags():
    text = "This is a note with #urgent and #todo tags #repeat"
    tags = extract_tags(text)
    assert "urgent" in tags
    assert "todo" in tags
    assert "repeat" in tags
    assert len(tags) == 3  # Should preserve order, remove duplicates


def test_extract_tags_no_duplicates():
    text = "This has #tag and #tag and #tag"
    tags = extract_tags(text)
    assert tags == ["tag"]
    assert len(tags) == 1


def test_extract_tags_empty():
    text = "This has no tags"
    tags = extract_tags(text)
    assert tags == []


def test_extract_tags_special_characters():
    text = "Tags with #underscore_123 and #dash-dash"
    tags = extract_tags(text)
    # Support for underscores and hyphens in tags
    assert "underscore_123" in tags
    assert "dash-dash" in tags


def test_extract_action_items_with_tags():
    text = """
    - TODO: write tests #testing #quality
    - Ship it! #urgent #release
    - Review PR #code-review
    Not actionable
    """.strip()

    items = extract_action_items_with_tags(text)
    assert len(items) == 3

    # Check first item
    assert items[0]["description"] == "write tests"
    assert "testing" in items[0]["tags"]
    assert "quality" in items[0]["tags"]

    # Check second item
    assert items[1]["description"] == "Ship it"
    assert "urgent" in items[1]["tags"]
    assert "release" in items[1]["tags"]

    # Check third item
    assert items[2]["description"] == "Review PR"
    assert "code-review" in items[2]["tags"]


def test_extract_action_items_with_tags_no_tags():
    text = """
    - TODO: write tests
    - Ship it!
    """.strip()

    items = extract_action_items_with_tags(text)
    assert len(items) == 2
    assert items[0]["tags"] == []
    assert items[1]["tags"] == []


def test_extract_action_items_with_tags_mixed():
    text = """
    Some text with #random tag
    - TODO: do this #urgent
    Normal line
    - Fix that bug! #bug
    Another #orphan tag
    """.strip()

    items = extract_action_items_with_tags(text)
    assert len(items) == 2
    assert items[0]["description"] == "do this"
    assert items[0]["tags"] == ["urgent"]
    assert items[1]["description"] == "Fix that bug"
    assert items[1]["tags"] == ["bug"]
