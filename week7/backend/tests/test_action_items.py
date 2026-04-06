def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_delete_action_item(client):
    create_payload = {"description": "To Delete"}
    r = client.post("/action-items/", json=create_payload)
    assert r.status_code == 201
    item_id = r.json()["id"]

    r = client.delete(f"/action-items/{item_id}")
    assert r.status_code == 204

    r = client.get(f"/action-items/{item_id}")
    assert r.status_code == 404


def test_delete_nonexistent_action_item(client):
    r = client.delete("/action-items/99999")
    assert r.status_code == 404


def test_validation_description_too_long(client):
    payload = {"description": "x" * 1001}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422


def test_validation_description_empty(client):
    payload = {"description": ""}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422


def test_validation_patch_description_empty(client):
    create_payload = {"description": "Test"}
    r = client.post("/action-items/", json=create_payload)
    item_id = r.json()["id"]

    r = client.patch(f"/action-items/{item_id}", json={"description": ""})
    assert r.status_code == 422


def test_action_items_pagination_skip_negative(client):
    r = client.get("/action-items/", params={"skip": -1})
    assert r.status_code == 422


def test_action_items_pagination_skip_zero(client):
    r = client.get("/action-items/", params={"skip": 0})
    assert r.status_code == 200


def test_action_items_pagination_limit_at_boundary(client):
    r = client.get("/action-items/", params={"limit": 200})
    assert r.status_code == 200

    r = client.get("/action-items/", params={"limit": 201})
    assert r.status_code == 422
