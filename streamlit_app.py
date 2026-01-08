import streamlit as st
import pandas as pd
import numpy as np

# Assuming you have pages/home.py and pages/dashboard.py
st.sidebar.title("Custom Navigation")
st.sidebar.page_link("test.py", label="Home", icon="🏠")
## st.sidebar.page_link("pages/dashboard.py", label="Dashboard", icon="📊")
st.sidebar.page_link("https://docs.streamlit.io", label="Streamlit Docs", icon="📚")

st.title("Welcome to the Home Page")
st.write("This is the main content area.")


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


st.set_page_config(page_title="Data Aggregation App", layout="wide")

st.title("Simple Data Aggregation Application")

# Function to load and cache data for performance
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            # Assuming the data is in CSV format
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error loading file: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

# File uploader widget
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

df = load_data(uploaded_file)

if not df.empty:
    st.subheader("Raw Data Preview")
    st.dataframe(df.head())

    st.subheader("Data Aggregation")

    # User selects columns for grouping and aggregation
    available_columns = df.columns.tolist()
    group_by_cols = st.multiselect("Select column(s) to group by", available_columns)
    
    # Identify numeric columns for aggregation
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    aggregation_col = st.selectbox("Select column to aggregate", numeric_cols)
    aggregation_func = st.selectbox("Select aggregation function", ["mean", "sum", "min", "max", "count"])

    if st.button("Perform Aggregation"):
        if group_by_cols and aggregation_col:
            try:
                # Perform the aggregation
                aggregated_data = df.groupby(group_by_cols)[aggregation_col].agg(aggregation_func).reset_index()
                st.write(f"### Aggregated Results ({aggregation_func} of {aggregation_col})")
                st.dataframe(aggregated_data)

                # Optional: display a simple chart of the results
                st.bar_chart(aggregated_data.set_index(group_by_cols))
            except Exception as e:
                st.error(f"An error occurred during aggregation: {e}")
        else:
            st.warning("Please select at least one column to group by and one column to aggregate.")
else:
    st.info("Please upload a file to begin.")
