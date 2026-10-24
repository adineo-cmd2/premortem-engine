from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.failure_scenario import FailureScenario
from app.models.mitigation_action import MitigationAction
from app.models.precedent_record import PrecedentRecord
from app.models.premortem_session import PreMortemSession
from app.models.user import User
from app.schemas.premortem import MitigateIn, PremortemSubmitIn, PremortemSubmitOut
from app.services import premortem_pipeline
from app.services.mitigation_planner import plan
from app.services.report_generator import render
from app.services.risk_matrix_builder import build

router = APIRouter()

PTYPES = {"software", "hardware", "research", "event", "business", "general", "default"}


def _own_session(db: Session, user: User, sid: int) -> PreMortemSession:
    s = db.query(PreMortemSession).filter(
        PreMortemSession.id == sid,
        PreMortemSession.user_id == user.id,
    ).first()
    if not s:
        raise HTTPException(status_code=404, detail="Session not found")
    return s


def _scenarios_for(db: Session, session_id: int):
    return db.query(FailureScenario).filter(
        FailureScenario.session_id == session_id
    ).order_by(FailureScenario.id).all()


def _precedent_for(db: Session, scenario_id: int):
    return db.query(PrecedentRecord).filter(
        PrecedentRecord.scenario_id == scenario_id
    ).first()


def _precedent_dict(p: PrecedentRecord | None) -> dict:
    if not p:
        return {}
    return {
        "id": p.id,
        "scenario_id": p.scenario_id,
        "project_name": p.project_name,
        "year": p.year,
        "industry": p.industry,
        "what_happened": p.what_happened,
        "prevention": p.prevention,
    }


def _scenario_full(db: Session, sc: FailureScenario) -> dict:
    prec = _precedent_for(db, sc.id)
    return {
        "id": sc.id,
        "session_id": sc.session_id,
        "category": sc.category,
        "title": sc.title,
        "narrative": sc.narrative,
        "probability": sc.probability,
        "severity": sc.severity,
        "precedent": sc.precedent or "",
        "warnings": list(sc.warnings or []),
        "precedent_record": _precedent_dict(prec),
        "precedent_detail": _precedent_dict(prec),
    }


@router.post("/submit", response_model=PremortemSubmitOut)
def submit(body: PremortemSubmitIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not (body.project_name or "").strip():
        raise HTTPException(status_code=400, detail="project_name required")
    if not (body.description or "").strip():
        raise HTTPException(status_code=400, detail="description required")
    ptype = (body.project_type or "").lower().strip() or "general"
    if ptype not in PTYPES:
        ptype = "general"
    result = premortem_pipeline.run_premortem(
        db,
        user.id,
        body.project_name.strip(),
        body.description.strip(),
        ptype,
        body.launch_date or "",
        body.team_size or 0,
        body.key_dependencies or [],
        body.known_risks or "",
    )
    return PremortemSubmitOut(session_id=result["session_id"], scenarios=result["scenarios"])


@router.get("/history")
def history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    sessions = db.query(PreMortemSession).filter(
        PreMortemSession.user_id == user.id
    ).order_by(PreMortemSession.id).all()
    out = []
    for s in sessions:
        count = db.query(FailureScenario).filter(
            FailureScenario.session_id == s.id
        ).count()
        out.append(
            {
                "id": s.id,
                "name": s.name,
                "project_name": s.name,
                "description": s.description,
                "project_type": s.project_type,
                "launch_date": s.launch_date,
                "team_size": s.team_size,
                "scenarios": count,
            }
        )
    return out


@router.get("/{sid}/scenarios")
def get_scenarios(sid: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    s = _own_session(db, user, sid)
    rows = _scenarios_for(db, s.id)
    return [_scenario_full(db, sc) for sc in rows]


@router.get("/{sid}/risk-matrix")
def get_risk_matrix(sid: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    s = _own_session(db, user, sid)
    rows = _scenarios_for(db, s.id)
    matrix = build(rows)
    return {"session_id": s.id, "points": matrix["points"], "axes": matrix["axes"]}


@router.post("/{sid}/mitigate")
def mitigate(sid: int, body: MitigateIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    s = _own_session(db, user, sid)
    rows = _scenarios_for(db, s.id)
    by_id = {sc.id: sc for sc in rows}
    for target in body.scenario_ids or []:
        if target not in by_id:
            raise HTTPException(status_code=404, detail="Scenario not found")
    created = []
    for target in body.scenario_ids or []:
        sc = by_id[target]
        db.query(MitigationAction).filter(
            MitigationAction.scenario_id == target
        ).delete(synchronize_session=False)
        db.flush()
        planned = plan(
            {"category": sc.category, "title": sc.title, "name": s.name},
            count=4,
        )
        for entry in planned:
            row = MitigationAction(
                scenario_id=target,
                action=entry["action"],
                owner_role=entry["owner_role"],
                effort=entry["effort"],
                timeline_weeks=entry["timeline_weeks"],
            )
            db.add(row)
            db.flush()
            created.append(
                {
                    "id": row.id,
                    "scenario_id": row.scenario_id,
                    "action": row.action,
                    "owner_role": row.owner_role,
                    "effort": row.effort,
                    "timeline_weeks": row.timeline_weeks,
                }
            )
    db.commit()
    return {"mitigations": created}


@router.get("/{sid}/mitigations")
def get_mitigations(sid: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    s = _own_session(db, user, sid)
    rows = _scenarios_for(db, s.id)
    grouped = []
    for sc in rows:
        mits = db.query(MitigationAction).filter(
            MitigationAction.scenario_id == sc.id
        ).order_by(MitigationAction.id).all()
        grouped.append(
            {
                "scenario_id": sc.id,
                "title": sc.title,
                "category": sc.category,
                "mitigations": [
                    {
                        "id": m.id,
                        "scenario_id": m.scenario_id,
                        "action": m.action,
                        "owner_role": m.owner_role,
                        "effort": m.effort,
                        "timeline_weeks": m.timeline_weeks,
                    }
                    for m in mits
                ],
            }
        )
    return grouped


@router.get("/{sid}/report")
def get_report(sid: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    s = _own_session(db, user, sid)
    rows = _scenarios_for(db, s.id)
    enriched = []
    for sc in rows:
        prec = _precedent_for(db, sc.id)
        mits = db.query(MitigationAction).filter(
            MitigationAction.scenario_id == sc.id
        ).order_by(MitigationAction.id).all()
        enriched.append(
            {
                "title": sc.title,
                "category": sc.category,
                "probability": sc.probability,
                "severity": sc.severity,
                "narrative": sc.narrative,
                "precedent": _precedent_dict(prec) or (sc.precedent or ""),
                "warnings": list(sc.warnings or []),
                "mitigations": [
                    {
                        "action": m.action,
                        "owner_role": m.owner_role,
                        "effort": m.effort,
                        "timeline_weeks": m.timeline_weeks,
                    }
                    for m in mits
                ],
            }
        )
    session_dict = {
        "name": s.name,
        "project_name": s.name,
        "description": s.description,
        "project_type": s.project_type,
    }
    md = render(session_dict, enriched)
    return {"markdown": md}


@router.delete("/{sid}")
def delete_session(sid: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    s = _own_session(db, user, sid)
    rows = _scenarios_for(db, s.id)
    for sc in rows:
        db.query(PrecedentRecord).filter(
            PrecedentRecord.scenario_id == sc.id
        ).delete(synchronize_session=False)
        db.query(MitigationAction).filter(
            MitigationAction.scenario_id == sc.id
        ).delete(synchronize_session=False)
        db.flush()
        db.query(FailureScenario).filter(
            FailureScenario.id == sc.id
        ).delete(synchronize_session=False)
    db.flush()
    db.query(PreMortemSession).filter(
        PreMortemSession.id == s.id
    ).delete(synchronize_session=False)
    db.commit()
    return {"ok": True}
