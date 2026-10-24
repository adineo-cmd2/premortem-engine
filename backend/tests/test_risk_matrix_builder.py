from app.services.risk_matrix_builder import AXES_X, AXES_Y, build


def test_build_points_in_range_and_axes_labels():
    scenarios = [
        {"title": "A", "category": "technical", "probability": "high", "severity": "critical"},
        {"title": "B", "category": "team", "probability": "low", "severity": "medium"},
        {"title": "C", "category": "market", "probability": "medium", "severity": "high"},
    ]
    matrix = build(scenarios)
    assert matrix["axes"]["x"] == ["medium", "high", "critical"]
    assert matrix["axes"]["y"] == ["low", "medium", "high"]
    assert AXES_X == ["medium", "high", "critical"]
    assert AXES_Y == ["low", "medium", "high"]
    assert len(matrix["points"]) == 3
    for p in matrix["points"]:
        assert p["x"] in (1, 2, 3)
        assert p["y"] in (1, 2, 3)
    by_title = {p["title"]: p for p in matrix["points"]}
    assert (by_title["A"]["x"], by_title["A"]["y"]) == (3, 3)
    assert (by_title["B"]["x"], by_title["B"]["y"]) == (1, 1)
    assert (by_title["C"]["x"], by_title["C"]["y"]) == (2, 2)
