import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Page Configuration
st.set_page_config(
    page_title="AI-Powered Revenue Leakage Detection",
    page_icon="🔍",
    layout="wide"
)

# Custom CSS for Modern Styling
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
    }
    .css-18e3th9 {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
    }
    .css-1d391kg {
        text-align: center;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        font-size: 16px;
        padding: 10px 20px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        transform: scale(1.05);
    }
    .footer {
        position: fixed;
        bottom: 10px;
        right: 20px;
        font-size: 12px;
        color: #6c757d;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown("""
    <h1 style='text-align: center; color: #007bff;'>📊 AI-Powered Revenue Leakage Detection Dashboard</h1>
    <h4 style='text-align: center; color: #6c757d;'>Detect anomalies and prevent revenue loss using AI</h4>
    <hr>
""", unsafe_allow_html=True)

# File Uploader
uploaded_file = st.file_uploader(
    "📂 Upload your financial transactions CSV file",
    type=["csv"],
    help="Ensure your file contains valid financial transaction data."
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Display Uploaded Data
    st.markdown("<h4 style='color: #17a2b8;'>📄 Uploaded Data Preview</h4>", unsafe_allow_html=True)
    st.dataframe(df.head())
    
    # Analyze Transactions
    with st.spinner("🔍 Analyzing transactions..."):
        response = requests.post("http://127.0.0.1:5000/upload", files={"file": uploaded_file})
    
    if response.status_code == 200:
        anomalies = response.json().get("anomalies", [])
        
        if anomalies:
            st.markdown("<h4 style='color: #dc3545;'>🚨 Detected Anomalies</h4>", unsafe_allow_html=True)
            anomalies_df = pd.DataFrame(anomalies)
            st.dataframe(anomalies_df)

            # Interactive Anomaly Graph
            st.markdown("<h4 style='color: #28a745;'>📈 Anomaly Distribution</h4>", unsafe_allow_html=True)
            fig = px.histogram(
                anomalies_df, 
                x="Amount", 
                nbins=50, 
                title="Anomalous Transaction Amounts", 
                color_discrete_sequence=["#17a2b8"]
            )
            st.plotly_chart(fig, use_container_width=True)

            # Filter Options
            st.markdown("<h4 style='color: #ffc107;'>🔎 Filter Anomalies</h4>", unsafe_allow_html=True)
            filter_type = st.selectbox("Select Transaction Type", anomalies_df['type'].unique(), index=0)
            filtered_df = anomalies_df[anomalies_df['type'] == filter_type]
            st.dataframe(filtered_df)

            st.success("✅ Analysis complete! Review detected anomalies and take corrective actions.")
        else:
            st.success("✅ No anomalies detected in the transactions.")
    else:
        st.error("❌ Failed to process file. Please try again.")

# Footer with User ID
st.markdown("""
    <div class="footer">
        <p>📌 Dashboard ID: <strong>23020023</strong></p>
    </div>
""", unsafe_allow_html=True)
