"""Graph state definition for Project Contra workflow."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from contra.app.models.schemas import (
    FramingScope,
    EvidenceItem,
    AtomicClaim,
    CrossExamExchange,
    DataSandboxResult,
    TrialReport,
)


class ContraTrialState(BaseModel):
    trial_id: str
    question: str
    user_context: Optional[str] = None
    deep_mode: bool = True
    loop_count: int = 0
    max_loops: int = 2

    # Step states
    current_stage: str = "INITIALIZED"
    scope: Optional[FramingScope] = None
    evidence_items: List[EvidenceItem] = Field(default_factory=list)
    sandbox_results: List[DataSandboxResult] = Field(default_factory=list)

    # Adversarial debate state
    advocate_summary: str = ""
    advocate_claims: List[AtomicClaim] = Field(default_factory=list)
    skeptic_summary: str = ""
    skeptic_claims: List[AtomicClaim] = Field(default_factory=list)
    cross_examinations: List[CrossExamExchange] = Field(default_factory=list)

    # Auditing and Output
    fact_check_passed: bool = True
    citation_audit_passed: bool = True
    final_report: Optional[TrialReport] = None
    event_log: List[Dict[str, Any]] = Field(default_factory=list)
