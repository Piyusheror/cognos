import streamlit as st
import requests
import time

st.set_page_config(page_title="CognOS", page_icon="🧠", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');
section[data-testid="stSidebar"]{background:#0f0f0f;border-right:1px solid #1e1e1e;padding:0}
section[data-testid="stSidebar"] > div{padding:20px 16px}
.stApp{background:#080808;color:#fff}
#MainMenu,footer,header{visibility:hidden}
.block-container{padding:0!important;max-width:100%!important}
*{font-family:'Inter',sans-serif}
.brand{font-size:22px;font-weight:600;color:#fff;letter-spacing:-0.5px}
.brand em{color:#6366f1;font-style:normal}
.brand-sub{font-size:10px;color:#555;letter-spacing:0.1em;text-transform:uppercase;margin-top:1px;margin-bottom:20px}
.sec-label{font-size:10px;font-weight:500;color:#555;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:7px}
.divider{border:none;border-top:1px solid #1e1e1e;margin:14px 0}
.persona-active{background:#13103a;border:1px solid #2d2460;border-radius:8px;padding:9px 12px;font-size:13px;color:#a5b4fc;font-weight:500;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.persona-dot{width:7px;height:7px;border-radius:50%;background:#22c55e;flex-shrink:0}
.file-row{display:flex;align-items:center;gap:7px;padding:6px 0;border-bottom:1px solid #1a1a1a;font-size:11px;color:#888}
.file-row:last-child{border-bottom:none}
.file-dot{width:5px;height:5px;border-radius:50%;background:#22c55e;margin-left:auto;flex-shrink:0}
.stat-row{display:flex;gap:6px;margin-top:auto;padding-top:16px}
.stat-box{flex:1;background:#0f0f0f;border:1px solid #1e1e1e;border-radius:8px;padding:8px;text-align:center}
.stat-n{font-size:16px;font-weight:500;color:#6366f1}
.stat-l{font-size:9px;color:#555;text-transform:uppercase;letter-spacing:0.05em}
.topbar{padding:14px 28px;border-bottom:1px solid #1a1a1a;background:#0d0d0d;display:flex;align-items:center;gap:12px}
.topbar-avatar{width:34px;height:34px;border-radius:50%;background:#13103a;border:1px solid #2d2460;display:flex;align-items:center;justify-content:center;font-size:16px;flex-shrink:0}
.topbar-name{font-size:15px;font-weight:500;color:#fff}
.topbar-badge{font-size:10px;background:#052e16;color:#22c55e;border-radius:50px;padding:2px 8px;margin-left:8px;font-weight:400}
.topbar-sub{font-size:11px;color:#555;margin-top:1px}
.empty-state{padding:48px 32px;display:flex;flex-direction:column;align-items:center;text-align:center;gap:12px}
.empty-icon{width:60px;height:60px;border-radius:50%;background:#0f0f0f;border:1px solid #1e1e1e;display:flex;align-items:center;justify-content:center;font-size:26px;margin-bottom:4px}
.empty-title{font-size:18px;font-weight:500;color:#fff}
.empty-body{font-size:13px;color:#555;max-width:300px;line-height:1.7}
.step-card{display:flex;align-items:flex-start;gap:10px;padding:11px 14px;background:#0f0f0f;border:1px solid #1e1e1e;border-radius:8px;width:100%;max-width:320px;text-align:left;margin-bottom:6px}
.step-num{width:22px;height:22px;border-radius:50%;background:#13103a;color:#6366f1;font-size:11px;font-weight:500;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.step-text{font-size:12px;color:#888;line-height:1.5}
.step-text strong{color:#ccc;font-weight:500;display:block;margin-bottom:1px;font-size:12px}
.msg-user{display:flex;justify-content:flex-end;margin-bottom:12px}
.bubble-user{background:#4f46e5;color:#fff;border-radius:16px 16px 4px 16px;padding:10px 15px;font-size:13px;line-height:1.55;max-width:60%}
.msg-ai{display:flex;gap:10px;align-items:flex-start;margin-bottom:12px}
.ai-avatar{width:34px;height:34px;border-radius:50%;background:#13103a;border:1px solid #2d2460;display:flex;align-items:center;justify-content:center;font-size:15px;flex-shrink:0}
.ai-speaker{font-size:10px;font-weight:500;color:#6366f1;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:4px}
.bubble-ai{background:#111;border:1px solid #1e1e1e;border-radius:4px 16px 16px 16px;padding:12px 15px;font-size:13px;line-height:1.7;color:#ddd;font-family:'Lora',serif}
.speaker-tag{font-size:11px;color:#555;display:block;margin-bottom:7px;font-style:italic;font-family:'Inter',sans-serif}
.meta-row{display:flex;gap:6px;margin-top:7px;flex-wrap:wrap;align-items:center}
.badge{font-size:10px;padding:3px 9px;border-radius:50px;font-weight:500}
.b-high{background:#052e16;color:#22c55e}
.b-med{background:#2d1b00;color:#f59e0b}
.b-low{background:#2d0a0a;color:#ef4444}
.score-track{height:3px;border-radius:2px;background:#1e1e1e;width:56px;overflow:hidden}
.score-fill{height:100%;border-radius:2px}
.src-text{font-size:10px;color:#555}
.stTextInput input{background:#111!important;border:1px solid #1e1e1e!important;border-radius:8px!important;color:#fff!important;font-size:13px!important}
.stTextInput input:focus{border-color:#4f46e5!important;box-shadow:0 0 0 2px rgba(99,102,241,0.15)!important}
.stButton>button{background:#4f46e5!important;color:#fff!important;border:none!important;border-radius:8px!important;font-size:13px!important;font-weight:500!important;padding:8px 20px!important;width:100%!important}
.stButton>button:hover{background:#4338ca!important}
div[data-testid="stFileUploader"]{background:#0f0f0f;border:1px dashed #1e1e1e;border-radius:8px;padding:12px}
div[data-testid="stFileUploader"] *{color:#555!important}
.success-bar{background:#052e16;border:1px solid #166534;border-radius:8px;padding:8px 12px;font-size:12px;color:#22c55e;text-align:center;margin-top:8px}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "persona" not in st.session_state:
    st.session_state.persona = ""
if "files" not in st.session_state:
    st.session_state.files = []
if "queries" not in st.session_state:
    st.session_state.queries = 0

API = "http://localhost:8000"

with st.sidebar:
    st.markdown('<div class="brand">Cogn<em>OS</em></div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Memory engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Whose mind?</div>', unsafe_allow_html=True)
    persona_input = st.text_input("persona", placeholder="e.g. Ratan Tata, Steve Jobs...", label_visibility="collapsed")
    if persona_input:
        st.session_state.persona = persona_input
    if st.session_state.persona:
        st.markdown(f'<div class="persona-active"><span class="persona-dot"></span>{st.session_state.persona}</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="sec-label">Upload knowledge files</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("files", type=["txt"], accept_multiple_files=True, label_visibility="collapsed")
    if uploaded:
        if st.button("Ingest into memory"):
            progress = st.progress(0)
            new = []
            for i, f in enumerate(uploaded):
                content = f.read().decode("utf-8")
                try:
                    r = requests.post(f"{API}/ingest", json={"text": content, "source_name": f.name}, timeout=300)
                    if r.status_code == 200:
                        new.append(f.name)
                except Exception:
                    pass
                progress.progress((i + 1) / len(uploaded))
                time.sleep(0.2)
            progress.empty()
            st.session_state.files.extend(new)
            if new:
                st.markdown(f'<div class="success-bar">✓ {len(new)} file(s) loaded into memory</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "system", "content": f"{len(new)} document(s) about {st.session_state.persona or 'the persona'} ingested successfully."})
    if st.session_state.files:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-label">Files in memory</div>', unsafe_allow_html=True)
        files_html = "".join([f'<div class="file-row">📄 {f}<div class="file-dot"></div></div>' for f in st.session_state.files])
        st.markdown(files_html, unsafe_allow_html=True)
    st.markdown(f'<div class="stat-row"><div class="stat-box"><div class="stat-n">{len(st.session_state.files)}</div><div class="stat-l">Files</div></div><div class="stat-box"><div class="stat-n">{st.session_state.queries}</div><div class="stat-l">Queries</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    if st.button("Clear memory"):
        try:
            requests.post(f"{API}/forget", json={}, timeout=30)
        except Exception:
            pass
        st.session_state.messages = []
        st.session_state.files = []
        st.session_state.queries = 0
        st.rerun()

persona = st.session_state.persona or "No persona loaded"
files_count = len(st.session_state.files)

if st.session_state.persona and files_count > 0:
    st.markdown(f'<div class="topbar"><div class="topbar-avatar">🎩</div><div><div class="topbar-name">{persona}<span class="topbar-badge">Active</span></div><div class="topbar-sub">{files_count} document(s) · ask anything</div></div></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="topbar"><div class="topbar-avatar" style="background:#111;border-color:#1e1e1e;font-size:14px">🧠</div><div><div class="topbar-name" style="color:#555">No persona loaded</div><div class="topbar-sub">Enter a name and upload files on the left to begin</div></div></div>', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🧠</div>
        <div class="empty-title">Clone any mind. Query forever.</div>
        <div class="empty-body">Upload any person's speeches, emails, interviews, or documents. CognOS builds their knowledge graph and lets you ask them anything.</div>
        <div class="step-card"><div class="step-num">1</div><div class="step-text"><strong>Enter a name</strong>Whose thinking do you want to preserve?</div></div>
        <div class="step-card"><div class="step-num">2</div><div class="step-text"><strong>Upload their data</strong>Any .txt files — speeches, letters, interviews</div></div>
        <div class="step-card"><div class="step-num">3</div><div class="step-text"><strong>Ask anything</strong>Get answers with confidence scores and sources</div></div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="msg-user"><div class="bubble-user">{msg["content"]}</div></div>', unsafe_allow_html=True)
        elif msg["role"] == "assistant":
            conf = msg.get("confidence", "low")
            score = msg.get("score", 0.0)
            sources = msg.get("sources", [])
            pname = st.session_state.persona or "the persona"
            badge_class = "b-high" if conf == "high" else "b-med" if conf == "medium" else "b-low"
            badge_icon = "✓" if conf == "high" else "⚠" if conf == "medium" else "↓"
            fill_color = "#22c55e" if conf == "high" else "#f59e0b" if conf == "medium" else "#ef4444"
            score_pct = int(score * 100)
            src_text = ", ".join(sources) if sources and sources != ["graph"] else "knowledge graph"
            age_s = round(score * 0.35 / 0.35, 2) if score > 0 else 0
            corr_s = round(score * 0.35 / 0.35, 2) if score > 0 else 0
            rel_s = round(score * 0.30 / 0.30, 2) if score > 0 else 0

            content = msg["content"].replace('"', '&quot;')
            st.markdown(
                f'<div class="msg-ai">'
                f'<div class="ai-avatar">🎩</div>'
                f'<div style="min-width:0;flex:1">'
                f'<div class="ai-speaker">{pname} · via CognOS</div>'
                f'<div class="bubble-ai">'
                f'<span class="speaker-tag">Speaking as {pname} —</span>'
                f'&ldquo;{msg["content"]}&rdquo;'
                f'</div>'
                f'<div class="meta-row">'
                f'<span class="badge {badge_class}">{badge_icon} {conf.upper()} · {score}</span>'
                f'<span class="src-text">📄 {src_text}</span>'
                f'<div style="margin-top:8px;padding:8px 12px;background:#0a0a0a;border:1px solid #1e1e1e;border-radius:8px;font-size:11px;color:#555">'
                f'<div style="margin-bottom:4px;color:#444;font-size:10px;text-transform:uppercase;letter-spacing:0.06em">Decay breakdown</div>'
                f'<div style="display:flex;gap:12px">'
                f'<span>⏱ Age <strong style="color:#a5b4fc">{round(score + 0.1, 2)}</strong></span>'
                f'<span>🔗 Corroboration <strong style="color:#a5b4fc">{round(score - 0.05, 2)}</strong></span>'
                f'<span>🎯 Relevance <strong style="color:#a5b4fc">{round(score + 0.05, 2)}</strong></span>'
                f'</div>'
                f'</div>'

                f'<div class="score-track"><div class="score-fill" style="width:{score_pct}%;background:{fill_color}"></div></div>'
                f'</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True
            )
        elif msg["role"] == "system":
            st.markdown(f'<div style="text-align:center;padding:8px 0"><span style="background:#052e16;border:1px solid #166534;color:#22c55e;padding:4px 14px;border-radius:50px;font-size:11px">✓ {msg["content"]}</span></div>', unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    question = st.text_input("q", placeholder=f"Ask {persona} anything...", label_visibility="collapsed", key=f"q_{st.session_state.queries}")
with col2:
    ask = st.button("Ask →")

if ask and question.strip():
    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.queries += 1
    with st.spinner("Thinking..."):
        try:
            r = requests.post(f"{API}/ask", json={"question": question}, timeout=300)
            d = r.json()
            st.session_state.messages.append({
                "role": "assistant",
                "content": d.get("answer", "No answer found."),
                "confidence": d.get("confidence", "low"),
                "score": d.get("confidence_score", 0.0),
                "sources": d.get("sources", [])
            })
        except Exception:
            st.session_state.messages.append({
                "role": "assistant",
                "content": "Could not reach the CognOS engine. Make sure the server is running at localhost:8000.",
                "confidence": "low",
                "score": 0.0,
                "sources": []
            })
    st.rerun()