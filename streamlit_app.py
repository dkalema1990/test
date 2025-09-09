import streamlit as st
import pandas as pd
import numpy as np
import openpyxl as xl


st.title("🎈 Excel Upload")
st.write(
    "How to upload excel files in streamlit")

st.title("Excel File Loader")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("File uploaded successfully! Here's the first few rows:")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
