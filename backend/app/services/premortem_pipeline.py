"""End-to-end pre-mortem pipeline: persist session + scenarios + precedents."""

from app.models.failure_scenario import FailureScenario
from app.models.mitigation_action import MitigationAction  # noqa: F401 (used by mitigate endpoint later)
from app.models.precedent_record import PrecedentRecord
from app.models.premortem_session import PreMortemSession
from app.services.precedent_matcher import match
from app.services.scenario_generator import generate


def run_premortem(db, user_id, name, description, ptype, launch_date,
                  team_size, deps, risks):
    """Run generation and persist everything.

    Returns {"session_id": int, "scenarios": [10 dicts with ids]}.
    """
    deps = list(deps or [])
    session = PreMortemSession(
        user_id=user_id,
        name=name or "Untitled project",
        description=description or "",
        project_type=(ptype or "general").lower() or "general",
        launch_date=launch_date or "",
        team_size=int(team_size or 0),
        dependencies=deps,
        risks=risks or "",
    )
    db.add(session)
    db.flush()

    generated = generate(
        name=session.name,
        description=session.description,
        ptype=session.project_type,
        team_size=session.team_size,
        deps=deps,
    )

    out = []
    for g in generated:
        rec = match(g["precedent_key"])
        row = FailureScenario(
            session_id=session.id,
            category=g["category"],
            title=g["title"],
            narrative=g["narrative"],
            probability=g["probability"],
            severity=g["severity"],
            precedent=f"{rec['project_name']} ({rec['year']})",
            warnings=g["warnings"],
        )
        db.add(row)
        db.flush()
        db.add(PrecedentRecord(
            scenario_id=row.id,
            project_name=rec["project_name"],
            year=rec["year"],
            industry=rec["industry"],
            what_happened=rec["what_happened"],
            prevention=rec["prevention"],
        ))
        out.append({
            "id": row.id,
            "session_id": session.id,
            "category": row.category,
            "title": row.title,
            "narrative": row.narrative,
            "probability": row.probability,
            "severity": row.severity,
            "precedent": row.precedent,
            "precedent_key": g["precedent_key"],
            "warnings": list(row.warnings or []),
        })
    db.commit()
    return {"session_id": session.id, "scenarios": out}
