"""Admin routes — stats, traces, A/B testing, diagnostics (Phase 11)."""

from fastapi import APIRouter

from app.core.metrics import get_metrics
from app.core.tracing import get_latest_traces, get_session_trace

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats")
async def admin_stats():
    """Get system metrics: routing, latency, error rate."""
    return get_metrics()


@router.get("/traces/latest")
async def admin_traces_latest():
    """Get the 10 most recent session traces."""
    return {"traces": get_latest_traces(10)}


@router.get("/traces/{session_id}")
async def admin_traces_session(session_id: str):
    """Get the full trace for a specific session."""
    return {
        "session_id": session_id,
        "spans": get_session_trace(session_id),
    }


@router.get("/diagnostics")
async def admin_diagnostics():
    """Full system diagnostic dump."""
    import sys
    from app.skills.registry import get_skill_registry
    from app.routers.system1 import PATTERNS as s1_patterns

    registry = get_skill_registry()

    return {
        "version": "0.1.0",
        "python": sys.version,
        "metrics": get_metrics(),
        "skills_loaded": registry.count,
        "s1_patterns": len(s1_patterns),
        "models": ["gpt-5.4-mini"],
    }


# ── Conversation log viewer ──────────────────────────────────

@router.get("/conversations/recent")
async def conversations_recent(limit: int = 20):
    """View recent conversation turns for debugging."""
    from app.core.conversation_logger import read_recent_logs
    return {"turns": read_recent_logs(limit)}


@router.get("/conversations/{session_id}")
async def conversations_session(session_id: str):
    """View all turns for a specific session."""
    from app.core.conversation_logger import get_session_logs
    return {"session_id": session_id, "turns": get_session_logs(session_id)}


@router.post("/conversations/clear")
async def conversations_clear():
    """Clear the conversation log file."""
    from app.core.conversation_logger import clear_logs
    count = clear_logs()
    return {"cleared": count}
