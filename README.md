# 🤖 AutoAnalyst AI
> Autonomous Data Analysis Agent powered by LangGraph + Groq + Tavily

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://astitva028-autoanalyst-ai-app-fjqkgh.streamlit.app/)

## 🎯 What it does
Upload any business dataset (CSV/Excel) → Ask a business question → The AI agent autonomously:
1. **Inspects** the data structure and columns
2. **Plans** the analysis step by step
3. **Writes & executes** Python code to compute insights
4. **Generates** professional charts and visualizations
5. **Searches the web** for industry benchmarks and context
6. **Delivers** a structured business report with recommendations

## 🚀 Live Demo
👉 [https://astitva028-autoanalyst-ai-app-fjqkgh.streamlit.app/](https://astitva028-autoanalyst-ai-app-fjqkgh.streamlit.app/)

## 🛠️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Agent Framework | LangGraph (ReAct architecture) |
| LLM | Groq — LLaMA 3.3 70B |
| Web Search | Tavily Search API |
| Data Analysis | Pandas, Matplotlib, Seaborn |
| Frontend | Streamlit |
| Deployment | Streamlit Community Cloud |

## 🧠 Architecture
User (CSV + Question)
↓
[Streamlit UI]
↓
[LangGraph ReAct Agent]
┌─────────────────────────┐
│  PLAN → ACT → OBSERVE   │
│                         │
│  Tools:                 │
│  🔧 Python REPL         │
│  🔍 Tavily Web Search   │
│  📊 DataFrame Inspector │
└─────────────────────────┘
↓
[Business Report + Charts]

## 💡 Example Questions
- *"What are the top revenue drivers?"*
- *"Show monthly trends and forecast next quarter"*
- *"Which customer segment is most valuable?"*
- *"What anomalies exist in this data?"*
- *"Give me a full business analysis"*

## ⚙️ Run Locally
```bash
git clone https://github.com/Astitva028/autoanalyst-ai.git
cd autoanalyst-ai
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Create `.env` file:
```env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```
```bash
streamlit run app.py
```

## 📁 Project Structure
autoanalyst-ai/
├── app.py              # Streamlit UI
├── agent/
│   ├── graph.py        # LangGraph ReAct agent
│   ├── tools.py        # Python REPL, Web Search, DataFrame tools
│   └── prompts.py      # Agent system prompt
├── utils/
│   └── file_handler.py # CSV/Excel file loading
└── requirements.txt