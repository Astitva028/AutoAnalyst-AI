import os
import streamlit as st
from agent.graph import build_agent, run_agent
from agent.tools import set_dataframe
from utils.file_handler import load_uploaded_file

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AutoAnalyst AI",
    page_icon="🤖",
    layout="wide"
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🤖 AutoAnalyst AI")
st.caption("Autonomous Data Analysis Agent · Powered by Gemini 1.5 Pro + LangGraph")
st.divider()

# ── Session State ─────────────────────────────────────────────────────────────
if "agent" not in st.session_state:
    with st.spinner("⚙️ Initializing agent..."):
        st.session_state.agent = build_agent()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "df_loaded" not in st.session_state:
    st.session_state.df_loaded = False

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("📂 Upload Your Data")
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx", "xls"],
        help="Your data never leaves your session."
    )

    if uploaded_file:
        df = load_uploaded_file(uploaded_file)
        if df is not None:
            set_dataframe(df)
            st.session_state.df_loaded = True
            st.success(f"✅ Loaded: {df.shape[0]} rows × {df.shape[1]} cols")
            st.dataframe(df.head(5), use_container_width=True)

    st.divider()
    st.markdown("**💡 Example questions:**")
    st.markdown("""
- *What are the top revenue drivers?*
- *Show monthly trends and forecast next quarter*
- *Which customer segment is most valuable?*
- *What anomalies exist in this data?*
- *Give me a full business analysis*
    """)

    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# ── Chat History ──────────────────────────────────────────────────────────────
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("chart") and os.path.exists(msg["chart"]):
            st.image(msg["chart"])

# ── Chat Input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input(
    "Ask a business question about your data...",
    disabled=not st.session_state.df_loaded
):
    # Show user message
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

   # Run agent
    with st.chat_message("assistant"):
        with st.spinner("🤖 Agent is analyzing... (may take 30-60s)"):
            try:
                response = run_agent(prompt, st.session_state.agent)
            except Exception as e:
                if "rate" in str(e).lower() or "429" in str(e):
                    response = "⚠️ Rate limit hit. Please wait 30 seconds and try again."
                else:
                    response = f"⚠️ Error: {str(e)}"

        st.markdown(response)

        # Show chart if generated
        chart_path = "charts/output.png"
        if os.path.exists(chart_path):
            st.image(chart_path, caption="📊 Generated Chart")

        # Save to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "chart": chart_path if os.path.exists(chart_path) else None
        })

# ── Empty State ───────────────────────────────────────────────────────────────
if not st.session_state.df_loaded:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Step 1**\n\nUpload a CSV or Excel file from the sidebar")
    with col2:
        st.info("**Step 2**\n\nAsk any business question about your data")
    with col3:
        st.info("**Step 3**\n\nGet a full analysis report with charts")