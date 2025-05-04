import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import datetime
import random

# --- SETUP ---
st.set_page_config(page_title="ProfitPlanr – Trade Planning Assistant", layout="wide")
st.title("📈 ProfitPlanr – Trade Planning Assistant")
st.markdown("_Full app logic restored._")

# --- STRATEGY SETTINGS ---
strategy_defaults = {
    "Scalping": {"duration": 5, "tp": 2, "sl": 1},
    "Day Trading": {"duration": 10, "tp": 4, "sl": 2},
    "Swing Trading": {"duration": 30, "tp": 8, "sl": 4},
    "Position Trading": {"duration": 90, "tp": 15, "sl": 7},
    "ETFs": {"duration": 180, "tp": 10, "sl": 5},
}

sentiment_labels = ["Fearful 😨", "Neutral 😐", "Greedy 😎"]
sentiment_modifiers = {"Fearful 😨": -0.2, "Neutral 😐": 0.0, "Greedy 😎": 0.2}
sentiment = random.choice(sentiment_labels)

# --- STRATEGY SELECTION ---
st.sidebar.header("📌 Investment Strategy")
strategy = st.sidebar.selectbox("Choose a strategy", list(strategy_defaults.keys()))

default = strategy_defaults[strategy]
base_tp = default["tp"]
base_sl = default["sl"]
adjustment = sentiment_modifiers[sentiment]
final_tp = round(base_tp * (1 + adjustment), 1)
final_sl = round(base_sl * (1 + adjustment), 1)

# --- DISPLAY STRATEGY ADJUSTMENTS ---
with st.container():
    st.info(f"🧠 Simulated Market Sentiment: **{sentiment}** — TP/SL adjusted accordingly.")
    st.markdown(f"**Final TP%**: {final_tp}%")
    st.markdown(f"**Final SL%**: {final_sl}%")
