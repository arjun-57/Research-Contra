"""FastAPI Routes and SSE streaming for Project Contra."""

import json
import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from sse_starlette.sse import EventSourceResponse

from contra.app.models.schemas import ResearchRequest, TrialReport
from contra.app.graph.workflow import workflow_engine
from contra.app.tools.sandbox import DataSandbox
from contra.app.core.llm import llm_client
from contra.app.core.config import settings

router = APIRouter(prefix="/api")

# Active cache of completed reports
trial_cache: Dict[str, TrialReport] = {}


@router.get("/health")
async def health_check():
    return {
        "status": "active",
        "project": "Contra: Research Team That Argues With Itself",
        "version": "1.0.0",
        "llm_provider": "Google GenAI SDK (gemini-3.8-flash)" if llm_client.is_live() else "Empirical Fallback Simulator",
        "has_gemini_key": bool(settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY),
        "has_tavily_key": bool(settings.TAVILY_API_KEY),
    }


@router.post("/trials/run", response_model=TrialReport)
async def run_trial_direct(request: ResearchRequest):
    """Executes full research trial and returns the calibrated report."""
    last_report = None
    async for event in workflow_engine.execute_trial(
        question=request.question,
        user_context=request.user_context or "",
        deep_mode=request.deep_mode,
    ):
        if event.get("type") == "trial_completed" and "report" in event:
            last_report = event["report"]

    if not last_report:
        raise HTTPException(status_code=500, detail="Trial failed to generate final report.")

    report_obj = TrialReport(**last_report)
    trial_cache[report_obj.report_id] = report_obj
    return report_obj


@router.get("/trials/stream")
async def stream_trial(question: str = Query(...), user_context: str = Query("")):
    """Streams live courtroom trial progression via Server-Sent Events (SSE)."""

    async def event_generator():
        async for event in workflow_engine.execute_trial(
            question=question,
            user_context=user_context,
            deep_mode=True,
        ):
            if event.get("type") == "trial_completed" and "report" in event:
                rep = TrialReport(**event["report"])
                trial_cache[rep.report_id] = rep
            yield {
                "event": "message",
                "data": json.dumps(event)
            }

    return EventSourceResponse(event_generator())


@router.get("/trials/{trial_id}", response_model=Optional[TrialReport])
async def get_cached_trial(trial_id: str):
    if trial_id in trial_cache:
        return trial_cache[trial_id]
    raise HTTPException(status_code=404, detail="Trial ID not found in memory.")


@router.post("/sandbox/second-derivative")
async def run_sandbox_analysis(segment: str = "2W"):
    """Show-The-Math endpoint: calculates empirical second derivative on VAHAN data."""
    try:
        res = DataSandbox.execute_second_derivative_analysis(segment=segment)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sandbox/custom-code")
async def run_custom_sandbox_code(payload: Dict[str, str]):
    code = payload.get("code", "")
    res = DataSandbox.execute_custom_code(code)
    return res
