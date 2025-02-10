### Flask API (app.py)
from flask import Flask, request, jsonify
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load pre-trained Isolation Forest model
iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process file
        df = pd.read_csv(filepath)
        df = preprocess_data(df)  # Preprocess data
        anomalies = detect_anomalies(df)
        
        return jsonify({'anomalies': anomalies}), 200

# Preprocessing function
def preprocess_data(df):
    if 'Amount' in df.columns:
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        df['Amount'] = scaler.fit_transform(df[['Amount']])
    return df.drop(columns=['Time'], errors='ignore')

# Anomaly detection function
def detect_anomalies(df):
    preds = iso_forest.fit_predict(df)
    anomalies = df[preds == -1].to_dict(orient='records')
    return anomalies

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)


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
