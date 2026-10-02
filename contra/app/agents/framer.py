"""Question Framer: Operationalizes vague queries before search begins."""

from typing import Dict, Any
from contra.app.agents.base import BaseAgent
from contra.app.models.schemas import FramingScope


class QuestionFramer(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Question Framer",
            role_description="Transforms vague or biased research questions into falsifiable, testable empirical inquiries."
        )

    async def run(self, context: Dict[str, Any]) -> FramingScope:
        question = context.get("question", "")
        user_context = context.get("user_context", "")

        prompt = f"""
        Act as the Lead Methodological Scientist and Question Framer for Project Contra.
        We treat research like a court trial, not a standard search.
        Given the following raw user question:
        "{question}"
        User notes: "{user_context}"

        Operationalize this question by defining:
        1. Exact operationalized question (unambiguous, empirical).
        2. Core measurable metric (e.g. second derivative of market share, YoY registration delta).
        3. Relevant sub-segments (e.g. 2W vs 3W vs 4W).
        4. Time horizon.
        5. Pre-registered success criteria (what proves the affirmative case).
        6. Pre-registered falsification criteria (what proves the skeptic's case).
        7. The central crux hypothesis where both sides will diverge.

        Output valid JSON matching this schema:
        {{
            "operationalized_question": str,
            "core_metric": str,
            "target_segments": [str, ...],
            "time_horizon": str,
            "pre_registered_success_criteria": str,
            "pre_registered_falsification_criteria": str,
            "crux_hypothesis": str
        }}
        """

        data = await self.llm.generate_json(prompt)
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            data = data[0]
        elif not isinstance(data, dict):
            data = {}

        return FramingScope(
            original_question=question,
            operationalized_question=data.get("operationalized_question", question),
            core_metric=data.get("core_metric", "Registration volume YoY change"),
            target_segments=data.get("target_segments", ["2W", "3W", "4W"]),
            time_horizon=data.get("time_horizon", "Last 3 fiscal years"),
            pre_registered_success_criteria=data.get("pre_registered_success_criteria", "Positive YoY acceleration in primary segments"),
            pre_registered_falsification_criteria=data.get("pre_registered_falsification_criteria", "Deceleration or growth reliant on transient subsidies"),
            crux_hypothesis=data.get("crux_hypothesis", "Whether organic consumer adoption survives subsidy expiration.")
        )


framer_agent = QuestionFramer()
