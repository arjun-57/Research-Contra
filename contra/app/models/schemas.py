"""Pydantic models and schemas for Project Contra research trial engine."""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class FramingScope(BaseModel):
    original_question: str
    operationalized_question: str
    core_metric: str
    target_segments: List[str] = Field(default_factory=list)
    time_horizon: str
    pre_registered_success_criteria: str
    pre_registered_falsification_criteria: str
    crux_hypothesis: str


class EvidenceItem(BaseModel):
    id: str
    source_title: str
    url: str
    source_type: Literal[
        "GOVERNMENT_REGISTRATION",
        "REGULATORY_FILING",
        "ACADEMIC_PEER_REVIEWED",
        "INDUSTRY_DATASET",
        "NEWS_REPORTER",
        "CORPORATE_PR",
        "DATA_SANDBOX_CALCULATION",
    ]
    raw_quote: str
    data_payload: Optional[Dict[str, Any]] = None
    stance: Literal["SUPPORTS", "CONTRADICTS", "NEUTRAL"]
    credibility_score: float = Field(ge=0.0, le=1.0)
    bias_notes: str
    extracted_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AtomicClaim(BaseModel):
    claim_id: str
    statement: str
    proponent: Literal["ADVOCATE", "SKEPTIC", "NEUTRAL"]
    status: Literal["PROPOSED", "VERIFIED", "CHALLENGED", "REFUTED", "STRUCK_BY_AUDITOR"] = "PROPOSED"
    evidence_ids: List[str] = Field(default_factory=list)
    rebuttal_notes: Optional[str] = None
    cross_exam_question: Optional[str] = None
    cross_exam_response: Optional[str] = None
    credibility_weight: float = 0.5


class DataSandboxResult(BaseModel):
    dataset_name: str
    description: str
    code_executed: str
    output_summary: str
    calculated_metrics: Dict[str, Any] = Field(default_factory=dict)
    chart_svg_or_base64: Optional[str] = None
    audit_passed: bool = True


class CrossExamExchange(BaseModel):
    examiner: Literal["ADVOCATE", "SKEPTIC"]
    target_claim_id: str
    interrogatory: str
    response: str
    judge_ruling: Literal["SUSTAINED", "OVERRULED", "STRUCK_DOWN", "NOTED_WITH_RESERVATION"]


class WhatWouldChangeMyMind(BaseModel):
    metric_or_event: str
    threshold: str
    current_observed_state: str
    verdict_consequence: str


class TrialReport(BaseModel):
    report_id: str
    title: str
    original_question: str
    scope: FramingScope
    calibrated_verdict: str
    confidence_score: float = Field(ge=0.0, le=1.0)
    confidence_rationale: str
    prior_probability: float = 0.50
    posterior_probability: float = 0.75
    bayes_factor: float = 3.0
    crux_summary: str
    advocate_case: str
    skeptic_case: str
    data_sandbox_executions: List[DataSandboxResult] = Field(default_factory=list)
    claims: List[AtomicClaim] = Field(default_factory=list)
    evidence_ledger: List[EvidenceItem] = Field(default_factory=list)
    cross_examinations: List[CrossExamExchange] = Field(default_factory=list)
    what_would_change_my_mind: List[WhatWouldChangeMyMind] = Field(default_factory=list)
    citation_audit_passed: bool = True
    struck_claims_count: int = 0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ResearchRequest(BaseModel):
    question: str
    user_context: Optional[str] = None
    segments_focus: Optional[List[str]] = None
    deep_mode: bool = True


class FramingApprovalRequest(BaseModel):
    approved_scope: FramingScope
    user_guidance: Optional[str] = None
