from app.services.precedent_matcher import REAL_PRECEDENTS
from app.services.scenario_generator import generate

PROBS = {"high", "medium", "low"}
SEVS = {"critical", "high", "medium"}
CATS = {"technical", "team", "market", "execution", "dependency", "unknown"}


def test_generate_ten_scenarios_all_categories_valid_values():
    scenarios = generate(
        name="Atlas",
        description="Ship a new SaaS billing platform for launch",
        ptype="software",
        team_size=8,
        deps=["stripe", "postgres"],
    )
    assert len(scenarios) == 10
    cats = {s["category"] for s in scenarios}
    assert cats == CATS
    for s in scenarios:
        assert s["category"] in CATS
        assert s["probability"] in PROBS
        assert s["severity"] in SEVS
        assert s["title"] and s["narrative"]
        assert isinstance(s["warnings"], list) and len(s["warnings"]) == 3
        assert s["precedent_key"] in REAL_PRECEDENTS
        rec = REAL_PRECEDENTS[s["precedent_key"]]
        assert isinstance(rec["year"], int) and rec["year"] > 1900
        assert rec["project_name"]


def test_generate_unknown_ptype_falls_back_to_general():
    scenarios = generate(
        name="X", description="mystery project", ptype="nope",
        team_size=3, deps=[],
    )
    assert len(scenarios) == 10
    assert {s["category"] for s in scenarios} == CATS
