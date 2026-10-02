"""Evidence Ledger: The single source of truth for Project Contra."""

import uuid
from typing import Dict, List, Optional
from contra.app.models.schemas import EvidenceItem, AtomicClaim, WhatWouldChangeMyMind


class EvidenceLedger:
    def __init__(self, ledger_id: Optional[str] = None):
        self.ledger_id = ledger_id or str(uuid.uuid4())[:8]
        self.evidence: Dict[str, EvidenceItem] = {}
        self.claims: Dict[str, AtomicClaim] = {}
        self.what_would_change_my_mind: List[WhatWouldChangeMyMind] = []
        self.struck_claims: List[str] = []

    def add_evidence(self, item: EvidenceItem) -> str:
        self.evidence[item.id] = item
        return item.id

    def add_claim(self, claim: AtomicClaim) -> str:
        self.claims[claim.claim_id] = claim
        return claim.claim_id

    def link_claim(self, claim_id: str, evidence_id: str):
        if claim_id in self.claims and evidence_id in self.evidence:
            if evidence_id not in self.claims[claim_id].evidence_ids:
                self.claims[claim_id].evidence_ids.append(evidence_id)

    def strike_claim(self, claim_id: str, reason: str):
        if claim_id in self.claims:
            self.claims[claim_id].status = "STRUCK_BY_AUDITOR"
            self.claims[claim_id].rebuttal_notes = reason
            if claim_id not in self.struck_claims:
                self.struck_claims.append(claim_id)

    def get_all_evidence(self) -> List[EvidenceItem]:
        return list(self.evidence.values())

    def get_all_claims(self) -> List[AtomicClaim]:
        return list(self.claims.values())

    def get_verified_claims(self) -> List[AtomicClaim]:
        return [c for c in self.claims.values() if c.status in ("VERIFIED", "PROPOSED", "CHALLENGED")]

    def compute_bayesian_posterior(self, prior: float = 0.50) -> Dict[str, float]:
        """
        Computes calibrated posterior probability and Bayes factor based on
        hard evidence vs contradicted evidence credibility weights.
        """
        support_weight = 0.0
        contradict_weight = 0.0

        weight_map = {
            "GOVERNMENT_REGISTRATION": 1.0,
            "DATA_SANDBOX_CALCULATION": 1.0,
            "REGULATORY_FILING": 0.90,
            "ACADEMIC_PEER_REVIEWED": 0.85,
            "INDUSTRY_DATASET": 0.70,
            "NEWS_REPORTER": 0.45,
            "CORPORATE_PR": 0.25,
        }

        for ev in self.evidence.values():
            base_w = weight_map.get(ev.source_type, 0.5) * ev.credibility_score
            if ev.stance == "SUPPORTS":
                support_weight += base_w
            elif ev.stance == "CONTRADICTS":
                contradict_weight += base_w

        # Avoid zero division
        denominator = support_weight + contradict_weight
        if denominator == 0:
            return {
                "prior": prior,
                "posterior": prior,
                "bayes_factor": 1.0,
                "support_mass": 0.0,
                "contradict_mass": 0.0,
            }

        # Bayes factor approximation
        likelihood_ratio = (support_weight + 0.1) / (contradict_weight + 0.1)
        prior_odds = prior / (1.0 - prior)
        posterior_odds = prior_odds * likelihood_ratio
        posterior = posterior_odds / (1.0 + posterior_odds)

        # Bound nicely between 0.05 and 0.95 to reflect honest calibration
        calibrated_posterior = max(0.05, min(0.95, round(posterior, 3)))
        return {
            "prior": prior,
            "posterior": calibrated_posterior,
            "bayes_factor": round(likelihood_ratio, 2),
            "support_mass": round(support_weight, 2),
            "contradict_mass": round(contradict_weight, 2),
        }
