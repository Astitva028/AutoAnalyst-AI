import pandas as pd
import streamlit as st

def load_uploaded_file(uploaded_file) -> pd.DataFrame | None:
    """Load CSV or Excel file into a DataFrame."""
    if uploaded_file is None:
        return None

    try:
        if uploaded_file.name.endswith(".csv"):
            # Try utf-8 first, fall back to latin-1
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                uploaded_file.seek(0)  # Reset file pointer
                df = pd.read_csv(uploaded_file, encoding="latin-1")

        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Only CSV and Excel files are supported.")
            return None

        return df

    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None