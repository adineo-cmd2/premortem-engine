from app.core.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models.failure_scenario import FailureScenario
from app.models.mitigation_action import MitigationAction
from app.models.precedent_record import PrecedentRecord
from app.models.premortem_session import PreMortemSession
from app.models.user import User


def test_session_scenarios_precedent_mitigations_link():
    for table in (MitigationAction.__table__, PrecedentRecord.__table__,
                  FailureScenario.__table__, PreMortemSession.__table__,
                  User.__table__):
        table.drop(bind=engine, checkfirst=True)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    u = User(email="t10@example.com", password_hash=hash_password("secret123"))
    db.add(u)
    db.commit()
    db.refresh(u)
    s = PreMortemSession(
        user_id=u.id,
        name="Launch Apollo",
        description="Ship a new SaaS billing platform.",
        project_type="software",
        launch_date="2026-12-01",
        team_size=8,
        dependencies=["stripe", "postgres"],
        risks="timeline slip",
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    assert s.team_size == 8
    sc1 = FailureScenario(
        session_id=s.id,
        category="technical",
        title="Billing outage at launch",
        narrative="Speculative planning aid: traffic spike breaks billing.",
        probability="high",
        severity="critical",
        precedent="Knight Capital 2012",
        warnings=["error rate spike", "queue growth"],
    )
    sc2 = FailureScenario(
        session_id=s.id,
        category="team",
        title="Key engineer quits",
        narrative="Speculative planning aid: single point of failure leaves.",
        probability="medium",
        severity="high",
        precedent="Illustrative analogue",
        warnings=["overtime trend"],
    )
    db.add_all([sc1, sc2])
    db.commit()
    db.refresh(sc1)
    db.refresh(sc2)
    assert sc1.session_id == s.id
    assert sc2.session_id == s.id
    p = PrecedentRecord(
        scenario_id=sc1.id,
        project_name="Knight Capital",
        year=2012,
        industry="finance",
        what_happened="Trading glitch lost $440M in under an hour.",
        prevention="Staged deploys plus kill switch.",
    )
    m = MitigationAction(
        scenario_id=sc1.id,
        action="Add feature flag and rollback runbook.",
        owner_role="Tech Lead",
        effort="medium",
        timeline_weeks=2,
    )
    db.add_all([p, m])
    db.commit()
    assert db.query(FailureScenario).filter_by(session_id=s.id).count() == 2
    assert db.query(PrecedentRecord).filter_by(scenario_id=sc1.id).count() == 1
    assert db.query(MitigationAction).filter_by(scenario_id=sc1.id).count() == 1
    assert p.year == 2012
    assert m.timeline_weeks == 2
    db.close()
