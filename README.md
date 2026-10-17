# ◈ AI Council — Multi-Agent Intelligence Platform

A premium, animated Streamlit experience for structured multi-perspective decision analysis. Inspired by the multi-agent debate pattern in the [500 AI Agents Projects collection](https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/agents/20-multi-agent-debate), with an original UI and demo implementation.

## Experience

- **3D-inspired animated reasoning core** with orbiting rings, glow, and floating motion.
- **Four specialist roles:** Research, Advocate, Challenger, and Judge.
- **Debate Studio** with topic presets, context, and configurable rounds.
- **Interactive intelligence report** with Plotly visualizations.
- **Claim review panel**, balanced verdict, unresolved questions, and Markdown export.
- **Responsive dark interface** with Space Grotesk, Manrope, and DM Mono typography.
- **Demo mode works without API keys.**

## Run locally

Python 3.10+ recommended.

```bash
py -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

If `py` is not available on your machine, install Python from https://www.python.org/downloads/ and enable the option to add Python to PATH.

## Deploy to Streamlit Community Cloud

1. Sign in at https://share.streamlit.io/
2. Choose **Create app** and select this repository.
3. Set the main file path to `app.py`.
4. Deploy. No secrets are required for demo mode.

## Important: demo mode vs. real AI

The current version uses deterministic, rule-based sample arguments so the complete experience works with **no API key**. It does **not** browse the web, verify factual claims, or call an LLM. Scores are illustrative heuristics—not calibrated probabilities.

A production upgrade can add:
- LangGraph orchestration and typed agent state.
- Optional LLM provider configured through Streamlit Secrets.
- Trusted-source retrieval with clickable citations and claim-level provenance.
- Evaluation tests, run history, and SQLite persistence.

## Tech stack

Python · Streamlit · Plotly · Pandas · custom CSS animations

## Project inspiration

The multi-agent debate workflow pattern is inspired by [Project 20 — Multi-Agent Debate](https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/agents/20-multi-agent-debate). This repository is an original interface/demo implementation, not a copy of that project's code.
