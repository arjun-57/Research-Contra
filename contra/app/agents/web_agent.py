"""Web Agent: Searches, scrapes, and collects verified empirical sources."""

from typing import Dict, Any, List
from contra.app.agents.base import BaseAgent
from contra.app.tools.search import search_tool
from contra.app.models.schemas import EvidenceItem


class WebAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Web Agent",
            role_description="Executes targeted queries for both affirmative and disconfirming sources."
        )

    async def run(self, context: Dict[str, Any]) -> List[EvidenceItem]:
        scope = context.get("scope")
        query = scope.operationalized_question if scope else context.get("question", "")

        # Execute dual queries: one seeking growth/support, one seeking bottlenecks/deceleration
        pro_results = await search_tool.search(f"{query} acceleration growth statistics", max_results=3)
        con_results = await search_tool.search(f"{query} deceleration subsidies plateau barriers", max_results=3)

        items: List[EvidenceItem] = []
        counter = 1

        for r in pro_results:
            item = EvidenceItem(
                id=f"EVD-WEB-PRO-{counter:03d}",
                source_title=r.get("title", "Web Source"),
                url=r.get("url", "https://source.internal"),
                source_type=r.get("source_type", "NEWS_REPORTER"),
                raw_quote=r.get("content", ""),
                stance="SUPPORTS",
                credibility_score=r.get("credibility_score", 0.75),
                bias_notes="Affirmative web source retrieval; subject to auditor corroboration."
            )
            items.append(item)
            counter += 1

        for r in con_results:
            item = EvidenceItem(
                id=f"EVD-WEB-CON-{counter:03d}",
                source_title=r.get("title", "Web Source"),
                url=r.get("url", "https://source.internal"),
                source_type=r.get("source_type", "INDUSTRY_DATASET"),
                raw_quote=r.get("content", ""),
                stance="CONTRADICTS",
                credibility_score=r.get("credibility_score", 0.80),
                bias_notes="Skeptical web source retrieval evaluating headwinds and friction."
            )
            items.append(item)
            counter += 1

        return items


web_agent = WebAgent()
