def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_search_case_insensitive_title(client):
    # Create a note with specific case in title
    payload = {"title": "Hello World", "content": "Test content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text

    # Search with uppercase query
    r = client.get("/notes/search/", params={"q": "HELLO"})
    assert r.status_code == 200, r.text
    items = r.json()
    assert len(items) >= 1, f"Expected at least 1 note, got {len(items)}"
    assert any(
        "Hello World" in item["title"] for item in items
    ), "Expected to find 'Hello World' in results"


def test_search_case_insensitive_content(client):
    # Create a note with specific case in content
    payload = {"title": "Test Note", "content": "This is a world of code"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text

    # Search with uppercase query
    r = client.get("/notes/search/", params={"q": "WORLD"})
    assert r.status_code == 200, r.text
    items = r.json()
    assert len(items) >= 1, f"Expected at least 1 note, got {len(items)}"
    assert any("world" in item["content"] for item in items), "Expected to find 'world' in content"


def test_search_case_insensitive_mixed(client):
    # Create a note with mixed case
    payload = {"title": "Hello World", "content": "Python programming"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text

    # Search with mixed case query
    r = client.get("/notes/search/", params={"q": "HeLLo"})
    assert r.status_code == 200, r.text
    items = r.json()
    assert len(items) >= 1, f"Expected at least 1 note, got {len(items)}"
    assert any(
        "Hello" in item["title"] for item in items
    ), "Expected to find 'Hello' in title with mixed case query"


def test_update_note(client):
    # Create a note first
    create_payload = {"title": "Original", "content": "Original content"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    # Update the note
    update_payload = {"title": "Updated", "content": "New content"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["title"] == "Updated"
    assert data["content"] == "New content"

    # Verify the update persisted
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["title"] == "Updated"
    assert data["content"] == "New content"


def test_update_note_not_found(client):
    # Try to update a note that doesn't exist
    update_payload = {"title": "Updated", "content": "New content"}
    r = client.put("/notes/999", json=update_payload)
    assert r.status_code == 404, r.text


def test_delete_note(client):
    # Create a note first
    create_payload = {"title": "To Delete", "content": "Content"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201, r.text
    note_id = r.json()["id"]

    # Delete the note
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204, r.text  # DELETE should return 204 No Content

    # Verify it's deleted
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404, r.text


def test_delete_note_not_found(client):
    # Try to delete a note that doesn't exist
    r = client.delete("/notes/999")
    assert r.status_code == 404, r.text
