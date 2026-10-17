"""Free research-assisted council engine.

Uses DuckDuckGo search results when available; never labels generated arguments as verified facts.
No paid API key or hosted LLM is required. Agent reasoning is structured heuristics, not an LLM.
"""
from datetime import datetime
import re

def search_sources(query: str, limit: int = 5) -> list[dict]:
    try:
        from ddgs import DDGS
        with DDGS() as ddgs:
            rows = list(ddgs.text(query, max_results=limit))
        clean = []
        for row in rows:
            title = str(row.get("title", "")).strip()
            href = str(row.get("href", row.get("url", ""))).strip()
            body = re.sub(r"\s+", " ", str(row.get("body", ""))).strip()
            if title and href.startswith("http"):
                clean.append({"title": title, "url": href, "snippet": body[:650]})
        return clean
    except Exception:
        return []

def run_free_council(topic: str, rounds: int = 3, context: str = "") -> dict:
    sources = search_sources(topic, 5)
    snippets = [s["snippet"] for s in sources if s.get("snippet")]
    evidence_note = ("Search snippets were retrieved; open each source to verify the context and date."
                     if sources else "Live search was unavailable. This run uses structured demo reasoning only.")
    pro = [
        f"The strongest case for “{topic}” is the potential upside. The proposal should be evaluated against a clear objective and measurable success criteria.",
        "A controlled pilot can test the most important assumptions while limiting cost and unintended consequences.",
        "Benefits are more credible when independent sources, baseline measurements, and transparent evaluation support them."
    ]
    con = [
        "The main risk is treating a plausible argument as proof. Context, implementation costs, and unintended consequences may change the outcome.",
        "Evidence may be incomplete, outdated, or specific to a different setting; search snippets alone are not enough to establish causality.",
        "Without a stop condition, owner, and independent review, a pilot can continue despite weak results."
    ]
    if snippets:
        pro[0] = "Research scan: " + snippets[0]
        if len(snippets) > 1:
            con[0] = "Counterpoint to investigate: " + snippets[1]
        if len(snippets) > 2:
            pro[1] = "Additional context to assess: " + snippets[2]
    rounds_out = []
    for i in range(max(1, min(3, int(rounds)))):
        rounds_out.append({"round": i + 1, "pro": pro[i], "con": con[i],
                           "focus": ["Initial evidence scan", "Assumptions & trade-offs", "Decision test"][i]})
    verdict = ("Provisional verdict: do not treat this as a factual conclusion yet. Compare the strongest supporting and opposing evidence, "
               "check source dates and original studies, and run a small reversible test with explicit success and stop criteria. "
               + evidence_note)
    if context.strip():
        verdict += " Context supplied by the user: " + context.strip()[:500]
    claims = [
        {"claim": "The proposal may help achieve the stated objective.", "status": "Hypothesis — test locally", "confidence": 50},
        {"claim": "A staged pilot can reduce implementation risk.", "status": "Practical safeguard; context-dependent", "confidence": 65},
        {"claim": "Search snippets establish the overall truth of the proposal.", "status": "Not established — open and verify sources", "confidence": 15}
    ]
    return {"topic": topic, "rounds": rounds_out, "verdict": verdict, "confidence": 50,
            "pro_score": 50, "con_score": 50, "claims": claims, "context": context,
            "sources": sources, "research_status": "Sources found" if sources else "Search unavailable / demo fallback",
            "generated_at": datetime.now().isoformat(timespec="seconds")}
