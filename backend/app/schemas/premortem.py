from typing import Optional

from pydantic import BaseModel, Field


class PremortemSubmitIn(BaseModel):
    project_name: str
    description: str = ""
    project_type: str = "general"
    launch_date: str = ""
    team_size: int = 0
    key_dependencies: list[str] = Field(default_factory=list)
    known_risks: str = ""


class ScenarioOut(BaseModel):
    id: int
    session_id: int
    category: str
    title: str
    narrative: str
    probability: str
    severity: str
    precedent: str = ""
    warnings: list = Field(default_factory=list)

    class Config:
        from_attributes = True


class PrecedentOut(BaseModel):
    id: int
    scenario_id: int
    project_name: str
    year: int
    industry: str
    what_happened: str
    prevention: str

    class Config:
        from_attributes = True


class MitigationOut(BaseModel):
    id: int
    scenario_id: int
    action: str
    owner_role: str
    effort: str
    timeline_weeks: int

    class Config:
        from_attributes = True


class PremortemSubmitOut(BaseModel):
    session_id: int
    scenarios: list = Field(default_factory=list)


class MitigateIn(BaseModel):
    scenario_ids: list[int] = Field(default_factory=list)


class RiskPoint(BaseModel):
    scenario_id: int
    x: int
    y: int
    title: str
    severity: str
    probability: str


class RiskMatrixOut(BaseModel):
    session_id: int
    points: list[RiskPoint] = Field(default_factory=list)
