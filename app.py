import json
import random
import re
from datetime import datetime
from io import StringIO

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="AI Council | Intelligence Lab", page_icon="◈", layout="wide", initial_sidebar_state="expanded")

# ----------------------------- Design system -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--bg:#080b14;--panel:rgba(18,24,42,.74);--line:rgba(150,170,255,.16);--text:#f4f6ff;--muted:#8e9ab7;--cyan:#63f4e8;--violet:#a78bfa;--pink:#fb79b7;--lime:#b8f36b}
html,body,[class*="css"]{font-family:'Manrope',sans-serif;color:var(--text)}
.stApp{background:radial-gradient(ellipse at 8% 0%,rgba(90,70,220,.18),transparent 34%),radial-gradient(ellipse at 90% 15%,rgba(37,221,214,.10),transparent 32%),linear-gradient(145deg,#080b14 0%,#0b1020 48%,#080b14 100%);background-attachment:fixed}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;opacity:.16;background-image:linear-gradient(rgba(130,150,220,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(130,150,220,.09) 1px,transparent 1px);background-size:48px 48px;mask-image:linear-gradient(to bottom,black,transparent 82%)}
.block-container{padding-top:1.7rem;max-width:1440px;position:relative;z-index:1}
[data-testid="stSidebar"]{background:rgba(9,13,25,.94);border-right:1px solid var(--line)}
[data-testid="stSidebar"] *{color:var(--text)}
h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;letter-spacing:-.035em}
h1{font-size:clamp(2.4rem,4.5vw,4.2rem)!important;line-height:1.02!important}
p{color:#b7c1d9}
.eyebrow{font:500 11px 'DM Mono',monospace;letter-spacing:.2em;text-transform:uppercase;color:var(--cyan)}
.hero-title{font-family:'Space Grotesk',sans-serif;font-size:clamp(42px,6vw,78px);line-height:.99;letter-spacing:-.065em;font-weight:700;margin:.65rem 0 1rem}
.gradient-text{background:linear-gradient(100deg,#f7f8ff 5%,#9f9bff 45%,#63f4e8 90%);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero-copy{font-size:16px;max-width:650px;color:#9da9c4;line-height:1.8}
.orbit-wrap{height:245px;display:flex;align-items:center;justify-content:center;perspective:900px;overflow:hidden}
.core{width:172px;height:172px;border-radius:38px;display:flex;align-items:center;justify-content:center;position:relative;transform:rotateX(16deg) rotateY(-18deg);background:linear-gradient(145deg,rgba(116,107,255,.28),rgba(39,234,224,.08));border:1px solid rgba(150,170,255,.48);box-shadow:0 0 60px rgba(104,94,255,.22),inset 0 0 35px rgba(104,244,232,.1);animation:float 5s ease-in-out infinite;transform-style:preserve-3d}
.core:before,.core:after{content:"";position:absolute;inset:-22px;border:1px solid rgba(99,244,232,.35);border-radius:45px;transform:translateZ(-20px) rotate(24deg);animation:orbit 13s linear infinite}
.core:after{inset:-39px;border-color:rgba(167,139,250,.28);transform:translateZ(-35px) rotate(-25deg);animation-direction:reverse;animation-duration:18s}
.core-glyph{font-size:62px;font-family:'Space Grotesk',sans-serif;color:#e6fffd;text-shadow:0 0 25px rgba(99,244,232,.6)}
@keyframes float{0%,100%{transform:translateY(0) rotateX(16deg) rotateY(-18deg)}50%{transform:translateY(-12px) rotateX(21deg) rotateY(-8deg)}}
@keyframes orbit{to{rotate:360deg}}
.glass{background:linear-gradient(145deg,rgba(22,29,50,.82),rgba(12,17,31,.72));border:1px solid var(--line);border-radius:22px;padding:22px;box-shadow:0 20px 55px rgba(0,0,0,.16);backdrop-filter:blur(18px);transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease}
.glass:hover{transform:translateY(-4px);border-color:rgba(99,244,232,.4);box-shadow:0 24px 65px rgba(0,0,0,.24),0 0 30px rgba(99,244,232,.05)}
.agent-card{min-height:220px;position:relative;overflow:hidden}
.agent-card:after{content:"";position:absolute;width:140px;height:140px;right:-50px;top:-55px;border-radius:50%;background:var(--glow);filter:blur(42px);opacity:.22;pointer-events:none}
.agent-icon{font-size:28px;margin-bottom:15px}
.agent-name{font-family:'Space Grotesk',sans-serif;font-size:21px;font-weight:700;margin-bottom:5px}
.agent-role{font:11px 'DM Mono',monospace;letter-spacing:.13em;text-transform:uppercase;color:var(--agent)}
.agent-copy{font-size:13px;line-height:1.65;color:#9ba8c5;margin-top:12px}
.metric{font:700 31px 'Space Grotesk',sans-serif;color:#f4f6ff}
.metric-label{font:10px 'DM Mono',monospace;letter-spacing:.13em;text-transform:uppercase;color:#8492b1}
.section-kicker{font:11px 'DM Mono',monospace;color:var(--cyan);letter-spacing:.16em;text-transform:uppercase;margin-bottom:8px}
.section-title{font:700 27px 'Space Grotesk',sans-serif;letter-spacing:-.04em;margin-bottom:8px}
.pill{display:inline-block;border:1px solid rgba(99,244,232,.3);border-radius:100px;padding:6px 10px;color:var(--cyan);font:10px 'DM Mono',monospace;letter-spacing:.1em;text-transform:uppercase;background:rgba(99,244,232,.05)}
.debate-line{border-left:2px solid var(--accent);padding:4px 0 4px 16px;margin:16px 0}
.debate-label{font:10px 'DM Mono',monospace;letter-spacing:.12em;color:var(--accent);text-transform:uppercase;margin-bottom:6px}
.debate-text{font-size:14px;color:#c5cde0;line-height:1.75}
.stButton>button{border:1px solid rgba(99,244,232,.45);border-radius:12px;background:linear-gradient(110deg,rgba(99,244,232,.15),rgba(167,139,250,.2));color:#f4ffff;font-family:'Manrope',sans-serif;font-weight:700;min-height:46px;transition:all .2s ease}
.stButton>button:hover{border-color:var(--cyan);box-shadow:0 0 25px rgba(99,244,232,.16);transform:translateY(-2px);color:white}
.stTextInput input,.stTextArea textarea,.stSelectbox div[data-baseweb="select"],.stNumberInput input{background:rgba(10,15,28,.9)!important;border-color:rgba(150,170,255,.2)!important;border-radius:12px!important}
.stProgress>div>div{background:linear-gradient(90deg,var(--violet),var(--cyan))}
hr{border-color:var(--line)}
[data-testid="stMetric"]{background:rgba(17,23,41,.7);border:1px solid var(--line);padding:17px 18px;border-radius:17px}
[data-testid="stMetricLabel"]{color:#8e9ab7}
[data-testid="stMetricValue"]{font-family:'Space Grotesk',sans-serif}
div[data-testid="stExpander"]{border:1px solid var(--line);border-radius:14px;background:rgba(15,20,36,.5)}
footer{visibility:hidden}
@media(max-width:800px){.orbit-wrap{height:180px}.core{width:130px;height:130px}.hero-copy{font-size:14px}.glass{padding:17px}}
</style>
""", unsafe_allow_html=True)

# ----------------------------- Demo intelligence engine -----------------------------
AGENTS = {
    "Research": {"icon":"⌕","color":"#63f4e8","glow":"#63f4e8","role":"Evidence intelligence","desc":"Frames the question, surfaces assumptions, and maps what would count as reliable evidence."},
    "Advocate": {"icon":"↗","color":"#a78bfa","glow":"#a78bfa","role":"Pro position","desc":"Builds the strongest affirmative case, with benefits, examples, and strategic reasoning."},
    "Challenger": {"icon":"⟡","color":"#fb79b7","glow":"#fb79b7","role":"Counter-position","desc":"Stress-tests the proposal, identifies trade-offs, and exposes hidden risks."},
    "Judge": {"icon":"◈","color":"#b8f36b","glow":"#b8f36b","role":"Synthesis & verdict","desc":"Weighs both sides against evidence quality, uncertainty, and the user's stated goal."},
}

TOPIC_PRESETS = {
    "AI in education": "Should colleges make AI tutors a core part of every student's learning experience?",
    "Four-day workweek": "Should knowledge-work companies adopt a four-day workweek by default?",
    "Open-source AI": "Should advanced AI models be open source by default?",
    "Remote-first teams": "Are remote-first teams more effective than office-first teams?",
    "Custom topic": "",
}

def make_debate(topic, rounds, context):
    t = topic.strip().rstrip(".?")
    lower = t.lower()
    if any(k in lower for k in ["education","student","college","tutor","learning"]):
        pro = [
            "Personalized AI support can give each learner immediate explanations, practice, and feedback at their own pace.",
            "Used well, AI tutors can reduce repetitive workload for educators and help them focus on mentoring and higher-order thinking.",
            "Always-available learning support can widen access for students who cannot easily get individual tutoring."
        ]
        con = [
            "Over-reliance can weaken independent reasoning if students accept answers without checking the logic or sources.",
            "Model errors, privacy concerns, and unequal access could widen the very learning gaps the tools aim to close.",
            "Learning outcomes depend on curriculum, teacher practice, and assessment design—not tool adoption alone."
        ]
    elif any(k in lower for k in ["workweek","four-day","4-day","remote","office","work"]):
        pro = [
            "A more intentional work structure can reduce low-value meetings and create longer stretches for focused work.",
            "Flexibility can improve retention and well-being when goals and accountability are clear.",
            "A pilot with measurable output targets allows teams to test the model without committing blindly."
        ]
        con = [
            "Customer coverage, collaboration windows, and operational handoffs may suffer if schedules are compressed without redesign.",
            "Some roles cannot reduce hours without adding workload to colleagues or creating service gaps.",
            "Productivity gains are not automatic; poor management can compress the same stress into fewer days."
        ]
    elif any(k in lower for k in ["open source","open-source","model"]):
        pro = [
            "Open releases can broaden independent research, auditing, customization, and competition.",
            "Developers can adapt models to local languages, specialized tasks, and constraints that a single vendor may not prioritize.",
            "Transparency can support reproducibility when model weights, evaluations, and limitations are documented."
        ]
        con = [
            "Once powerful weights are released, downstream use is harder to monitor or reverse.",
            "Open weights do not automatically provide transparency into training data, evaluation quality, or deployment behavior.",
            "Smaller teams may lack the resources to audit or secure a model after release."
        ]
    else:
        pro = [
            f"The strongest case for the proposal is that it can create a clearer path toward the stated objective: {t}.",
            "A well-designed pilot can turn assumptions into measurable results before a large commitment is made.",
            "The upside may be meaningful when implementation includes clear ownership, transparent metrics, and regular review."
        ]
        con = [
            "The proposal may hide costs, dependencies, or second-order effects that are not visible in the headline benefit.",
            "Results could vary across contexts; a compelling example is not enough to establish a general rule.",
            "Without a baseline and an exit criterion, teams may continue investing even when evidence is weak."
        ]
    pro = (pro * ((rounds + 2)//3))[:rounds]
    con = (con * ((rounds + 2)//3))[:rounds]
    judge = "The most defensible position is conditional rather than absolute: test the proposal against a defined baseline, publish the success criteria, and preserve a practical fallback. The pro case is strongest on potential upside; the con case is strongest on execution risk and uncertainty."
    if context.strip():
        judge += " The user's context should be treated as a constraint for the next iteration, not as independently verified evidence."
    return {"topic":topic,"rounds":[{"round":i+1,"pro":pro[i],"con":con[i],"focus":["Core case","Trade-offs","Implementation test"][i%3]} for i in range(rounds)],"verdict":judge,"confidence":76 if rounds>=3 else 67,"pro_score":78,"con_score":74,"claims":[{"claim":"The proposal can improve outcomes when implemented with clear goals.","status":"Plausible — validate locally","confidence":72},{"claim":"Risks can be reduced through staged rollout and human oversight.","status":"Practical safeguard","confidence":81},{"claim":"Results will generalize across all contexts.","status":"Not established","confidence":31}],"context":context}

def report_markdown(data):
    lines = ["# AI Council — Intelligence Brief", "", f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}", f"**Question:** {data['topic']}", "", "## Executive verdict", data["verdict"], "", f"**Confidence indicator:** {data['confidence']}% (heuristic demo score; not a calibrated probability)", "", "## Debate transcript"]
    for item in data["rounds"]:
        lines += [f"### Round {item['round']} — {item['focus']}", f"**Advocate:** {item['pro']}", f"**Challenger:** {item['con']}", ""]
    lines += ["## Claim review"]
    for claim in data["claims"]:
        lines.append(f"- **{claim['claim']}** — {claim['status']} (heuristic confidence: {claim['confidence']}%)")
    lines += ["", "## Limitations", "This report was generated by the built-in demo engine. It does not perform live web research, verify external sources, or use an LLM. Treat claims as discussion prompts, not verified facts.", ""]
    return "\n".join(lines)

if "debate_result" not in st.session_state:
    st.session_state.debate_result = None
if "runs" not in st.session_state:
    st.session_state.runs = 0

# ----------------------------- Sidebar -----------------------------
with st.sidebar:
    st.markdown("<div style='display:flex;align-items:center;gap:12px;margin:8px 0 30px'><div style='width:42px;height:42px;border:1px solid rgba(99,244,232,.55);border-radius:13px;display:grid;place-items:center;color:#63f4e8;font-size:24px;box-shadow:0 0 25px rgba(99,244,232,.13)'>◈</div><div><div style='font:700 17px Space Grotesk'>AI COUNCIL</div><div style='font:10px DM Mono;color:#8492b1;letter-spacing:.15em'>INTELLIGENCE LAB</div></div></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-kicker'>Workspace</div>", unsafe_allow_html=True)
    page = st.radio("Navigation", ["Overview", "Debate Studio", "Intelligence Report", "Agent Network"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<div class='section-kicker'>System status</div>", unsafe_allow_html=True)
    st.markdown("<div class='glass' style='padding:14px;border-radius:15px'><span style='color:#b8f36b'>●</span> <b>Demo engine online</b><div style='font-size:12px;color:#8997b6;margin-top:7px'>No API key required · Local simulation</div></div>", unsafe_allow_html=True)
    st.markdown("<div style='font:10px DM Mono;color:#667391;margin-top:22px;line-height:1.8'>BUILD 0.1.0<br>HUMAN-LED INTELLIGENCE<br>DESIGNED FOR UNCERTAINTY</div>", unsafe_allow_html=True)

# ----------------------------- Header -----------------------------
st.markdown("<div class='eyebrow'>MULTI-AGENT REASONING SYSTEM <span style='color:#6f7b98'>/ BUILD 0.1</span></div>", unsafe_allow_html=True)

if page == "Overview":
    left, right = st.columns([1.35, .85], gap="large")
    with left:
        st.markdown("<div class='hero-title'>Better questions.<br><span class='gradient-text'>Sharper decisions.</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='hero-copy'>A multi-agent intelligence workspace where perspectives collide, assumptions get stress-tested, and a balanced verdict emerges. Explore the demo—no API keys, no setup, just structured reasoning.</div>", unsafe_allow_html=True)
        st.markdown("<div style='display:flex;gap:9px;flex-wrap:wrap;margin-top:22px'><span class='pill'>4 specialist agents</span><span class='pill'>Multi-round debate</span><span class='pill'>Exportable brief</span></div>", unsafe_allow_html=True)
        st.write("")
        if st.button("✦  Open Debate Studio", use_container_width=False):
            st.session_state.nav_debate = True
            st.session_state.debate_result = st.session_state.debate_result
            st.rerun()
    with right:
        st.markdown("<div class='orbit-wrap'><div class='core'><div class='core-glyph'>◈</div></div></div>", unsafe_allow_html=True)
        st.markdown("<div style='text-align:center;font:10px DM Mono;letter-spacing:.2em;color:#8290b2'>REASONING CORE // ACTIVE</div>", unsafe_allow_html=True)
    st.write("")
    m1,m2,m3,m4=st.columns(4)
    with m1: st.markdown("<div class='glass'><div class='metric'>04</div><div class='metric-label'>Specialist agents</div></div>",unsafe_allow_html=True)
    with m2: st.markdown("<div class='glass'><div class='metric'>03</div><div class='metric-label'>Reasoning rounds</div></div>",unsafe_allow_html=True)
    with m3: st.markdown("<div class='glass'><div class='metric'>360°</div><div class='metric-label'>Perspective coverage</div></div>",unsafe_allow_html=True)
    with m4: st.markdown(f"<div class='glass'><div class='metric'>{st.session_state.runs:02d}</div><div class='metric-label'>Sessions this visit</div></div>",unsafe_allow_html=True)
    st.write("")
    st.markdown("<div class='section-kicker'>The intelligence loop</div><div class='section-title'>One question. Four distinct lenses.</div>",unsafe_allow_html=True)
    cols=st.columns(4,gap="medium")
    for col,(name,info) in zip(cols,AGENTS.items()):
        with col:
            st.markdown(f"<div class='glass agent-card' style='--agent:{info['color']};--glow:{info['glow']}'><div class='agent-icon' style='color:{info['color']}'>{info['icon']}</div><div class='agent-name'>{name}</div><div class='agent-role'>{info['role']}</div><div class='agent-copy'>{info['desc']}</div></div>",unsafe_allow_html=True)
    st.write("")
    st.markdown("<div class='glass'><div class='section-kicker'>Designed for clarity, not false certainty</div><div class='section-title'>Debate is a tool. Evidence is the standard.</div><p style='margin-bottom:0'>The included demo illustrates the workflow using transparent, rule-based sample arguments. It does not claim to verify facts or conduct live research. Add an LLM and trusted retrieval sources when you are ready for production-grade analysis.</p></div>",unsafe_allow_html=True)

elif page == "Debate Studio":
    st.markdown("<div class='section-kicker'>Interactive workspace / 01</div><div class='section-title'>Set the question. Convene the council.</div>",unsafe_allow_html=True)
    a,b=st.columns([1.2,.8],gap="large")
    with a:
        preset=st.selectbox("Start from a topic",list(TOPIC_PRESETS.keys()))
        default=TOPIC_PRESETS[preset]
        topic=st.text_area("Debate question",value=default,height=100,placeholder="What decision are you trying to make?")
        context=st.text_area("Optional context or constraints",height=85,placeholder="Audience, budget, goals, constraints…")
    with b:
        st.markdown("<div class='glass' style='height:100%'><div class='section-kicker'>Debate configuration</div>",unsafe_allow_html=True)
        rounds=st.slider("Rounds of argument",1,3,3)
        st.markdown("<div style='margin-top:16px;color:#9aa7c3;font-size:13px;line-height:1.7'>Each round pairs an affirmative argument with a skeptical counterargument. The final judge synthesizes trade-offs and suggests a practical next step.</div><hr><div style='font:10px DM Mono;color:#63f4e8;letter-spacing:.12em'>MODE: SIMULATED / NO API</div></div>",unsafe_allow_html=True)
    if st.button("◈  Convene AI Council",use_container_width=True):
        if len(topic.strip())<10:
            st.warning("Add a clear question with at least 10 characters to convene the council.")
        else:
            with st.spinner("Convening agents · mapping arguments · synthesizing verdict…"):
                st.session_state.debate_result=make_debate(topic,rounds,context)
                st.session_state.runs+=1
    data=st.session_state.debate_result
    if data:
        st.write("")
        st.markdown("<div class='section-kicker'>Session output / live simulation</div><div class='section-title'>The room is in session.</div>",unsafe_allow_html=True)
        status=st.progress(100,text="All agents completed · demo simulation")
        c1,c2,c3=st.columns(3)
        with c1: st.metric("Rounds completed",len(data["rounds"]))
        with c2: st.metric("Advocate score",f"{data['pro_score']}/100")
        with c3: st.metric("Challenger score",f"{data['con_score']}/100")
        for item in data["rounds"]:
            with st.expander(f"ROUND {item['round']:02d}  /  {item['focus'].upper()}",expanded=True):
                st.markdown(f"<div class='debate-line' style='--accent:#a78bfa'><div class='debate-label'>↗ Advocate · supporting case</div><div class='debate-text'>{item['pro']}</div></div><div class='debate-line' style='--accent:#fb79b7'><div class='debate-label'>⟡ Challenger · countercase</div><div class='debate-text'>{item['con']}</div></div>",unsafe_allow_html=True)
        st.markdown(f"<div class='glass' style='border-color:rgba(184,243,107,.3)'><div class='section-kicker' style='color:#b8f36b'>◈ Judge's synthesis</div><div class='section-title'>A balanced verdict</div><p style='font-size:15px;line-height:1.85'>{data['verdict']}</p><div class='pill'>Heuristic confidence indicator: {data['confidence']}%</div><p style='font-size:11px;margin-top:12px'>This score is a demo heuristic, not a calibrated probability or verified assessment.</p></div>",unsafe_allow_html=True)
        st.markdown("#### Claim review")
        st.dataframe(pd.DataFrame(data["claims"]),use_container_width=True,hide_index=True)
        st.download_button("↓  Export intelligence brief (.md)",report_markdown(data),file_name="ai_council_brief.md",mime="text/markdown")

elif page == "Intelligence Report":
    st.markdown("<div class='section-kicker'>Decision support / 02</div><div class='section-title'>Intelligence report</div>",unsafe_allow_html=True)
    data=st.session_state.debate_result
    if not data:
        st.markdown("<div class='glass'><div class='section-title'>No session report yet</div><p>Run a debate in Debate Studio. Your verdict, round transcript, and claim review will appear here.</p></div>",unsafe_allow_html=True)
        if st.button("Go to Debate Studio"): st.rerun()
    else:
        st.markdown(f"<div class='glass'><div class='section-kicker'>Current question</div><div class='section-title'>{data['topic']}</div><p>{data['verdict']}</p><span class='pill'>Confidence indicator {data['confidence']}%</span></div>",unsafe_allow_html=True)
        st.write("")
        l,r=st.columns([1,1],gap="large")
        with l:
            fig=go.Figure(go.Bar(x=["Advocate","Challenger"],y=[data["pro_score"],data["con_score"]],marker=dict(color=["#a78bfa","#fb79b7"]),text=[data["pro_score"],data["con_score"]],textposition="outside"))
            fig.update_layout(title="Argument strength (illustrative)",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#c5cde0",height=320,margin=dict(l=20,r=20,t=55,b=20),yaxis=dict(range=[0,100],gridcolor="rgba(150,170,255,.12)",title="Heuristic score"),xaxis=dict(showgrid=False))
            st.plotly_chart(fig,use_container_width=True)
        with r:
            claims=pd.DataFrame(data["claims"])
            fig2=go.Figure(go.Bar(y=claims["claim"],x=claims["confidence"],orientation="h",marker_color=["#63f4e8","#b8f36b","#fb79b7"],text=claims["confidence"].astype(str)+"%",textposition="outside"))
            fig2.update_layout(title="Claim review signals (illustrative)",paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#c5cde0",height=320,margin=dict(l=20,r=30,t=55,b=20),xaxis=dict(range=[0,110],gridcolor="rgba(150,170,255,.12)",title="Heuristic confidence"),yaxis=dict(showgrid=False,automargin=True))
            st.plotly_chart(fig2,use_container_width=True)
        st.markdown("#### Unresolved questions")
        st.markdown("- What independent evidence would change the verdict?\n- Which assumptions are most sensitive to local context?\n- What is the smallest safe experiment that can test the claim?")
        st.download_button("↓  Download full report",report_markdown(data),file_name="ai_council_intelligence_report.md",mime="text/markdown")

elif page == "Agent Network":
    st.markdown("<div class='section-kicker'>System architecture / 03</div><div class='section-title'>The council, under the hood.</div>",unsafe_allow_html=True)
    st.markdown("<p>Each role has a bounded responsibility. The current build uses deterministic demo logic; the architecture is designed to support real model calls later.</p>",unsafe_allow_html=True)
    cols=st.columns(2,gap="large")
    for i,(name,info) in enumerate(AGENTS.items()):
        with cols[i%2]:
            st.markdown(f"<div class='glass agent-card' style='--agent:{info['color']};--glow:{info['glow']};margin-bottom:18px'><div style='display:flex;align-items:center;gap:14px'><div style='font-size:34px;color:{info['color']}'>{info['icon']}</div><div><div class='agent-name'>{name}</div><div class='agent-role'>{info['role']}</div></div></div><div class='agent-copy' style='font-size:14px'>{info['desc']}</div><div style='border-top:1px solid rgba(150,170,255,.13);margin-top:18px;padding-top:12px;font:10px DM Mono;color:#8290b2'>INPUT → REASON → STRUCTURED OUTPUT</div></div>",unsafe_allow_html=True)
    st.markdown("<div class='glass'><div class='section-kicker'>Planned production path</div><div class='section-title'>From simulation to grounded intelligence</div><ol style='color:#aab6d0;line-height:2'><li>Connect an LLM provider through environment secrets (optional).</li><li>Add retrieval from trusted sources and keep source URLs with every factual claim.</li><li>Use LangGraph for typed state, retries, and explicit agent handoffs.</li><li>Evaluate outputs against curated test questions; log uncertainty and failures.</li></ol></div>",unsafe_allow_html=True)

st.markdown("<div style='margin-top:44px;padding:20px 0;border-top:1px solid rgba(150,170,255,.13);display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;color:#667391;font:10px DM Mono;letter-spacing:.08em'><span>AI COUNCIL · INTELLIGENCE LAB</span><span>DEMO MODE · NO LIVE FACT-CHECKING</span><span>BUILT FOR BETTER QUESTIONS</span></div>",unsafe_allow_html=True)
