import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from fitparse import FitFile
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="FIT File Analyzer", page_icon="❤️", layout="wide")

def load_fit_file(file_path):
    """Load a .fit file and extract heart rate data."""
    fitfile = FitFile(file_path)
    
    # Get all data messages that are of type "record"
    records = []
    for record in fitfile.get_messages("record"):
        record_dict = {}
        for record_data in record:
            record_dict[record_data.name] = record_data.value
        records.append(record_dict)
    
    df = pd.DataFrame(records)
    
    # Convert timestamp to datetime if it exists
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    return df

def calculate_metrics(hr_data):
    """Calculate heart rate metrics."""
    metrics = {
        "Average HR": round(hr_data.mean(), 1),
        "Min HR": int(hr_data.min()),
        "Max HR": int(hr_data.max()),
        "Q1 (25%)": int(np.percentile(hr_data, 25)),
        "Median HR": int(np.percentile(hr_data, 50)),
        "Q3 (75%)": int(np.percentile(hr_data, 75))
    }
    return metrics

def main():
    st.title("Garmin FIT File Analyzer")
    st.write("Upload a .fit file to analyze your activity heart rate data.")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a FIT file", type=["fit"])
    
    # Display sample file option
    use_sample = st.checkbox("Use sample file", value=False)
    
    data = None
    
    if uploaded_file is not None:
        # Save uploaded file temporarily
        with open("temp_upload.fit", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        data = load_fit_file("temp_upload.fit")
        st.success(f"Uploaded file processed successfully!")
        
        # Clean up
        os.remove("temp_upload.fit")
    
    elif use_sample:
        # Use the sample file in the directory
        sample_files = [f for f in os.listdir('.') if f.endswith('.fit')]
        if sample_files:
            selected_file = st.selectbox("Select a sample file", sample_files)
            data = load_fit_file(selected_file)
            st.success(f"Sample file '{selected_file}' processed successfully!")
        else:
            st.error("No sample .fit files found in the directory.")
    
    if data is not None and 'heart_rate' in data.columns:
        # Display heart rate time series plot
        st.header("Heart Rate Over Time")
        
        # Check if timestamp exists, otherwise use index
        if 'timestamp' in data.columns:
            x_axis = 'timestamp'
            title = "Heart Rate vs. Time"
        else:
            data['point_index'] = range(len(data))
            x_axis = 'point_index'
            title = "Heart Rate vs. Data Points"
        
        fig = px.line(
            data, 
            x=x_axis, 
            y='heart_rate',
            title=title,
            labels={'heart_rate': 'Heart Rate (bpm)', x_axis: 'Time'},
            template="plotly_white"
        )
        
        # Customize the layout
        fig.update_layout(
            xaxis_title="Time" if x_axis == 'timestamp' else "Data Points",
            yaxis_title="Heart Rate (bpm)",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate and display metrics
        metrics = calculate_metrics(data['heart_rate'])
        
        # Create columns for metrics
        st.header("Heart Rate Metrics")
        cols = st.columns(len(metrics))
        
        for i, (metric_name, metric_value) in enumerate(metrics.items()):
            cols[i].metric(metric_name, f"{metric_value} bpm")
        
        # Heart Rate Distribution
        st.header("Heart Rate Distribution")
        hist_fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(data['heart_rate'], bins=20, color='#FF4B4B', alpha=0.7)
        ax.set_xlabel('Heart Rate (bpm)')
        ax.set_ylabel('Frequency')
        ax.set_title('Heart Rate Distribution')
        ax.grid(True, alpha=0.3)
        
        # Add lines for key statistics
        ax.axvline(metrics['Average HR'], color='red', linestyle='-', label=f"Avg: {metrics['Average HR']} bpm")
        ax.axvline(metrics['Q1 (25%)'], color='green', linestyle='--', label=f"Q1: {metrics['Q1 (25%)']} bpm")
        ax.axvline(metrics['Median HR'], color='blue', linestyle='--', label=f"Median: {metrics['Median HR']} bpm")
        ax.axvline(metrics['Q3 (75%)'], color='purple', linestyle='--', label=f"Q3: {metrics['Q3 (75%)']} bpm")
        
        ax.legend()
        st.pyplot(hist_fig)
        
        # Display raw data if requested
        if st.checkbox("Show raw data"):
            st.subheader("Raw Data")
            st.dataframe(data)
    
    elif data is not None:
        st.error("No heart rate data found in the file.")

if __name__ == "__main__":
    main() 