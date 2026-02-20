from app import app

def test_healthz():
    c = app.test_client()
    resp = c.get("/healthz")
    assert resp.status_code == 200
    assert resp.is_json
    assert resp.json["status"] == "ok"

def test_index_loads():
    c = app.test_client()
    resp = c.get("/")
    assert resp.status_code == 200
    assert b"Generate" in resp.data

def test_generate_post():
    c = app.test_client()
    resp = c.post("/generate", data={"seed_hint": "demo"})
    assert resp.status_code == 200
    assert b"rand_a" in resp.data
    assert b"calc_b" in resp.data