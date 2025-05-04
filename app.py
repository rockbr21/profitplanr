
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

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

# Sidebar Chatbot
st.sidebar.markdown("## 🤖 Strategy Assistant")
with st.sidebar.expander("Ask Anything About Investing"):
    question = st.text_input("Your question here:")
    if question:
        q = question.lower()
        if "etf" in q:
            st.sidebar.info("An ETF is a basket of securities that trades like a stock on exchanges.")
        elif "roi" in q:
            st.sidebar.info("ROI = (Profit ÷ Invested) × 100")
        elif "stop" in q:
            st.sidebar.info("A Stop-Loss is a limit that sells your stock to prevent larger losses.")
        elif "take" in q:
            st.sidebar.info("A Take-Profit is a target where you sell to secure gains.")
        else:
            st.sidebar.info("Try asking about ROI, ETFs, stop-loss, or take-profit!")

# Step 1: Ticker Input
st.subheader("Step 1: Enter Tickers")
tickers_input = st.text_area("Enter NASDAQ stock tickers (one per line):", placeholder="e.g. AAPL\nTSLA\nQQQ", height=100)
tickers = [t.strip().upper() for t in tickers_input.splitlines() if t.strip()]

# Step 2: Trade Table
data = []
for ticker in tickers:
    try:
        price = round(yf.Ticker(ticker).history(period="5d")["Close"].iloc[-1], 2)
    except:
        price = 100
    data.append({
        "Ticker": ticker,
        "Avg Buy Price ($)": price,
        "Shares": 0,
        "Duration (Days)": duration_days,
        "Take-Profit ($)": round(price * (1 + tp_pct), 2),
        "Stop-Loss ($)": round(price * (1 - sl_pct), 2),
    })

if data:
    st.subheader("Step 2: Confirm or Edit Your Trade Info")
    df = pd.DataFrame(data)
    edited = st.data_editor(df, num_rows="fixed", use_container_width=True)

    st.subheader("📊 ROI Breakdown")
    rows = []
    for _, row in edited.iterrows():
        invested = row["Avg Buy Price ($)"] * row["Shares"]
        profit = (row["Take-Profit ($)"] - row["Avg Buy Price ($)"]) * row["Shares"]
        roi = (profit / invested) * 100 if invested else 0
        rows.append({
            "Ticker": row["Ticker"],
            "Profit ($)": round(profit, 2),
            "Invested ($)": round(invested, 2),
            "ROI (%)": round(roi, 2)
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.subheader("📉 Price Projection")
    fig = go.Figure()
    for _, row in edited.iterrows():
        start_price = row["Avg Buy Price ($)"]
        days = int(row["Duration (Days)"])
        dates = [datetime.today() + timedelta(days=i) for i in range(days)]
        prices = [start_price * (1 + 0.001 * i) for i in range(days)]
        upper = [p * 1.05 for p in prices]
        lower = [p * 0.95 for p in prices]
        fig.add_trace(go.Scatter(x=dates, y=prices, name=row["Ticker"], mode="lines"))
        fig.add_trace(go.Scatter(x=dates, y=upper, mode="lines", line=dict(width=0), showlegend=False))
        fig.add_trace(go.Scatter(x=dates, y=lower, mode="lines", line=dict(width=0), fill='tonexty', fillcolor='rgba(255,215,0,0.2)', showlegend=False))
    fig.update_layout(title="Forecasted Price Projection", xaxis_title="Date", yaxis_title="Price ($)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("📉 Projection data is simulated using daily growth estimates and public price history from Yahoo Finance.")

st.markdown("---")
st.markdown("_Designed and developed by Naris Borin_")
