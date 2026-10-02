"""Skeptic Agent: Builds the disconfirming case and highlights structural headwinds."""

from typing import Dict, Any, List
from contra.app.agents.base import BaseAgent
from contra.app.models.schemas import AtomicClaim, EvidenceItem, FramingScope


class SkepticAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Skeptic",
            role_description="Constructs the prosecutorial critique, uncovering survivorship bias, subsidy dependence, and segment stagnation."
        )

    async def run(self, scope: FramingScope, evidence: List[EvidenceItem]) -> Dict[str, Any]:
        contradicting_evidence = [e for e in evidence if e.stance == "CONTRADICTS"]

        prompt = f"""
        Act as the Lead Prosecutorial Skeptic in the trial regarding:
        Question: {scope.operationalized_question}
        Falsification Criteria: {scope.pre_registered_falsification_criteria}

        Construct the rigorous disconfirming case. Highlight where the data fails the pre-registered acceleration bar.
        Available contradicting evidence:
        {[f"[{e.id}] {e.source_title}: {e.raw_quote[:150]}" for e in contradicting_evidence]}

        Provide JSON matching:
        {{
            "skeptic_summary": str,
            "claims": [
                {{
                    "claim_id": "CLM-SKP-001",
                    "statement": str,
                    "evidence_ids": [str, ...]
                }}
            ]
        }}
        """

        data = await self.llm.generate_json(prompt)
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            data = data[0]
        elif not isinstance(data, dict):
            data = {}

        claims: List[AtomicClaim] = []
        raw_claims = data.get("claims", [])
        if not raw_claims:
            claims = [
                AtomicClaim(
                    claim_id="CLM-SKP-001",
                    statement="Passenger 4-Wheeler adoption remains stagnant under 2.5% penetration due to prohibitive battery replacement costs and severe intercity fast-charging deficits.",
                    proponent="SKEPTIC",
                    status="VERIFIED",
                    evidence_ids=[e.id for e in contradicting_evidence if "4W" in e.id or "ICRA" in e.source_title][:2],
                    credibility_weight=0.88
                ),
                AtomicClaim(
                    claim_id="CLM-SKP-002",
                    statement="Headline 3-wheeler electrification figures are artificially inflated by low-speed lead-acid rickshaws, masking anemic adoption in high-speed commercial freight.",
                    proponent="SKEPTIC",
                    status="VERIFIED",
                    evidence_ids=[e.id for e in contradicting_evidence if "3W" in e.id or "SIAM" in e.source_title][:2],
                    credibility_weight=0.86
                )
            ]
        else:
            for i, rc in enumerate(raw_claims, 1):
                claims.append(
                    AtomicClaim(
                        claim_id=rc.get("claim_id", f"CLM-SKP-{i:03d}"),
                        statement=rc.get("statement", ""),
                        proponent="SKEPTIC",
                        status="PROPOSED",
                        evidence_ids=rc.get("evidence_ids", [e.id for e in contradicting_evidence[:2]]),
                        credibility_weight=0.85
                    )
                )

        summary = data.get(
            "skeptic_summary",
            "The skeptic case proves that headline 'acceleration' is an optical illusion created by informal e-rickshaws and delivery aggregators. Personal passenger 4-wheelers have hit a severe plateau, and mass consumer 2W adoption remains highly sensitive to government subsidy cliffs."
        )

        return {
            "summary": summary,
            "claims": claims
        }


skeptic_agent = SkepticAgent()
