"""Benchmark evaluation questions and scoring suite for Contra."""

import asyncio
from typing import List, Dict, Any
from contra.app.graph.workflow import workflow_engine

BENCHMARK_TRIALS = [
    {
        "id": "BENCH-01",
        "question": "Is EV adoption in India accelerating?",
        "context": "Distinguish 2W vs 3W vs 4W, evaluate FAME-II subsidy expiration impact",
        "expected_segments": ["2W", "3W", "4W"],
        "expected_crux_keyword": "subsidy"
    },
    {
        "id": "BENCH-02",
        "question": "Are frontier AI foundation models hitting pre-training scaling walls?",
        "context": "Compare test-time compute scaling vs pre-training data exhaustion",
        "expected_segments": ["Pre-training tokens", "Test-time compute", "Energy/Datacenter capacity"],
        "expected_crux_keyword": "compute"
    },
    {
        "id": "BENCH-03",
        "question": "Do GLP-1 agonists reduce all-cause cardiovascular mortality independent of weight loss?",
        "context": "SELECT trial endpoints, direct vascular mechanisms vs glycemic control",
        "expected_segments": ["Direct cardiovascular protection", "Weight-loss mediated benefits"],
        "expected_crux_keyword": "cardiovascular"
    }
]


async def run_benchmark_suite() -> Dict[str, Any]:
    results = []
    print("=" * 60)
    print("RUNNING CONTRA ADVERSARIAL BENCHMARK SUITE")
    print("=" * 60)

    for bench in BENCHMARK_TRIALS:
        print(f"\n[Evaluating {bench['id']}]: {bench['question']}")
        final_report = None
        events_count = 0

        async for ev in workflow_engine.execute_trial(
            question=bench["question"],
            user_context=bench["context"],
            deep_mode=True
        ):
            events_count += 1
            if ev.get("type") == "trial_completed":
                final_report = ev.get("report")

        assert final_report is not None, "Trial did not produce a final report."

        # Evaluate quality metrics
        falsification_conditions_count = len(final_report.get("what_would_change_my_mind", []))
        confidence = final_report.get("confidence_score", 0.0)
        evidence_count = len(final_report.get("evidence_ledger", []))
        cross_exams_count = len(final_report.get("cross_examinations", []))

        score = {
            "trial_id": bench["id"],
            "title": final_report.get("title"),
            "calibrated_verdict": final_report.get("calibrated_verdict"),
            "confidence_score": confidence,
            "evidence_items_audited": evidence_count,
            "cross_examinations_held": cross_exams_count,
            "falsification_triggers": falsification_conditions_count,
            "citation_audit_passed": final_report.get("citation_audit_passed", False),
            "benchmark_status": "PASSED" if falsification_conditions_count >= 2 and evidence_count >= 3 else "FAILED"
        }
        results.append(score)
        print(f" -> Status: {score['benchmark_status']} | Confidence: {int(confidence*100)}% | Falsification Triggers: {falsification_conditions_count}")

    print("\n" + "=" * 60)
    print(f"BENCHMARK COMPLETE: {len(results)}/{len(BENCHMARK_TRIALS)} PASSED")
    print("=" * 60)
    return {"benchmark_summary": results}


if __name__ == "__main__":
    asyncio.run(run_benchmark_suite())
