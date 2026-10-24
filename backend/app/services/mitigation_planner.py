"""Mitigation action pool per category. Templates use {name} (project name)
and {title} (scenario title). plan(scenario) returns 3-5 filled mitigations."""

ACTIONS = {
    "technical": [
        {"action_t": "Add staged deploy with feature flags and rollback runbook for {title} in {name}.", "owner_role": "Tech Lead", "effort": "medium", "timeline_weeks": 2},
        {"action_t": "Write contract tests pinning interfaces behind {title} in {name}.", "owner_role": "QA", "effort": "medium", "timeline_weeks": 3},
        {"action_t": "Load-test {name} at 10x forecast before launch to blunt {title}.", "owner_role": "Tech Lead", "effort": "high", "timeline_weeks": 4},
        {"action_t": "Add monitoring alerts and automated kill switch covering {title} in {name}.", "owner_role": "Ops", "effort": "low", "timeline_weeks": 1},
    ],
    "team": [
        {"action_t": "Create anonymous dissent channel and independent no-go vote for {name} to surface {title} early.", "owner_role": "PM", "effort": "low", "timeline_weeks": 1},
        {"action_t": "Document critical paths and pair owners so {title} survives anyone leaving {name}.", "owner_role": "Tech Lead", "effort": "medium", "timeline_weeks": 2},
        {"action_t": "Cap on-call load and rotate heroes on {name} to prevent {title}.", "owner_role": "PM", "effort": "low", "timeline_weeks": 2},
        {"action_t": "Hold monthly demo-or-it-didn't-happen reviews of {title} for {name}.", "owner_role": "Founder", "effort": "low", "timeline_weeks": 4},
    ],
    "market": [
        {"action_t": "Run 15 problem interviews before building further on {name} to test {title}.", "owner_role": "Founder", "effort": "medium", "timeline_weeks": 2},
        {"action_t": "Ship a small paid pilot of {name} to validate {title} with real money.", "owner_role": "PM", "effort": "medium", "timeline_weeks": 4},
        {"action_t": "Test pricing and positioning against the bundled alternative behind {title}.", "owner_role": "Designer", "effort": "low", "timeline_weeks": 2},
        {"action_t": "Define kill/pivot metrics for {name} so {title} triggers a decision, not drift.", "owner_role": "Founder", "effort": "low", "timeline_weeks": 1},
    ],
    "execution": [
        {"action_t": "Freeze scope for {name} with a written change-control log to stop {title}.", "owner_role": "PM", "effort": "low", "timeline_weeks": 1},
        {"action_t": "Rehearse a manual fallback for the automated flow behind {title} in {name}.", "owner_role": "Ops", "effort": "medium", "timeline_weeks": 2},
        {"action_t": "Commission an independent audit of {name} schedule and defects tied to {title}.", "owner_role": "PM", "effort": "medium", "timeline_weeks": 3},
        {"action_t": "Ring-fence 20% contingency budget and time for {name} against {title}.", "owner_role": "Founder", "effort": "low", "timeline_weeks": 1},
    ],
    "dependency": [
        {"action_t": "Qualify a second supplier for the dependency behind {title} in {name}.", "owner_role": "Ops", "effort": "high", "timeline_weeks": 6},
        {"action_t": "Load-test the backup path for {name} so {title} has a tested failover.", "owner_role": "Tech Lead", "effort": "medium", "timeline_weeks": 2},
        {"action_t": "Renegotiate SLA and exit clause with the vendor behind {title}.", "owner_role": "Founder", "effort": "low", "timeline_weeks": 2},
        {"action_t": "Map single points of failure across {name}, starting with {title}.", "owner_role": "Ops", "effort": "low", "timeline_weeks": 1},
        {"action_t": "Stock buffer inventory/credits to survive a 30-day outage of {title}.", "owner_role": "Ops", "effort": "medium", "timeline_weeks": 3},
    ],
    "unknown": [
        {"action_t": "Write worst-case capacity and abort criteria for {name} covering {title}.", "owner_role": "PM", "effort": "low", "timeline_weeks": 1},
        {"action_t": "Over-provision safety margin (water/staff/cash) for {name} against {title}.", "owner_role": "Ops", "effort": "medium", "timeline_weeks": 2},
        {"action_t": "Draft a one-page crisis playbook for {name} naming owners for {title}.", "owner_role": "Founder", "effort": "low", "timeline_weeks": 1},
        {"action_t": "Buy tabletop exercise time: simulate {title} with the {name} team quarterly.", "owner_role": "PM", "effort": "low", "timeline_weeks": 4},
    ],
}


def _get(item, key, default=""):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def plan(scenario, count=4):
    """Return 3-5 filled mitigations for a scenario dict (or ORM object).

    Fills {name} from project/session name fields and {title} from title.
    """
    category = _get(scenario, "category", "general")
    pool = ACTIONS.get(category, ACTIONS["unknown"])
    title = _get(scenario, "title", "this scenario")
    name = (
        _get(scenario, "project_name", "")
        or _get(scenario, "name", "")
        or _get(scenario, "session_name", "")
        or "the project"
    )
    n = max(3, min(5, count, len(pool)))
    out = []
    for entry in pool[:n]:
        out.append({
            "action": entry["action_t"].format(name=name, title=title),
            "owner_role": entry["owner_role"],
            "effort": entry["effort"],
            "timeline_weeks": entry["timeline_weeks"],
        })
    return out
