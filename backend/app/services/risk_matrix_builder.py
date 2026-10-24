"""Probability x severity risk matrix builder.

Severity is the x-axis: medium=1, high=2, critical=3.
Probability is the y-axis: low=1, medium=2, high=3.
"""

SEV_X = {"medium": 1, "high": 2, "critical": 3}
PROB_Y = {"low": 1, "medium": 2, "high": 3}

AXES_X = ["medium", "high", "critical"]
AXES_Y = ["low", "medium", "high"]


def _get(item, key, default=""):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def build(scenarios):
    """Build matrix JSON from scenario dicts (or ORM objects).

    Returns {points: [{x, y, scenario, title, category, severity,
    probability}], axes: {x: [...], y: [...]}}.
    """
    points = []
    for i, s in enumerate(scenarios):
        severity = _get(s, "severity", "medium")
        probability = _get(s, "probability", "low")
        x = SEV_X.get(severity, 1)
        y = PROB_Y.get(probability, 1)
        sid = _get(s, "id", _get(s, "scenario_id", i))
        points.append({
            "scenario": sid,
            "scenario_id": sid,
            "title": _get(s, "title", ""),
            "category": _get(s, "category", ""),
            "severity": severity,
            "probability": probability,
            "x": x,
            "y": y,
        })
    return {
        "points": points,
        "axes": {"x": list(AXES_X), "y": list(AXES_Y)},
    }
