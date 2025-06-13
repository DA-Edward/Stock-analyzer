import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")
st.title("📈 Crisis-Resilient Stock Performance (2000–2025)")

default_tickers = ['XOM', 'CVX', 'LMT', 'RTX', 'GD', 'NOC', 'GLD', 'XLP', 'XLU', 'SPY']
tickers = st.multiselect("Select stocks or ETFs:", default_tickers, default=default_tickers)

start = st.date_input("Start Date", datetime(2000, 1, 1))
end = st.date_input("End Date", datetime.today())

if tickers:
    st.info("Loading data...")
    try:
        raw_data = yf.download(tickers, start=start, end=end)

        if raw_data.empty:
            st.warning("⚠️ No data returned. Try different tickers or date range.")
            st.stop()

        # Handle single vs multiple ticker cases
        if isinstance(raw_data.columns, pd.MultiIndex):
            if 'Adj Close' not in raw_data.columns:
                st.error("⚠️ 'Adj Close' not found in data. Some tickers may be invalid.")
                st.dataframe(raw_data.head())
                st.stop()
            data = raw_data['Adj Close']
        else:
            if 'Adj Close' not in raw_data:
                st.error("⚠️ 'Adj Close' not found. Try a different ticker.")
                st.dataframe(raw_data.head())
                st.stop()
            data = raw_data[['Adj Close']]

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

    except Exception as e:
        st.error(f"❌ Error loading or processing data: {e}")
