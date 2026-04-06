def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_put_note(client):
    create_payload = {"title": "Original", "content": "Original content"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    update_payload = {"title": "Updated", "content": "Updated content"}
    r = client.put(f"/notes/{note_id}", json=update_payload)
    assert r.status_code == 200
    updated = r.json()
    assert updated["title"] == "Updated"
    assert updated["content"] == "Updated content"


def test_delete_note(client):
    create_payload = {"title": "To Delete", "content": "Will be deleted"}
    r = client.post("/notes/", json=create_payload)
    assert r.status_code == 201
    note_id = r.json()["id"]

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_nonexistent_note(client):
    r = client.delete("/notes/99999")
    assert r.status_code == 404


def test_validation_title_too_long(client):
    payload = {"title": "x" * 201, "content": "content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_validation_title_empty(client):
    payload = {"title": "", "content": "content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_validation_content_empty(client):
    payload = {"title": "Test", "content": ""}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_validation_patch_empty_fields(client):
    create_payload = {"title": "Test", "content": "content"}
    r = client.post("/notes/", json=create_payload)
    note_id = r.json()["id"]

    r = client.patch(f"/notes/{note_id}", json={"title": ""})
    assert r.status_code == 422


def test_pagination_skip_negative(client):
    r = client.get("/notes/", params={"skip": -1})
    assert r.status_code == 422


def test_pagination_skip_zero(client):
    r = client.get("/notes/", params={"skip": 0})
    assert r.status_code == 200


def test_pagination_limit_at_boundary(client):
    r = client.get("/notes/", params={"limit": 200})
    assert r.status_code == 200

    r = client.get("/notes/", params={"limit": 201})
    assert r.status_code == 422
