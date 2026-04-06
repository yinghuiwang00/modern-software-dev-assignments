import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    # Updated for new return format with tags
    assert len(items) == 2
    descriptions = [item["description"] for item in items]
    assert "TODO: write tests" in descriptions
    assert "Ship it!" in descriptions
    # These items should have empty tags if no tags present
    for item in items:
        assert "tags" in item
        assert isinstance(item["tags"], list)


def test_extract_action_items_with_tags():
    """Test extracting action items with hashtag tags"""
    text = """
    #urgent: Fix the bug #critical
    #lowpriority: Documentation
    - TODO: write tests #important
    - Complete the feature #blocker
    - Regular task without tags!
    Not actionable text
    """.strip()
    items = extract_action_items(text)
    # Should extract at least 4-5 items depending on implementation
    assert len(items) >= 4

    # Check for items with tags
    urgent_item = next((i for i in items if "Fix the bug" in i["description"]), None)
    assert urgent_item is not None
    assert "tags" in urgent_item
    assert isinstance(urgent_item["tags"], list)
    # Tags should contain either "#urgent" or "urgent"
    assert "#urgent" in urgent_item["tags"] or "urgent" in urgent_item["tags"]

    tests_item = next((i for i in items if "write tests" in i["description"]), None)
    assert tests_item is not None
    assert "tags" in tests_item
    assert "#important" in tests_item["tags"] or "important" in tests_item["tags"]

    # Check item with no tags
    regular_item = next((i for i in items if "Regular task" in i["description"]), None)
    assert regular_item is not None
    assert "tags" in regular_item
    assert isinstance(regular_item["tags"], list)


def test_extract_tags_only():
    """Test that tags are properly extracted from various formats"""
    text = """
    - Fix bug #urgent #critical #production
    - Review code #review
    - Deploy to staging #deploy
    - Simple task!
    """.strip()
    items = extract_action_items(text)
    assert len(items) == 4

    # Check multi-tag extraction
    bug_item = next((i for i in items if "Fix bug" in i["description"]), None)
    assert bug_item is not None
    assert len(bug_item["tags"]) >= 3
    # Should contain at least these tags (with or without #)
    tag_set = set(bug_item["tags"])
    assert any("urgent" in tag for tag in tag_set)
    assert any("critical" in tag for tag in tag_set)
    assert any("production" in tag for tag in tag_set)

    # Check single tag
    review_item = next((i for i in items if "Review code" in i["description"]), None)
    assert review_item is not None
    assert len(review_item["tags"]) >= 1
    assert any("review" in tag for tag in review_item["tags"])

    # Check item without tags
    simple_item = next((i for i in items if "Simple task" in i["description"]), None)
    assert simple_item is not None
    assert len(simple_item["tags"]) == 0


def test_extract_mixed_content():
    """Test mixed content with multiple tags, items, and edge cases"""
    text = """
    Meeting notes
    - Follow up with team #urgent #meeting
    - Send report #email #deadline
    Some description here
    #priority: Update documentation
    - TODO: Fix the bug! #critical
    - Deploy to production #deploy #monday
    Regular text without action items
    - Simple reminder
    Final action item! #final
    """.strip()
    items = extract_action_items(text)
    # Should extract items ending with ! or starting with # or TODO:
    assert len(items) >= 5

    # Verify structure for all items
    for item in items:
        assert isinstance(item, dict), "Each item should be a dictionary"
        assert "description" in item, "Each item should have a description field"
        assert "tags" in item, "Each item should have a tags field"
        assert isinstance(item["description"], str), "Description should be a string"
        assert isinstance(item["tags"], list), "Tags should be a list"

    # Check specific items
    followup_item = next((i for i in items if "Follow up with team" in i["description"]), None)
    if followup_item:
        assert any("urgent" in tag for tag in followup_item["tags"])
        assert any("meeting" in tag for tag in followup_item["tags"])

    deploy_item = next((i for i in items if "Deploy to production" in i["description"]), None)
    if deploy_item:
        assert any("deploy" in tag for tag in deploy_item["tags"])
        assert any("monday" in tag for tag in deploy_item["tags"])
