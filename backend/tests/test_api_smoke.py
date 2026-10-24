import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi.testclient import TestClient

from app.db.session import Base, engine
from app.main import app


def test_api_smoke():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    c = TestClient(app)
    assert c.get("/healthz").json() == {"ok": True}

    # validation: empty project_name + description -> 400
    r = c.post(
        "/api/premortem/submit",
        json={"project_name": "   ", "description": "", "project_type": "software"},
    )
    assert r.status_code == 400, r.text

    r = c.post(
        "/api/premortem/submit",
        json={
            "project_name": "Rocket Notes",
            "description": "Collaborative notes app for launch teams",
            "project_type": "software",
            "launch_date": "2026-12-01",
            "team_size": 6,
            "key_dependencies": ["postgres", "stripe"],
            "known_risks": "tight deadline",
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()
    sid = body["session_id"]
    assert sid
    assert len(body["scenarios"]) == 10

    r = c.get(f"/api/premortem/{sid}/scenarios")
    assert r.status_code == 200, r.text
    scenarios = r.json()
    scenarios = scenarios["scenarios"] if isinstance(scenarios, dict) and "scenarios" in scenarios else scenarios
    assert isinstance(scenarios, list) and len(scenarios) == 10
    cats = {s["category"] for s in scenarios}
    assert len(cats) == 6, cats

    r = c.get(f"/api/premortem/{sid}/risk-matrix")
    assert r.status_code == 200, r.text
    matrix = r.json()
    points = matrix["points"]
    assert len(points) == 10
    for p in points:
        assert p["x"] in (1, 2, 3), p
        assert p["y"] in (1, 2, 3), p

    two_ids = [scenarios[0]["id"], scenarios[1]["id"]]
    r = c.post(f"/api/premortem/{sid}/mitigate", json={"scenario_ids": two_ids})
    assert r.status_code == 200, r.text
    payload = r.json()
    mits = payload["mitigations"] if isinstance(payload, dict) and "mitigations" in payload else payload
    assert isinstance(mits, list) and len(mits) >= 2, payload

    r = c.get(f"/api/premortem/{sid}/mitigations")
    assert r.status_code == 200, r.text
    payload = r.json()
    if isinstance(payload, dict) and "mitigations" in payload:
        all_mits = payload["mitigations"]
        assert isinstance(all_mits, list) and len(all_mits) >= 2
    elif isinstance(payload, list):
        # grouped by scenario: [{scenario_id, mitigations:[...]}]
        total = 0
        for g in payload:
            assert "mitigations" in g, g
            total += len(g["mitigations"])
        assert total >= 2
    else:
        raise AssertionError(f"unexpected mitigations shape: {payload!r}")

    r = c.get(f"/api/premortem/{sid}/report")
    assert r.status_code == 200, r.text
    md = r.json()["markdown"] if isinstance(r.json(), dict) else str(r.json())
    assert "speculative planning aid" in md.lower(), md[:500]

    r = c.get("/api/premortem/history")
    assert r.status_code == 200, r.text
    hist = r.json()
    hist = hist["history"] if isinstance(hist, dict) and "history" in hist else hist
    assert isinstance(hist, list) and len(hist) >= 1
    assert any(item.get("id") == sid for item in hist)

    r = c.delete(f"/api/premortem/{sid}")
    assert r.status_code == 200, r.text
    r = c.get(f"/api/premortem/{sid}/scenarios")
    assert r.status_code == 404, r.text
