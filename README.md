# Student Grade Analyzer

An interactive web app built with Python and Streamlit that analyzes student scores from a CSV file. Generates grade distributions, pass/fail breakdowns, score histograms, and a downloadable report — all in the browser.

## Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://sannanali-grade-analyzer-app-hwjtfr.streamlit.app/)


## Features

- Upload any CSV with student names and scores
- Summary metrics: average, highest, lowest score, pass rate
- Grade distribution bar chart (A / B / C / D / F)
- Score histogram with pass mark and average lines
- Pass vs Fail pie chart
- Adjustable passing score threshold via sidebar slider
- Color-coded results table
- Download full report as CSV
- Sample CSV included to try instantly

## How to Run Locally

```bash
git clone https://github.com/SannanAli/grade-analyzer.git
cd grade-analyzer
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

## CSV Format
Your CSV must have at a minimum a `Score` column. A `Name` column is optional.
