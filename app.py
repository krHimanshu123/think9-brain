from pathlib import Path
import os
import streamlit as st
from dotenv import load_dotenv

from src.data_loader import load_documents, extract_upload, BRAND_LABELS
from src.retrieval import retrieve
from src.intelligence import analyze
from src.actions import seed_actions, create_action

load_dotenv()
ROOT = Path(__file__).parent
st.set_page_config(page_title="Think9 Brain", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --bg:#080b17; --surface:#11162a; --line:rgba(145,157,255,.16); --muted:#9da6c7; --accent:#8c7cff; --cyan:#55d8ff; }
.stApp { background:radial-gradient(circle at 80% -10%,#25204e 0,transparent 34%),radial-gradient(circle at 0% 20%,#10253c 0,transparent 28%),var(--bg); color:#f2f4ff; font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:rgba(8,11,23,.96) !important; }
[data-testid="stToolbar"] { background:transparent !important; }
[data-testid="stSidebar"] * { color:#e7ebff; }
[data-testid="stSidebar"] .meta,[data-testid="stSidebar"] .small-note { color:#9da6c7 !important; }
[data-testid="stSidebar"] { background:rgba(8,11,23,.94); border-right:1px solid var(--line); }
h1,h2,h3,h4 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-.03em; }
.block-container { padding:2.5rem 4rem 4rem; max-width:1500px; }
.eyebrow { color:var(--cyan); font-size:.72rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; }
.hero { padding:1.8rem 2.5rem; border:1px solid var(--line); border-radius:24px; background:linear-gradient(120deg,rgba(25,34,68,.92),rgba(20,16,47,.75)); box-shadow:0 22px 70px rgba(0,0,0,.25); margin-bottom:1.25rem; }
.hero h1 { font-size:3.2rem; margin:.25rem 0 .2rem; }.hero p { color:#b5bddb; font-size:1.07rem; max-width:680px; margin:0; }
.online { display:inline-flex; gap:.5rem; align-items:center; color:#bfffe1; background:rgba(62,211,139,.09); border:1px solid rgba(62,211,139,.27); padding:.42rem .75rem; border-radius:99px; font-size:.78rem; margin-top:1.2rem; }.dot { width:7px;height:7px;background:#44db91;border-radius:50%;box-shadow:0 0 12px #44db91; }
.metric,.card,.evidence,.signal,.timeline { background:rgba(17,22,42,.82); border:1px solid var(--line); border-radius:16px; padding:1.2rem; transition:transform .2s,border .2s; }.metric:hover,.card:hover,.evidence:hover,.signal:hover { transform:translateY(-2px); border-color:rgba(140,124,255,.5); }
.metric-label,.meta { color:var(--muted); font-size:.78rem; }.metric-value { font-family:'Space Grotesk'; font-size:1.6rem; font-weight:700; margin-top:.4rem; }.section-head { display:flex;justify-content:space-between;align-items:end;margin:2.1rem 0 .9rem; }.section-head h2 { margin:0;font-size:1.35rem; }.badge { display:inline-block;padding:.28rem .58rem;border-radius:99px;color:#cdd5ff;background:rgba(140,124,255,.13);border:1px solid rgba(140,124,255,.25);font-size:.72rem; }.badge.green { color:#adf5d0;background:rgba(62,211,139,.1);border-color:rgba(62,211,139,.25); }
.evidence { min-height:175px; }.evidence h4 { margin:.6rem 0;font-size:1.08rem; }.quote { color:#d9def3;line-height:1.55;font-size:.91rem; }.signal strong { display:block;margin:.55rem 0 .25rem; }.signal p { color:var(--muted);font-size:.8rem;margin:0; }.arch-step { text-align:center;padding:1.4rem;border-radius:18px;border:1px solid var(--line);background:linear-gradient(135deg,rgba(22,29,57,.9),rgba(14,18,36,.9));margin:.7rem auto;max-width:850px; }.arch-step h3 { margin:.25rem 0;color:#fff; }.arch-step p { color:var(--muted);margin:0; }.arrow { text-align:center;color:var(--accent);font-size:1.4rem; }.small-note { color:#7e88aa;font-size:.74rem; }.prototype-label { color:#7e88aa;font-size:.72rem;letter-spacing:.04em;margin:.25rem 0 .65rem; }.reason-line { color:#cbd3ef;border-left:2px solid var(--cyan);padding:.45rem .8rem;margin-top:.8rem;font-size:.9rem; }.success-card { border:1px solid rgba(62,211,139,.35);background:rgba(35,102,76,.2);border-radius:16px;padding:1rem 1.2rem; }
div[data-testid="stButton"] button { border-radius:10px;border:1px solid rgba(140,124,255,.35);background:rgba(140,124,255,.1);color:#eef0ff;transition:all .2s ease; } div[data-testid="stButton"] button:hover { border-color:var(--cyan);color:#fff;background:linear-gradient(135deg,rgba(67,106,220,.38),rgba(140,124,255,.32));box-shadow:0 0 18px rgba(85,216,255,.12); }
/* Keep native Streamlit controls readable when the Cloud browser preference is Light. */
textarea, input, [data-baseweb="select"] > div, [data-baseweb="input"] > div, [data-testid="stDateInput"] input { background:#11162a !important; color:#f2f4ff !important; border-color:rgba(145,157,255,.35) !important; -webkit-text-fill-color:#f2f4ff !important; }
textarea::placeholder, input::placeholder { color:#8f99bd !important; -webkit-text-fill-color:#8f99bd !important; }
[data-baseweb="select"] *, [data-baseweb="input"] * { color:#f2f4ff !important; }
[role="listbox"], [role="option"] { background:#11162a !important; color:#f2f4ff !important; }
[role="option"]:hover { background:#243b80 !important; }
div[data-testid="stTextArea"] label, div[data-testid="stTextInput"] label, div[data-testid="stSelectbox"] label, div[data-testid="stFileUploader"] label { color:#cbd3ef !important; }
/* Streamlit Cloud uploader: keep the complete dropzone dark in Light/System browser themes. */
div[data-testid="stFileUploader"] section { background:#11162a !important; border:1px solid rgba(145,157,255,.35) !important; border-radius:12px !important; }
div[data-testid="stFileUploader"] section > div { color:#cbd3ef !important; }
div[data-testid="stFileUploader"] section small, div[data-testid="stFileUploader"] section span { color:#9da6c7 !important; }
div[data-testid="stFileUploader"] button { background:#1b2650 !important; color:#f2f4ff !important; border:1px solid #6674f4 !important; }
div[data-testid="stFileUploader"] button:hover { background:#243b80 !important; border-color:#62d8ff !important; }
div[data-testid="stFileUploader"] svg { fill:#8fa2ff !important; color:#8fa2ff !important; }
/* Scoped selected query styling; overrides Streamlit primary/focus tokens and inner label text. */
div[data-testid="stButton"] button:focus,div[data-testid="stButton"] button:active,div[data-testid="stButton"] button[aria-pressed="true"] { color:#f8faff !important;background:linear-gradient(135deg,#243B80,#443B83) !important;border:1px solid #6674F4 !important;box-shadow:0 0 18px rgba(102,116,244,.16) !important;outline:none !important; }
div[data-testid="stButton"] button:focus:hover,div[data-testid="stButton"] button:active:hover,div[data-testid="stButton"] button[aria-pressed="true"]:hover { color:#fff !important;background:linear-gradient(135deg,#2d4b98,#514899) !important;border-color:#62D8FF !important; }
div[data-testid="stButton"] button:focus > *,div[data-testid="stButton"] button:active > *,div[data-testid="stButton"] button[aria-pressed="true"] > * { color:#f8faff !important; }
</style>""", unsafe_allow_html=True)

def init():
    if "documents" not in st.session_state: st.session_state.documents=load_documents(ROOT/"data")
    if "actions" not in st.session_state: st.session_state.actions=seed_actions()
    if "result" not in st.session_state: st.session_state.result=None
    if "query" not in st.session_state: st.session_state.query="Should Brand Gamma introduce trial-size products?"
    if "upload_notice" not in st.session_state: st.session_state.upload_notice=None

def card_metric(label,value,sub=""): st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="small-note">{sub}</div></div>',unsafe_allow_html=True)

def sidebar():
    with st.sidebar:
        st.markdown('<div class="eyebrow">THINK9 / INTELLIGENCE</div><h2 style="margin:.25rem 0 0">Think9 Brain</h2><div class="meta">Central Intelligence Layer</div><br>',unsafe_allow_html=True)
        page=st.radio("Navigate",["Intelligence Hub","Knowledge Base","Decision Memory","Action Center","System Architecture","About Prototype"],label_visibility="collapsed")
        st.markdown("<br><div class='meta'>SYSTEM STATUS</div><p style='line-height:2;font-size:.84rem'>🟢 Knowledge Engine · Online<br>🟢 Cross-Brand Memory · Active<br>🟢 Retrieval Engine · Ready</p><hr><div class='small-note'>Think9 AI & Intelligence Challenge<br>Demonstration prototype · v0.1</div>",unsafe_allow_html=True)
    return page

def header():
    mode="LLM Enhanced Mode" if os.getenv("OPENAI_API_KEY") else "Demo Intelligence Mode"
    st.markdown(f'<div class="hero"><div class="eyebrow">THINK9 BRAIN · CROSS-BRAND INTELLIGENCE ENGINE</div><h1>Intelligence that compounds<br>across every brand.</h1><p>Every meeting, experiment, decision and learning becomes reusable intelligence for the entire Think9 portfolio.</p><div class="online"><span class="dot"></span> AI Intelligence Layer Online <span class="badge">{mode}</span></div></div>',unsafe_allow_html=True)
    st.markdown('<div class="prototype-label">Illustrative Portfolio Metrics · Prototype</div>',unsafe_allow_html=True)
    for col,args in zip(st.columns(4),[("Brands Connected","30+","Demonstration portfolio"),("Knowledge Sources","1,248","Indexed organizational memory"),("Decisions Indexed","386","Institutional memory"),("Intelligence Mode","Cross-Brand","Evidence-backed reasoning")]):
        with col: card_metric(*args)

def run_query(query):
    if not query.strip(): st.session_state.result=None; st.warning("Enter a business question to generate intelligence."); return
    with st.spinner("Connecting insights across Think9's brand memory..."): st.session_state.result=analyze(query,retrieve(query,st.session_state.documents))

def hub():
    header(); st.markdown('<div class="section-head"><h2>Ask Think9 Brain</h2><span class="badge">Cross-brand retrieval active</span></div>',unsafe_allow_html=True)
    chips=["Should Brand Gamma introduce trial-size products?","What have we learned about price-sensitive consumers?","Which supply chain risks have appeared across brands?","What packaging strategies have worked previously?"]
    for col,query in zip(st.columns(4),chips):
        with col:
            if st.button(query,key=f"chip-{query}",use_container_width=True): st.session_state.query=query; run_query(query)
    query=st.text_area("Business question",key="query",height=78,label_visibility="collapsed",placeholder="Ask a question across the Think9 portfolio...")
    if st.button("Generate Intelligence  →",type="primary",use_container_width=False): run_query(query)
    if st.session_state.result:
        result=st.session_state.result; unique_brands=len({x["brand"] for x in result["evidence"]}); why="Portfolio evidence indicates that smaller entry packs can reduce first-purchase price friction, but packaging economics must be validated before scaling." if "Gamma" in query else "The recommendation follows the strongest retrieved portfolio evidence and an explicit scale gate."
        st.markdown('<div class="section-head"><h2>Intelligence Response</h2><span class="badge green">Grounded in internal evidence</span></div>',unsafe_allow_html=True)
        st.markdown(f'<div class="card"><div class="eyebrow">EXECUTIVE ANSWER</div><h3>{result["answer"]}</h3><div class="reason-line"><b>Why this recommendation:</b> {why}</div><div class="small-note" style="margin-top:.8rem">Prototype synthesis · {unique_brands} contributing brand perspectives</div></div>',unsafe_allow_html=True)
        st.markdown('<div class="section-head"><h2>Cross-Brand Evidence</h2></div>',unsafe_allow_html=True)
        for col,item in zip(st.columns(min(3,max(1,len(result["evidence"]))),),result["evidence"]):
            with col: st.markdown(f'<div class="evidence"><span class="badge">{item["brand"]}</span><h4>{item["category"]}</h4><div class="quote">{item["quote"]}</div><div class="meta" style="margin-top:1rem">Source · {item["source"]}</div></div>',unsafe_allow_html=True)
        st.markdown('<div class="section-head"><h2>Think9 Brain Synthesis</h2><span class="badge">Portfolio Pattern Detected</span></div>',unsafe_allow_html=True); st.markdown(f'<div class="card"><div class="eyebrow">PORTFOLIO PATTERN DETECTED</div><p style="font-size:1.05rem;line-height:1.6">{result["synthesis"]}</p></div>',unsafe_allow_html=True)
        a=result["action"]; left,right=st.columns([2,1])
        with left: st.markdown(f'<div class="card"><div class="eyebrow">RECOMMENDED ACTION</div><h3>{a["title"]}</h3><p>{a["description"]}</p><ul>{"".join(f"<li>{x}</li>" for x in a["steps"])}</ul><div class="small-note">External Jira / Slack execution is simulated; consequential actions require human approval.</div></div>',unsafe_allow_html=True)
        with right:
            st.markdown(f'<div class="card"><div class="eyebrow">PROTOTYPE CONFIDENCE SCORE</div><div class="metric-value">{result["confidence"]}%</div><div class="small-note">Heuristic score based on retrieval strength and evidence agreement.</div></div>',unsafe_allow_html=True)
            if st.button("Create Action Item",use_container_width=True): st.session_state.show_action=True
        if st.session_state.get("show_action"):
            with st.form("action-form"):
                st.markdown("### Convert Insight into Action"); c1,c2=st.columns(2); title=c1.text_input("Task title",a["title"]); brand=c2.selectbox("Brand",BRAND_LABELS); owner=c1.text_input("Owner",a["owner"]); priority=c2.selectbox("Priority",["High","Medium","Low"],index=0); deadline=c1.date_input("Deadline"); description=st.text_area("Description",a["description"])
                if st.form_submit_button("Confirm Action",type="primary"):
                    st.session_state.actions.insert(0,create_action({"title":title,"brand":brand,"owner":owner,"priority":priority,"deadline":deadline,"description":description})); st.session_state.show_action=False; st.session_state.action_created=st.session_state.actions[0]; st.rerun()
        if st.session_state.get("action_created"):
            x=st.session_state.action_created; st.markdown(f'<div class="success-card"><b>Action Created Successfully</b><br><span class="small-note">{x["id"]} · {x["brand"]} · {x["owner"]} · High Priority · Status: Open</span></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-head"><h2>Portfolio Intelligence Signals</h2></div>',unsafe_allow_html=True)
    for col,title,text in zip(st.columns(4),["Price Sensitivity","Trial-Pack Opportunity","Packaging Cost Risk","Vendor Consolidation"],["Detected across multiple brand sources","Strong cross-brand evidence","Validate economics before scale","Potential cross-brand sourcing leverage"]):
        with col: st.markdown(f'<div class="signal"><span class="eyebrow">SIGNAL</span><strong>{title}</strong><p>{text}</p></div>',unsafe_allow_html=True)

def knowledge():
    header(); st.markdown('<div class="section-head"><h2>Knowledge Base</h2><span class="badge">Session-indexed sources</span></div>',unsafe_allow_html=True); c1,c2,c3=st.columns([1,1,2]); brand=c1.selectbox("Brand",["All brands"]+BRAND_LABELS); category=c2.selectbox("Category",["All categories"]+sorted({d["category"] for d in st.session_state.documents})); search=c3.text_input("Search",placeholder="Search sources..."); docs=[d for d in st.session_state.documents if (brand=="All brands" or d["brand"]==brand) and (category=="All categories" or d["category"]==category) and (not search or search.lower() in (d["name"]+d["text"]).lower())]
    for d in docs: st.markdown(f'<div class="card" style="margin:.6rem 0"><span class="badge">{d["brand"]}</span><h3 style="margin:.5rem 0 .25rem">{d["title"]}</h3><div class="meta">{d["category"]} · {d["date"]} · {d["type"]} · <span class="badge green">Indexed</span></div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-head"><h2>Add knowledge</h2></div>',unsafe_allow_html=True); upload=st.file_uploader("Upload a TXT or PDF document",type=["txt","pdf"])
    if upload:
        c1,c2=st.columns(2); ubrand=c1.selectbox("Brand",BRAND_LABELS,key="upload-brand"); ucat=c2.selectbox("Category",["Consumer Research","Meeting","Growth Experiment","Supply Chain","Product Strategy","SOP / Playbook"],key="upload-category")
        if st.button("Index document",type="primary"):
            try:
                text=extract_upload(upload)
                if not text.strip(): raise ValueError("No readable text found")
                st.session_state.documents.append({"id":upload.name,"name":upload.name,"title":Path(upload.name).stem.replace("_"," ").title(),"brand":ubrand,"category":ucat,"date":"Session upload","type":"Uploaded document","text":text,"indexed":True}); st.session_state.upload_notice=upload.name; st.rerun()
            except Exception as exc: st.error(f"Could not index this document: {exc}")
    if st.session_state.upload_notice: st.success(f"Document successfully indexed into Think9 Brain · {st.session_state.upload_notice}")

def decisions():
    header(); st.markdown('<div class="section-head"><h2>Decision Memory</h2><span class="badge">What → Why → Who → Outcome</span></div>',unsafe_allow_html=True); entries=[{"brand":"Brand Alpha","decision":"Introduce 250 ml trial packs","why":"Reduce purchase friction among price-sensitive consumers.","who":"Product Team","status":"Pilot Approved","type":"Product"},{"brand":"Brand Beta","decision":"Continue trial-pack acquisition experiment","why":"First-time conversion improved by 17%; packaging cost needed control.","who":"Growth Team","status":"Scaling with guardrails","type":"Growth"},{"brand":"Brand Gamma","decision":"Prioritize D2C retention experiment","why":"Repeat purchases were below target despite strong reviews.","who":"Strategy Team","status":"In Progress","type":"Growth"},{"brand":"Brand Alpha","decision":"Retain sustainable packaging specification","why":"Complaint reduction justified the unit-cost increase in the pilot.","who":"Operations Team","status":"Approved","type":"Operations"},{"brand":"Portfolio","decision":"Evaluate shared packaging suppliers","why":"Alpha and Beta have vendor overlap and possible volume leverage.","who":"Procurement","status":"Under Review","type":"Operations"},{"brand":"Brand Gamma","decision":"Pair creator content with product demonstrations","why":"UGC-style creative performed better with concrete use cases.","who":"Growth Team","status":"Completed","type":"Marketing"}]; c1,c2,c3=st.columns(3); fbrand=c1.selectbox("Brand",["All"]+BRAND_LABELS); ftype=c2.selectbox("Decision type",["All"]+sorted({e["type"] for e in entries})); fstatus=c3.selectbox("Status",["All"]+sorted({e["status"] for e in entries}));
    for e in entries:
        if (fbrand!="All" and e["brand"]!=fbrand) or (ftype!="All" and e["type"]!=ftype) or (fstatus!="All" and e["status"]!=fstatus): continue
        st.markdown(f'<div class="timeline" style="margin:.8rem 0"><span class="badge">{e["brand"]}</span> <span class="badge green">{e["status"]}</span><h3>{e["decision"]}</h3><p><b>Why:</b> {e["why"]}</p><div class="meta">Owner · {e["who"]} / Decision type · {e["type"]}</div></div>',unsafe_allow_html=True)

def actions_page():
    header(); st.markdown('<div class="section-head"><h2>Action Center</h2><span class="badge">Human approval required for external actions</span></div>',unsafe_allow_html=True); actions=st.session_state.actions
    for col,label,value in zip(st.columns(4),["Open Actions","High Priority","In Progress","Completed"],[sum(x["status"]=="Open" for x in actions),sum(x["priority"]=="High" for x in actions),sum(x["status"]=="In Progress" for x in actions),sum(x["status"]=="Completed" for x in actions)]):
        with col: card_metric(label,value,"Live prototype queue")
    for i,a in enumerate(actions):
        c1,c2,c3,c4,c5,c6=st.columns([2.4,1.2,1.6,1,1.2,1.4]); c1.markdown(f"**{a['title']}**\n\n<small>{a['id']}</small>",unsafe_allow_html=True); c2.write(a["brand"]); c3.write(a["owner"]); c4.write(a["priority"]); c5.write(a["status"]); new=c6.selectbox("Status",["Open","In Progress","Completed"],index=["Open","In Progress","Completed"].index(a["status"]),key=f"status-{i}")
        if new!=a["status"]: a["status"]=new; st.rerun()
        st.divider()

def architecture():
    header(); st.markdown('<div class="section-head"><h2>System Architecture</h2><span class="badge">Modular agentic flow</span></div>',unsafe_allow_html=True); steps=[("DATA SOURCES","Meetings · Documents · Reports · SOPs · Consumer Research · Product Strategy · Vendor Intelligence"),("INGESTION AGENT","Parsing · Metadata Extraction · Brand Classification"),("CENTRAL KNOWLEDGE LAYER","Organizational Memory · Decision Memory · Cross-Brand Metadata · Retrieval Index"),("RETRIEVAL & REASONING","Evidence Retrieval · Cross-Brand Comparison · Pattern Detection · Recommendation Generation"),("THINK9 INTELLIGENCE COPILOT","Executive Answer · Evidence · Synthesis · Recommendation · Confidence"),("ACTION AGENT","Tasks · Slack · Jira · Email"),("HUMAN APPROVAL","External and consequential actions require confirmation")]
    for i,(title,body) in enumerate(steps): st.markdown(f'<div class="arch-step"><div class="eyebrow">STAGE {i+1}</div><h3>{title}</h3><p>{body}</p></div>{"<div class=arrow>↓</div>" if i<len(steps)-1 else ""}',unsafe_allow_html=True)

def about():
    header(); st.markdown("## Problem"); st.write("Knowledge becomes fragmented as brand count grows."); st.markdown("## Opportunity"); st.write("Every brand should benefit from the experience of the entire Think9 portfolio."); st.markdown("## Solution"); st.write("Think9 Brain turns fragmented organizational knowledge into reusable cross-brand intelligence."); st.markdown("## What This POC Demonstrates"); st.write("Multi-brand ingestion · centralized memory · evidence retrieval · cross-brand reasoning · decision memory · recommendations · action creation · human approval."); st.markdown("## Production Evolution"); st.write("Google Drive, Slack, Microsoft Teams, Notion, Jira, email, meeting transcripts and ERP systems, with RBAC, tenant controls, audit logs, encryption, enterprise identity and observability.")

init(); page=sidebar()
if page=="Intelligence Hub": hub()
elif page=="Knowledge Base": knowledge()
elif page=="Decision Memory": decisions()
elif page=="Action Center": actions_page()
elif page=="System Architecture": architecture()
else: about()
