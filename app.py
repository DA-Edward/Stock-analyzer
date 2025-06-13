import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(layout="wide")
st.title("📈 Crisis-Resilient Stock Performance (2000–2025)")

default_tickers = ['XOM', 'CVX', 'LMT', 'RTX', 'GD', 'NOC', 'GLD', 'XLP', 'XLU', 'SPY']
tickers = st.multiselect("Select stocks or ETFs:", default_tickers, default=default_tickers)

start = st.date_input("Start Date", datetime(2000, 1, 1))
end = st.date_input("End Date", datetime.today())

if tickers:
    st.info("Loading data...")
    data = yf.download(tickers, start=start, end=end)['Adj Close']
    normalized = data / data.iloc[0]

    st.subheader("📊 Normalized Chart (Start = 1.0)")
    fig, ax = plt.subplots(figsize=(14, 6))
    for t in normalized.columns:
        ax.plot(normalized.index, normalized[t], label=t)
    ax.set_ylabel("Normalized Price")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.subheader("🔢 Return Summary")
    returns = ((normalized.iloc[-1] - 1) * 100).sort_values(ascending=False).round(2)
    st.dataframe(returns.rename("Return (%)"))
