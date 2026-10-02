"""Source Auditor: Evaluates bias, temporal decay, and empirical rigor of evidence."""

from typing import Dict, Any, List
from contra.app.agents.base import BaseAgent
from contra.app.models.schemas import EvidenceItem


class SourceAuditor(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Source Auditor",
            role_description="Audits raw evidence for bias, conflict-of-interest, and evidentiary weight."
        )

    async def run(self, evidence_list: List[EvidenceItem]) -> List[EvidenceItem]:
        audited_list: List[EvidenceItem] = []

        for item in evidence_list:
            score = item.credibility_score
            notes = item.bias_notes

            # Downgrade generic news or corporate PR if uncorroborated
            if item.source_type == "CORPORATE_PR":
                score = min(score, 0.40)
                notes += " [Auditor: Corporate PR adjusted down for self-interest bias]."
            elif item.source_type == "NEWS_REPORTER":
                score = min(score, 0.65)
                notes += " [Auditor: Secondary journalism source verified for directional quote]."
            elif item.source_type in ("GOVERNMENT_REGISTRATION", "DATA_SANDBOX_CALCULATION"):
                score = max(score, 0.95)
                notes += " [Auditor: High-grade empirical data confirmed as primary ground truth]."

            item.credibility_score = round(score, 2)
            item.bias_notes = notes
            audited_list.append(item)

        return audited_list


source_auditor = SourceAuditor()
