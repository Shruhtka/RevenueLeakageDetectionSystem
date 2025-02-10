### Streamlit Dashboard (dashboard.py)
import streamlit as st
import pandas as pd
import requests

st.title("🔍 Revenue Leakage Detection System")

# File upload
uploaded_file = st.file_uploader("📂 Upload your financial transactions CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("## 📊 Uploaded Data Preview")
    st.dataframe(df.head())
    
    # Send data to backend API for anomaly detection
    API_URL = "http://127.0.0.1:8000/upload"
    
    with st.spinner("🔄 Analyzing transactions..."):
        response = requests.post(API_URL, files={"file": uploaded_file})
        
    if response.status_code == 200:
        anomalies = response.json().get("anomalies", [])
        if anomalies:
            st.write("## 🚨 Detected Anomalies")
            anomalies_df = pd.DataFrame(anomalies)
            st.dataframe(anomalies_df)
        else:
            st.success("✅ No anomalies detected in the transactions.")
    else:
        st.error("❌ Failed to process file. Please try again.")
