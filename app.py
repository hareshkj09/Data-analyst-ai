import importlib
import json
import google.generativeai as genai
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI Data Analyst & Visualisation Engine", layout="wide"
)

st.title("📊 AI Data Analyst with Schema & Visualisation Engine")
st.write(
    "Upload any dataset (CSV/Excel/JSON) to query rows, understand schema, and"
    " generate dynamic charts."
)

# Configure Gemini API Key securely
try:
  api_key = st.secrets["GEMINI_API_KEY"]
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel("gemini-3.8-flash")
")
except Exception as e:
    st.error(f"API setup error: {e}")
  model = None

uploaded_file = st.file_uploader(
    "Upload your dataset (CSV, Excel or JSON)", type=["csv", "xlsx", "json"]
)

if uploaded_file is not None:
  if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
  elif uploaded_file.name.endswith(".xlsx"):
    df = pd.read_excel(uploaded_file)
  else:
    df = pd.read_json(uploaded_file)

  # Safe data cleaning for AY column
  if "AY" in df.columns:
    df["AY"] = pd.to_numeric(df["AY"], errors="coerce")

  st.subheader("📋 Dataset Preview & Schema")
  st.dataframe(df.head())

  st.info(
      f"Shape: {df.shape[0]} rows, {df.shape[1]} columns | Columns detected:"
      f" {list(df.columns)}"
  )

  user_query = st.text_input(
      "Ask a question (e.g., 'Show total revenue by region as a bar chart'):"
  )

  if user_query and model:
    with st.spinner("Analyzing data structure and generating insights..."):
      # 1. Capture Schema Information
      schema_info = df.dtypes.to_string()
      full_data_text = df.to_string()

      # 2. Text Response Prompt
      prompt = f"""
            You are an expert data analyst. 
            
            SCHEMA INFORMATION:
            {schema_info}
            
            ENTIRE DATASET:
            {full_data_text}
            
            USER QUESTION: {user_query}
            
            Analyze the dataset and provide a clear, detailed text response answering the user question.
            """

      try:
        response = model.generate_content(prompt)
        
        # Display Text Answer
        st.success("### Analysis Result")
        st.write(response.text)

      except Exception as e:
        st.error(f"An error occurred: {e}")