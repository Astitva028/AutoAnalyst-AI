import os
import sys
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for Streamlit
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
from langchain.tools import tool
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
load_dotenv()

# ── Global dataframe store ────────────────────────────────────────────────────
_dataframe_store: dict = {}

def set_dataframe(df: pd.DataFrame):
    _dataframe_store["df"] = df

def get_dataframe() -> pd.DataFrame | None:
    return _dataframe_store.get("df")

# ── Tool 1: DataFrame Info ────────────────────────────────────────────────────
@tool
def get_dataframe_info(query: str) -> str:
    """
    Get metadata about the uploaded dataframe: shape, columns, dtypes,
    missing values, and a sample. Call this FIRST before any analysis.
    """
    df = get_dataframe()
    if df is None:
        return "No dataframe loaded."

    info = f"""
Shape: {df.shape[0]} rows x {df.shape[1]} columns
Columns: {list(df.columns)}
Data Types:
{df.dtypes.to_string()}
Missing Values:
{df.isnull().sum().to_string()}
Sample (first 3 rows):
{df.head(3).to_string()}
Basic Stats:
{df.describe().to_string()}
"""
    return info

# ── Tool 2: Python REPL ───────────────────────────────────────────────────────
@tool
def python_repl(code: str) -> str:
    """
    Execute Python code for data analysis.
    The uploaded dataframe is available as variable `df`.
    Always print() your results so they appear in output.
    For charts, use plt.savefig('charts/output.png') then plt.close().
    """
    os.makedirs("charts", exist_ok=True)

    df = get_dataframe()
    if df is None:
        return "Error: No dataframe loaded. Ask user to upload a CSV first."

    local_vars = {"df": df, "pd": pd, "plt": plt, "sns": sns, "os": os}

    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        exec(code, local_vars)
        output = sys.stdout.getvalue()
        return output if output else "Code executed successfully (no printed output)."
    except Exception as e:
        return f"Error executing code: {str(e)}"
    finally:
        sys.stdout = old_stdout

# ── Tool 3: Web Search ────────────────────────────────────────────────────────
web_search = TavilySearch(max_results=3)

# ── All tools in one list ─────────────────────────────────────────────────────
TOOLS = [get_dataframe_info, python_repl, web_search]