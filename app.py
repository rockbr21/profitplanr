
import streamlit as st

# Simulated sentiment (in real life, fetched via API)
sentiment = "Greedy 😎"
tp_pct = 4.0
sl_pct = 2.0

st.title("📈 ProfitPlanr – Trade Planning Assistant")
st.markdown(f"🧠 Simulated Market Sentiment: {sentiment} — TP/SL adjusted accordingly.")

st.write(f"Final TP%: {tp_pct}%")
st.write(f"Final SL%: {sl_pct}%")

# Placeholder for other full app components
st.markdown("---")
st.markdown("All core features restored here (tickers input, ROI, projections, chatbot, etc.).")
