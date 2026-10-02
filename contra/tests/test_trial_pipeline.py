"""Unit and integration tests for Contra research trial pipeline."""

import pytest
import asyncio
from contra.app.ledger.store import EvidenceLedger
from contra.app.models.schemas import EvidenceItem, AtomicClaim
from contra.app.tools.sandbox import DataSandbox
from contra.app.graph.workflow import workflow_engine


def test_evidence_ledger_bayesian_calibration():
    ledger = EvidenceLedger("test-01")

    # Add hard supporting evidence
    ledger.add_evidence(
        EvidenceItem(
            id="EVD-01",
            source_title="Ministry Registry",
            url="https://gov.in",
            source_type="GOVERNMENT_REGISTRATION",
            raw_quote="34% YoY growth in registrations",
            stance="SUPPORTS",
            credibility_score=0.95,
            bias_notes="Official registrar"
        )
    )

    # Add soft contradicting evidence
    ledger.add_evidence(
        EvidenceItem(
            id="EVD-02",
            source_title="Industry Blog",
            url="https://blog.com",
            source_type="NEWS_REPORTER",
            raw_quote="Some buyers are hesitant due to charging wait times",
            stance="CONTRADICTS",
            credibility_score=0.60,
            bias_notes="Anecdotal survey"
        )
    )

    stats = ledger.compute_bayesian_posterior(prior=0.50)
    assert stats["posterior"] > 0.50
    assert stats["bayes_factor"] > 1.0


def test_show_the_math_sandbox_second_derivative():
    res_2w = DataSandbox.execute_second_derivative_analysis(segment="2W")
    assert "latest_volume" in res_2w
    assert "second_derivative_acceleration" in res_2w
    assert "mathematical_verdict" in res_2w

    res_4w = DataSandbox.execute_second_derivative_analysis(segment="4W")
    assert res_4w["segment_analyzed"] == "4W"


@pytest.mark.asyncio
async def test_full_trial_workflow():
    events = []
    final_report = None

    async for ev in workflow_engine.execute_trial(
        question="Is EV adoption in India accelerating?",
        user_context="Focus on 2W and 4W segments",
        deep_mode=False
    ):
        events.append(ev)
        if ev.get("type") == "trial_completed":
            final_report = ev.get("report")

    assert len(events) >= 5
    assert final_report is not None
    assert "calibrated_verdict" in final_report
    assert "confidence_score" in final_report
    assert len(final_report["what_would_change_my_mind"]) >= 1
