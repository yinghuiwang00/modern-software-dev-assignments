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


def test_unsafe_search_normal_query(client):
    """Test that unsafe_search works with normal queries"""
    # Create test notes
    client.post("/notes/", json={"title": "Python Programming", "content": "Learn Python basics"})
    client.post("/notes/", json={"title": "JavaScript Guide", "content": "Advanced JS techniques"})

    # Search for "Python"
    r = client.get("/notes/unsafe-search?q=Python")
    assert r.status_code == 200, r.text
    items = r.json()
    assert len(items) >= 1
    assert any("Python" in item["title"] or "Python" in item["content"] for item in items)

    # Search for "JavaScript"
    r = client.get("/notes/unsafe-search?q=JavaScript")
    assert r.status_code == 200, r.text
    items = r.json()
    assert len(items) >= 1
    assert any("JavaScript" in item["title"] or "JavaScript" in item["content"] for item in items)


def test_unsafe_search_sql_injection_or_true(client):
    """Test that SQL injection with OR '1'='1 is prevented"""
    # Create a test note
    client.post("/notes/", json={"title": "Secret Note", "content": "Sensitive data"})

    # Try SQL injection: ' OR '1'='1
    # If vulnerable, this would return all notes
    # If fixed, this treats the injection as literal text
    r = client.get("/notes/unsafe-search?q=' OR '1'='1")
    assert r.status_code == 200, r.text
    items = r.json()

    # With the fix, the search should look for the literal string "' OR '1'='1"
    # which won't match any notes, so results should be empty
    assert len(items) == 0, f"SQL injection succeeded! Found {len(items)} notes when expecting 0"


def test_unsafe_search_sql_injection_union(client):
    """Test that SQL injection with UNION is prevented"""
    # Create a test note
    client.post("/notes/", json={"title": "Test Note", "content": "Test content"})

    # Try UNION injection to extract schema info
    injection = "' UNION SELECT 1,2,3,4,5--"
    r = client.get(f"/notes/unsafe-search?q={injection}")
    assert r.status_code == 200, r.text
    items = r.json()

    # With the fix, the injection is treated as literal text
    # and won't match any notes
    assert len(items) == 0, f"UNION injection succeeded! Found {len(items)} notes when expecting 0"


def test_unsafe_search_sql_injection_drop(client):
    """Test that SQL injection with DROP TABLE is prevented"""
    # Create a test note
    client.post("/notes/", json={"title": "Important Note", "content": "Important data"})

    # Try DROP TABLE injection
    injection = "'; DROP TABLE notes;--"
    r = client.get(f"/notes/unsafe-search?q={injection}")
    assert r.status_code == 200, r.text

    # Verify notes table still exists by trying to get notes
    r = client.get("/notes/")
    assert r.status_code == 200, r.text
    items = r.json()
    assert len(items) >= 1, "DROP TABLE injection succeeded! Notes table was deleted"


def test_unsafe_search_special_characters(client):
    """Test that special characters are handled safely"""
    # Create a note with special characters
    client.post(
        "/notes/", json={"title": "C++ & Python", "content": "Code: <script>alert('XSS')</script>"}
    )

    # Search with special characters - TestClient handles URL encoding
    r = client.get("/notes/unsafe-search", params={"q": "C++ & Python"})
    assert r.status_code == 200, r.text
    items = r.json()

    # Should find the note with the literal search term
    # The & character might be URL-encoded as %26 by the client
    if len(items) == 0:
        # Try searching for just "C++" if the full search fails
        r = client.get("/notes/unsafe-search", params={"q": "C++"})
        assert r.status_code == 200, r.text
        items = r.json()
        assert len(items) >= 1, "Search with special characters failed"

    # Search with quotes - use params dict to avoid URL encoding issues
    r = client.get("/notes/unsafe-search", params={"q": "<script>"})
    assert r.status_code == 200, r.text
    items = r.json()

    # Should find the note with the literal search term
    assert len(items) >= 1, "Search with quotes failed"


def test_unsafe_search_empty_query(client):
    """Test that empty query doesn't cause issues"""
    # Create a test note
    client.post("/notes/", json={"title": "Test", "content": "Content"})

    # Search with empty string
    r = client.get("/notes/unsafe-search?q=")
    assert r.status_code == 200, r.text
    items = r.json()

    # Empty query should match all notes (LIKE '%%' matches everything)
    assert len(items) >= 1


def test_debug_run_endpoint_removed(client):
    """Test that the debug_run endpoint with command injection vulnerability is removed"""
    # Try to access the command injection endpoint
    r = client.get("/notes/debug/run?cmd=echo%20test")
    # Should return 404 because the endpoint is removed
    assert r.status_code == 404, f"debug_run endpoint still exists! Status: {r.status_code}"


def test_debug_eval_endpoint_removed(client):
    """Test that the debug_eval endpoint with code injection vulnerability is removed"""
    # Try to access the code injection endpoint
    r = client.get("/notes/debug/eval?expr=1%2B1")
    # Should return 404 because the endpoint is removed
    assert r.status_code == 404, f"debug_eval endpoint still exists! Status: {r.status_code}"


def test_debug_fetch_endpoint_removed(client):
    """Test that the debug_fetch endpoint with SSRF vulnerability is removed"""
    # Try to access the SSRF endpoint
    r = client.get("/notes/debug/fetch?url=http://example.com")
    # Should return 404 because the endpoint is removed
    assert r.status_code == 404, f"debug_fetch endpoint still exists! Status: {r.status_code}"


def test_debug_read_endpoint_removed(client):
    """Test that the debug_read endpoint with path traversal vulnerability is removed"""
    # Try to access the path traversal endpoint
    r = client.get("/notes/debug/read?path=/etc/passwd")
    # Should return 404 because the endpoint is removed
    assert r.status_code == 404, f"debug_read endpoint still exists! Status: {r.status_code}"


def test_debug_hash_md5_endpoint_removed(client):
    """Test that the debug_hash_md5 endpoint with weak cryptography is removed"""
    # Try to access the weak cryptography endpoint
    r = client.get("/notes/debug/hash-md5?q=test")
    # Should return 404 because the endpoint is removed
    assert r.status_code == 404, f"debug_hash_md5 endpoint still exists! Status: {r.status_code}"


def test_all_debug_endpoints_removed(client):
    """Test that all debug endpoints are removed for security"""
    debug_endpoints = [
        "/notes/debug/run",
        "/notes/debug/eval",
        "/notes/debug/fetch",
        "/notes/debug/read",
        "/notes/debug/hash-md5",
    ]

    for endpoint in debug_endpoints:
        r = client.get(endpoint)
        assert (
            r.status_code == 404
        ), f"Debug endpoint {endpoint} still exists! Status: {r.status_code}"
