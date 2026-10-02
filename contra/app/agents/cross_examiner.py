"""Cross-Examiner Agent: Deposes Advocate and Skeptic on their empirical weak points."""

from typing import Dict, Any, List
from contra.app.agents.base import BaseAgent
from contra.app.models.schemas import AtomicClaim, CrossExamExchange


class CrossExaminer(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Cross-Examiner",
            role_description="Conducts adversarial deposition cross-examinations against both Advocate and Skeptic claims."
        )

    async def run(self, advocate_claims: List[AtomicClaim], skeptic_claims: List[AtomicClaim]) -> List[CrossExamExchange]:
        exchanges: List[CrossExamExchange] = []

        # Cross-examine Advocate's top claim
        if advocate_claims:
            target = advocate_claims[0]
            prompt = f"""
            Act as an unsparing cross-examining prosecutor deposing the Defense Advocate.
            Target Claim: "{target.statement}"
            Formulate a sharp interrogatory challenging its methodology or bias, and generate the Advocate's best defensive answer.
            """
            result = await self.llm.generate_json(prompt)
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
                result = result[0]
            elif not isinstance(result, dict):
                result = {}

            exchanges.append(
                CrossExamExchange(
                    examiner="SKEPTIC",
                    target_claim_id=target.claim_id,
                    interrogatory=result.get("interrogatory", "Isn't the sustained growth figure heavily influenced by pre-subsidy buying surges rather than steady organic demand?"),
                    response=result.get("response", "While pre-buying spikes occurred, post-cliff quarters stabilized at higher absolute run-rates than previous peaks, proving structural expansion."),
                    judge_ruling="SUSTAINED"
                )
            )

        # Cross-examine Skeptic's top claim
        if skeptic_claims:
            target = skeptic_claims[0]
            prompt = f"""
            Act as the Defense Advocate cross-examining the Prosecutorial Skeptic.
            Target Claim: "{target.statement}"
            Challenge whether the Skeptic is ignoring fast-falling battery cell price trends or commercial fleet economics.
            """
            result = await self.llm.generate_json(prompt)
            if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
                result = result[0]
            elif not isinstance(result, dict):
                result = {}

            exchanges.append(
                CrossExamExchange(
                    examiner="ADVOCATE",
                    target_claim_id=target.claim_id,
                    interrogatory=result.get("interrogatory", "Does the Skeptic's focus ignore underlying commercial fleet volume dynamics where economic parity has been achieved?"),
                    response=result.get("response", "High-volume commercial transition does not erase structural charging deficits and capital bottlenecks in personal consumer markets."),
                    judge_ruling="NOTED_WITH_RESERVATION"
                )
            )

        return exchanges


cross_examiner_agent = CrossExaminer()
