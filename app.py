
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="ProfitPlanr", layout="wide")
st.title("📈 ProfitPlanr – Trade Planning Assistant")

# Strategies and dynamic TP/SL settings
strategies = {
    "Scalping": {"duration": 5, "tp": 0.02, "sl": 0.01},
    "Day Trading": {"duration": 7, "tp": 0.03, "sl": 0.015},
    "Swing Trading": {"duration": 30, "tp": 0.10, "sl": 0.05},
    "ETFs": {"duration": 180, "tp": 0.15, "sl": 0.07},
    "Growth Investing": {"duration": 365, "tp": 0.30, "sl": 0.15},
    "Value Investing": {"duration": 365, "tp": 0.25, "sl": 0.10},
    "Long-Term Holding": {"duration": 730, "tp": 0.40, "sl": 0.15},
    "Dividend Investing": {"duration": 365, "tp": 0.12, "sl": 0.05}
}

st.sidebar.header("📌 Investment Strategy")
selected_strategy = st.sidebar.selectbox("Choose a strategy", list(strategies.keys()))
duration_days = strategies[selected_strategy]["duration"]
tp_pct = strategies[selected_strategy]["tp"]
sl_pct = strategies[selected_strategy]["sl"]

# --- Simulated Market Sentiment ---
sentiment_options = [
    {"label": "Extreme Fear 😱", "tp_adj": -0.02, "sl_adj": -0.01},
    {"label": "Fearful 😰", "tp_adj": -0.01, "sl_adj": -0.005},
    {"label": "Neutral 😐", "tp_adj": 0.00, "sl_adj": 0.00},
    {"label": "Greedy 😎", "tp_adj": 0.01, "sl_adj": 0.005},
    {"label": "Extreme Greed 🚀", "tp_adj": 0.02, "sl_adj": 0.01},
]
market_mood = random.choice(sentiment_options)
tp_pct += market_mood["tp_adj"]
sl_pct += market_mood["sl_adj"]
st.info(f"🧠 Simulated Market Sentiment: {market_mood['label']} — TP/SL adjusted accordingly.")

# Display sentiment-adjusted values
st.write(f"Final TP%: {round(tp_pct*100, 2)}%")
st.write(f"Final SL%: {round(sl_pct*100, 2)}%")
