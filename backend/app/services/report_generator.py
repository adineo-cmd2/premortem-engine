"""Markdown report renderer for a pre-mortem session."""

DISCLAIMER = (
    "> Disclaimer: this report is a speculative planning aid, not a prediction. "
    "Scenarios are imagined failure modes to help you prepare; precedents are "
    "real historical cases cited for learning."
)


def _get(item, key, default=""):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def _precedent_lines(precedent):
    if isinstance(precedent, dict):
        name = precedent.get("project_name", "")
        year = precedent.get("year", "")
        what = precedent.get("what_happened", "")
        prev = precedent.get("prevention", "")
        head = f"{name} ({year})" if year else name
        lines = []
        if head:
            lines.append(f"- Precedent: **{head}**")
        if what:
            lines.append(f"  - What happened: {what}")
        if prev:
            lines.append(f"  - Lesson: {prev}")
        return lines
    if precedent:
        return [f"- Precedent: {precedent}"]
    return []


def render(session, scenarios):
    """Render markdown for session + enriched scenarios.

    Each scenario dict may carry precedent (dict or str), warnings (list),
    mitigations (list of {action, owner_role, effort, timeline_weeks}).
    """
    name = _get(session, "name", _get(session, "project_name", "Untitled project"))
    description = _get(session, "description", "")
    ptype = _get(session, "project_type", "general")

    out = [f"# Pre-mortem: {name}", "", DISCLAIMER, ""]
    if description:
        out += [f"Project: {description}", ""]
    out += [f"Project type: {ptype}", f"Scenarios: {len(scenarios)}", ""]

    # Matrix summary counts by severity and probability.
    sev_counts: dict = {}
    prob_counts: dict = {}
    for s in scenarios:
        sev_counts[_get(s, "severity", "")] = sev_counts.get(_get(s, "severity", ""), 0) + 1
        prob_counts[_get(s, "probability", "")] = prob_counts.get(_get(s, "probability", ""), 0) + 1
    out += ["## Risk matrix summary", ""]
    for sev in ("critical", "high", "medium"):
        if sev in sev_counts:
            out.append(f"- Severity {sev}: {sev_counts[sev]}")
    for prob in ("high", "medium", "low"):
        if prob in prob_counts:
            out.append(f"- Probability {prob}: {prob_counts[prob]}")
    out.append("")

    for i, s in enumerate(scenarios, 1):
        title = _get(s, "title", f"Scenario {i}")
        out += [f"## {i}. {title}", ""]
        out.append(
            f"Category: {_get(s, 'category', '')} | "
            f"Probability: {_get(s, 'probability', '')} | "
            f"Severity: {_get(s, 'severity', '')}"
        )
        out.append("")
        narrative = _get(s, "narrative", "")
        if narrative:
            out += [narrative, ""]
        out += _precedent_lines(_get(s, "precedent", ""))
        if _get(s, "precedent", ""):
            out.append("")
        warnings = _get(s, "warnings", []) or []
        if warnings:
            out += ["Early warnings:", ""]
            out += [f"- {w}" for w in warnings]
            out.append("")
        mitigations = _get(s, "mitigations", []) or []
        if mitigations:
            out += ["Mitigations:", "", "| Action | Owner | Effort | Weeks |",
                    "| --- | --- | --- | --- |"]
            for m in mitigations:
                if isinstance(m, dict):
                    out.append(
                        f"| {m.get('action', '')} | {m.get('owner_role', '')} | "
                        f"{m.get('effort', '')} | {m.get('timeline_weeks', '')} |"
                    )
            out.append("")
    return "\n".join(out).rstrip() + "\n"
