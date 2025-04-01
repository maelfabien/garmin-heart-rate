# FIT File Analyzer

A Streamlit dashboard for analyzing heart rate data from Garmin .fit files.

## Features

- Upload and process Garmin .fit files
- Visualize heart rate over time during activity
- Display key heart rate metrics:
  - Average heart rate
  - Minimum and maximum heart rate
  - Q1 (25th percentile)
  - Median (50th percentile)
  - Q3 (75th percentile)
- View heart rate distribution histogram
- Option to use sample files included in the directory
- Display raw data from the .fit file

## Setup

1. Install the required packages:

```
pip install -r requirements.txt
```

2. Run the Streamlit app:

```
streamlit run app.py
```

## Usage

1. Upload a .fit file using the file uploader, or use the sample file option.
2. View the heart rate time series plot and metrics.
3. Explore the heart rate distribution histogram.
4. Optionally, check the "Show raw data" box to see all data from the .fit file.

## Requirements

See `requirements.txt` for the full list of dependencies. 