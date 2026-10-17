# ◈ AI Council Intelligence

A free, research-assisted multi-perspective decision workspace inspired by the multi-agent debate pattern in the [500 AI Agents Projects collection](https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/agents/20-multi-agent-debate).

## What's included

- **Interactive Three.js 3D core** with orbiting wireframes, glowing agent nodes, drag-to-rotate, and zoom.
- **Structured council roles:** Research, Advocate, Challenger, and Judge.
- **Free public web-search attempt** through the `ddgs` package, with result titles, snippets, and source links when available.
- **Research transparency:** if search fails, the app says so and falls back to clearly labeled structured demo reasoning.
- **SQLite session history** for saved debates.
- **Claim review, Plotly report charts, and Markdown export.**
- **No paid API key required.** The app does not call a hosted LLM.

## Run locally

Python 3.10+ recommended.

```bash
py -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

If `py` is unavailable, install Python from https://www.python.org/downloads/ and enable Add Python to PATH.

## Deploy to Streamlit Community Cloud

1. Open https://share.streamlit.io/
2. Choose **Create app** and select `pradeeppullamsetty/ai-council-intelligence`.
3. Set the main file path to `app.py`.
4. Deploy. No secrets are required.

## Important limitations

- The council roles use structured, rule-based reasoning; they are **not independent LLM agents**.
- Search results can be unavailable or incomplete. A search snippet is not verification; open and evaluate the original source before relying on it.
- The 3D canvas loads Three.js from a public CDN, so the animated 3D scene needs network access.
- SQLite history is local to the running app. On hosted ephemeral storage it may reset after restart or redeployment.
- The displayed confidence indicators are illustrative heuristics, not calibrated probabilities.
- This project is a decision-support demo, not a substitute for expert review or primary-source verification.

## Stack

Python · Streamlit · Three.js · Plotly · Pandas · DuckDuckGo search package · SQLite

## Inspiration

The multi-agent debate workflow is inspired by [Project 20 — Multi-Agent Debate](https://github.com/ashishpatel26/500-AI-Agents-Projects/tree/main/agents/20-multi-agent-debate). This repository is an original implementation and interface, not a copy of that project's code.
