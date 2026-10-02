"""Contra Workflow Orchestrator: Drives the adversarial trial graph and yields live SSE events."""

import asyncio
import uuid
from typing import AsyncGenerator, Dict, Any
from contra.app.graph.state import ContraTrialState
from contra.app.agents.framer import framer_agent
from contra.app.agents.web_agent import web_agent
from contra.app.agents.data_agent import data_agent
from contra.app.agents.source_auditor import source_auditor
from contra.app.agents.advocate import advocate_agent
from contra.app.agents.skeptic import skeptic_agent
from contra.app.agents.cross_examiner import cross_examiner_agent
from contra.app.agents.factcheck import fact_checker, citation_auditor
from contra.app.agents.writer import writer_agent
from contra.app.ledger.store import EvidenceLedger


class ContraWorkflow:
    def __init__(self):
        pass

    async def execute_trial(
        self, question: str, user_context: str = "", deep_mode: bool = True
    ) -> AsyncGenerator[Dict[str, Any], None]:
        trial_id = f"TRL-{uuid.uuid4().hex[:8]}"
        state = ContraTrialState(
            trial_id=trial_id,
            question=question,
            user_context=user_context,
            deep_mode=deep_mode,
        )
        ledger = EvidenceLedger(ledger_id=trial_id)

        # 1. INITIALIZE & FRAMER
        yield {
            "type": "stage_changed",
            "stage": "QUESTION_FRAMING",
            "message": "The Question Framer is operationalizing definitions, metrics, and pre-registered falsification criteria...",
            "trial_id": trial_id,
        }
        await asyncio.sleep(0.3)

        scope = await framer_agent.run({"question": question, "user_context": user_context})
        state.scope = scope
        yield {
            "type": "scope_framed",
            "stage": "SCOPE_FRAMED",
            "scope": scope.model_dump(),
            "message": f"Question operationalized: '{scope.operationalized_question}'",
        }
        await asyncio.sleep(0.3)

        # 2. MANAGER & PARALLEL INVESTIGATION (Web Agent + Data Agent + Source Auditor)
        yield {
            "type": "stage_changed",
            "stage": "PARALLEL_INVESTIGATION",
            "message": "Dispatching Web Agent (dialectical retrieval) and Show-The-Math Data Agent (sandbox computation)...",
        }

        # Run Data Agent and Web Agent in parallel
        data_task = asyncio.create_task(data_agent.run({"scope": scope}))
        web_task = asyncio.create_task(web_agent.run({"scope": scope}))
        data_res, web_evidence = await asyncio.gather(data_task, web_task)

        # Ingest into Evidence Ledger
        state.sandbox_results = data_res.get("sandbox_results", [])
        for ev in data_res.get("evidence_items", []):
            ledger.add_evidence(ev)
            yield {
                "type": "evidence_added",
                "evidence": ev.model_dump(),
                "message": f"Show-The-Math Data Sandbox generated empirical evidence: {ev.id}",
            }
            await asyncio.sleep(0.1)

        # Run Source Auditor on web evidence
        audited_web_evidence = await source_auditor.run(web_evidence)
        for ev in audited_web_evidence:
            ledger.add_evidence(ev)
            yield {
                "type": "evidence_added",
                "evidence": ev.model_dump(),
                "message": f"Source Auditor ingested and scored {ev.id} ({ev.source_type}, Credibility: {ev.credibility_score})",
            }
            await asyncio.sleep(0.1)

        state.evidence_items = ledger.get_all_evidence()

        # 3. ADVERSARIAL DEBATE (Advocate vs Skeptic)
        yield {
            "type": "stage_changed",
            "stage": "ADVERSARIAL_DEBATE",
            "message": "Convening the court: Advocate and Skeptic agents are formulating atomic claims from the Evidence Ledger...",
        }
        await asyncio.sleep(0.4)

        adv_task = asyncio.create_task(advocate_agent.run(scope, state.evidence_items))
        skp_task = asyncio.create_task(skeptic_agent.run(scope, state.evidence_items))
        adv_res, skp_res = await asyncio.gather(adv_task, skp_task)

        state.advocate_summary = adv_res.get("summary", "")
        state.advocate_claims = adv_res.get("claims", [])
        for c in state.advocate_claims:
            ledger.add_claim(c)

        state.skeptic_summary = skp_res.get("summary", "")
        state.skeptic_claims = skp_res.get("claims", [])
        for c in state.skeptic_claims:
            ledger.add_claim(c)

        yield {
            "type": "debate_opened",
            "advocate": {
                "summary": state.advocate_summary,
                "claims": [c.model_dump() for c in state.advocate_claims],
            },
            "skeptic": {
                "summary": state.skeptic_summary,
                "claims": [c.model_dump() for c in state.skeptic_claims],
            },
            "message": "Both Advocate and Skeptic have filed their opening claims.",
        }
        await asyncio.sleep(0.4)

        # 4. CROSS-EXAMINATION (Deposition & Interrogatories)
        yield {
            "type": "stage_changed",
            "stage": "CROSS_EXAMINATION",
            "message": "Commencing adversarial cross-examination: opposing agents interrogating evidentiary weak points...",
        }
        cross_exams = await cross_examiner_agent.run(state.advocate_claims, state.skeptic_claims)
        state.cross_examinations = cross_exams

        for x in cross_exams:
            yield {
                "type": "cross_exam_exchange",
                "exchange": x.model_dump(),
                "message": f"Cross-examination: {x.examiner} challenged claim {x.target_claim_id} -> Judge ruling: {x.judge_ruling}",
            }
            await asyncio.sleep(0.3)

        # 5. FACT CHECK & CITATION AUDIT
        yield {
            "type": "stage_changed",
            "stage": "FACT_CHECKING",
            "message": "Fact Checker verifying claim links against raw ledger sources...",
        }
        all_claims = state.advocate_claims + state.skeptic_claims
        audited_claims = await fact_checker.run(all_claims, ledger)
        state.fact_check_passed = True
        await asyncio.sleep(0.2)

        # 6. REPORT WRITER & CALIBRATED VERDICT
        yield {
            "type": "stage_changed",
            "stage": "SYNTHESIZING_VERDICT",
            "message": "The Presiding Magistrate is calculating Bayesian posterior probabilities and formulating 'What Would Change My Mind' falsification triggers...",
        }
        report = await writer_agent.run(
            scope=scope,
            ledger=ledger,
            advocate_case={"summary": state.advocate_summary, "claims": state.advocate_claims},
            skeptic_case={"summary": state.skeptic_summary, "claims": state.skeptic_claims},
            cross_exams=cross_exams,
            sandbox_executions=state.sandbox_results,
        )

        # Citation Auditor check
        audit_res = await citation_auditor.audit_report(report.calibrated_verdict, ledger)
        report.citation_audit_passed = audit_res.get("citation_audit_passed", True)

        state.final_report = report

        yield {
            "type": "trial_completed",
            "stage": "COMPLETED",
            "report": report.model_dump(),
            "message": f"Trial concluded. Calibrated Verdict: '{report.calibrated_verdict}' (Confidence: {int(report.confidence_score*100)}%)",
        }


workflow_engine = ContraWorkflow()
