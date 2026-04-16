import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from agent.tools import TOOLS
from agent.prompts import SYSTEM_PROMPT

load_dotenv()

def build_agent():
    """Build and return the LangGraph ReAct agent."""
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        api_key=os.getenv("GROQ_API_KEY")
    )

    agent = create_react_agent(
        model=llm,
        tools=TOOLS,
        prompt=SYSTEM_PROMPT
    )

    return agent

def run_agent(question: str, agent) -> str:
    """Run the agent and extract the final text response."""
    result = agent.invoke({
        "messages": [{"role": "user", "content": question}]
    })

    for msg in reversed(result["messages"]):
        if hasattr(msg, "content") and msg.content:
            if hasattr(msg, "type") and msg.type == "ai":
                if isinstance(msg.content, str) and len(msg.content) > 50:
                    return msg.content

    return "Analysis complete. Check the charts folder for visualizations."