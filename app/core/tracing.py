"""Span-based tracing — every decision logged (Phase 11)."""

import time
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class TraceSpan:
    name: str
    start_ms: float
    end_ms: float = 0
    metadata: dict = field(default_factory=dict)


_traces: dict[str, list[TraceSpan]] = defaultdict(list)
_active_spans: dict[str, dict[str, float]] = defaultdict(dict)


def start_span(session_id: str, name: str, **meta) -> None:
    """Start a trace span for a session."""
    _active_spans[session_id][name] = time.perf_counter() * 1000


def end_span(session_id: str, name: str, **meta) -> TraceSpan:
    """End a trace span and record it."""
    start_ms = _active_spans[session_id].pop(name, 0)
    span = TraceSpan(
        name=name,
        start_ms=start_ms,
        end_ms=time.perf_counter() * 1000,
        metadata=meta,
    )
    _traces[session_id].append(span)
    return span


def get_session_trace(session_id: str) -> list[dict]:
    """Get all spans for a session."""
    spans = _traces.get(session_id, [])
    return [
        {
            "name": s.name,
            "duration_ms": round(s.end_ms - s.start_ms, 2),
            "metadata": s.metadata,
        }
        for s in spans
    ]


def get_latest_traces(limit: int = 10) -> list[dict]:
    """Get the most recent session traces."""
    sessions = list(_traces.keys())[-limit:]
    return [
        {"session_id": sid, "spans": get_session_trace(sid)}
        for sid in sessions
    ]


def clear_session_trace(session_id: str) -> None:
    """Clear traces for a session."""
    _traces.pop(session_id, None)
    _active_spans.pop(session_id, None)
