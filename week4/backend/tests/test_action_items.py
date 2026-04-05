def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1


def test_create_action_item_validation_empty_description(client):
    payload = {"description": ""}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422, r.text
    error = r.json()
    assert "description" in str(error["detail"]).lower()


def test_create_action_item_validation_whitespace_description(client):
    payload = {"description": "   "}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422, r.text
    error = r.json()
    assert "description" in str(error["detail"]).lower()


def test_create_action_item_validation_missing_description(client):
    payload = {}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422, r.text
    error = r.json()
    assert "description" in str(error["detail"]).lower()


def test_create_action_item_validation_description_too_long(client):
    payload = {"description": "x" * 501}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422, r.text


def test_complete_action_item_not_found(client):
    r = client.put("/action-items/999999/complete")
    assert r.status_code == 404, r.text
    error = r.json()
    assert "not found" in error["detail"].lower()
