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


def test_create_note_validation_empty_title(client):
    payload = {"title": "", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422, r.text
    error = r.json()
    assert "title" in str(error["detail"]).lower()


def test_create_note_validation_whitespace_title(client):
    payload = {"title": "   ", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422, r.text
    error = r.json()
    assert "title" in str(error["detail"]).lower()


def test_create_note_validation_empty_content(client):
    payload = {"title": "Test", "content": ""}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422, r.text
    error = r.json()
    assert "content" in str(error["detail"]).lower()


def test_create_note_validation_missing_title(client):
    payload = {"content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422, r.text
    error = r.json()
    assert "title" in str(error["detail"]).lower()


def test_create_note_validation_missing_content(client):
    payload = {"title": "Test"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422, r.text
    error = r.json()
    assert "content" in str(error["detail"]).lower()


def test_create_note_validation_title_too_long(client):
    payload = {"title": "x" * 201, "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422, r.text


def test_create_note_validation_content_too_long(client):
    payload = {"title": "Test", "content": "x" * 5001}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422, r.text


def test_get_note_not_found(client):
    r = client.get("/notes/999999")
    assert r.status_code == 404, r.text
    error = r.json()
    assert "not found" in error["detail"].lower()


def test_update_note(client):
    # Create a note first
    create_payload = {"title": "Original", "content": "Content"}
    r = client.post("/notes/", json=create_payload)
    note_id = r.json()["id"]

    # Update the note
    update_payload = {"title": "Updated", "content": "New content"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["title"] == "Updated"
    assert data["content"] == "New content"
    assert data["id"] == note_id


def test_update_note_partial(client):
    # Create a note first
    create_payload = {"title": "Original", "content": "Content"}
    r = client.post("/notes/", json=create_payload)
    note_id = r.json()["id"]

    # Update only title
    update_payload = {"title": "New Title"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["title"] == "New Title"
    assert data["content"] == "Content"

    # Update only content
    update_payload = {"content": "New content"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["title"] == "New Title"
    assert data["content"] == "New content"


def test_update_note_not_found(client):
    update_payload = {"title": "Updated", "content": "New content"}
    r = client.put("/notes/999999", json=update_payload)
    assert r.status_code == 404, r.text
    error = r.json()
    assert "not found" in error["detail"].lower()


def test_update_note_validation_empty_title(client):
    # Create a note first
    create_payload = {"title": "Original", "content": "Content"}
    r = client.post("/notes/", json=create_payload)
    note_id = r.json()["id"]

    # Try to update with empty title
    update_payload = {"title": ""}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 422, r.text


def test_update_note_validation_whitespace_title(client):
    # Create a note first
    create_payload = {"title": "Original", "content": "Content"}
    r = client.post("/notes/", json=create_payload)
    note_id = r.json()["id"]

    # Try to update with whitespace title
    update_payload = {"title": "   "}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 422, r.text


def test_delete_note(client):
    # Create a note first
    create_payload = {"title": "To Delete", "content": "Content"}
    r = client.post("/notes/", json=create_payload)
    note_id = r.json()["id"]

    # Delete the note
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204, r.text

    # Verify it's deleted
    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404, r.text


def test_delete_note_not_found(client):
    r = client.delete("/notes/999999")
    assert r.status_code == 404, r.text
    error = r.json()
    assert "not found" in error["detail"].lower()
