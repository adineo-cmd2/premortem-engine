from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.session import Base, engine
import app.models.user  # noqa: F401
import app.models.premortem_session  # noqa: F401
import app.models.failure_scenario  # noqa: F401
import app.models.precedent_record  # noqa: F401
import app.models.mitigation_action  # noqa: F401
from app.api.routes import premortem

settings = get_settings()
Base.metadata.create_all(bind=engine)
app = FastAPI(title="AI Pre-Mortem Engine")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://127.0.0.1:4330"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz():
    return {"ok": True}


app.include_router(premortem.router, prefix="/api/premortem", tags=["premortem"])
