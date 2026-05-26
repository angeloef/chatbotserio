"""FastAPI application entry point — ChatbotSerio."""

from contextlib import asynccontextmanager
import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.core.config import settings
from app.core.database import create_tables, engine, ping_db
from app.api.routes.chat import router as chat_router
from app.api.routes.simulate import router as simulate_router
from app.api.routes.admin import router as admin_router
from app.skills.registry import get_skill_registry
from app.skills.mcp_server import handle_mcp_request_raw


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"ChatbotSerio v{__import__('app').__version__} starting | env={settings.ENVIRONMENT}")
    await create_tables()
    logger.info("Database tables verified/created")

    # Load skills
    registry = get_skill_registry()
    logger.info(f"Loaded {registry.count} skills")
    yield
    logger.info("ChatbotSerio shutting down")
    await engine.dispose()


app = FastAPI(
    title="ChatbotSerio",
    description="Agentic AI Chatbot — stratified autonomy, skill ecosystem, 4-tier memory",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(chat_router)
app.include_router(simulate_router)
app.include_router(admin_router)

# Mount static files for chat UI
import os
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.isdir(static_dir):
    app.mount("/ui", StaticFiles(directory=static_dir, html=True), name="static")


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}


@app.get("/health/ready")
async def health_ready():
    db_ok = await ping_db()
    redis_ok = await _ping_redis()

    all_ok = db_ok and redis_ok
    return {
        "status": "ready" if all_ok else "degraded",
        "checks": {
            "database": "connected" if db_ok else "disconnected",
            "redis": "connected" if redis_ok else "disconnected",
        },
    }


async def _ping_redis() -> bool:
    try:
        import redis.asyncio as aioredis
        r = aioredis.from_url(settings.REDIS_URL, socket_connect_timeout=2)
        await r.ping()
        await r.aclose()
        return True
    except Exception:
        return False


# ── MCP endpoint ─────────────────────────────────────────────


@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """MCP JSON-RPC 2.0 endpoint — exposes all skills as MCP tools."""
    body = await request.body()
    result = handle_mcp_request_raw(body.decode("utf-8"))
    return JSONResponse(content=json.loads(result))


# ── Skills management ────────────────────────────────────────


@app.post("/skills/reload")
async def reload_skills():
    """Hot-reload all skills from SKILL.md files."""
    registry = get_skill_registry()
    results = registry.hot_reload()
    return {
        "reloaded": sum(1 for v in results.values() if v == "reloaded"),
        "added": sum(1 for v in results.values() if v == "added"),
        "removed": sum(1 for v in results.values() if v == "removed"),
        "unchanged": sum(1 for v in results.values() if v == "unchanged"),
        "details": results,
        "total_skills": registry.count,
    }


@app.get("/skills")
async def list_skills():
    """List all loaded skills with metadata."""
    registry = get_skill_registry()
    return {
        "count": registry.count,
        "skills": [
            {
                "name": s.name,
                "version": s.version,
                "category": s.category,
                "description": s.description,
                "summary_tokens": s.level1_tokens,
            }
            for s in registry.skills.values()
        ],
    }


# ── Memory consolidation (Phase 7) ────────────────────────────

from pydantic import BaseModel


class ConsolidateRequest(BaseModel):
    session_id: str
    phone: str = ""


@app.post("/admin/consolidate")
async def consolidate_session(request: ConsolidateRequest):
    """Run memory consolidation after a session ends.

    Saves episode summary, updates persona, and updates zone stats.
    """
    from app.core.belief_state import get_belief
    from app.memory.consolidation import consolidate_session as run_consolidation

    belief = get_belief(request.session_id)
    results = await run_consolidation(belief, phone=request.phone)
    return results


@app.get("/admin/memory/{phone}")
async def get_user_memory(phone: str):
    """Get all memory tiers for a user (debug/diagnostic)."""
    from app.memory.episodic import get_episodes
    from app.memory.user_model import get_persona
    from app.memory.procedural import get_skill_stats

    return {
        "phone": phone,
        "persona": await get_persona(phone),
        "episodes": await get_episodes(phone, limit=5),
        "skill_stats": await get_skill_stats(phone),
    }


# ── Proactive engine (Phase 8) ─────────────────────────────────

@app.get("/admin/proactive")
async def proactive_check():
    """Check for proactive alerts across all zones."""
    from app.core.proactive_engine import get_proactive_summary
    return await get_proactive_summary()
