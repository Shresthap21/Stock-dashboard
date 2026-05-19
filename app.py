import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Title
st.title("Stock Data Visualization Dashboard")

# User inputs
symbol = st.text_input("Enter Stock Symbol (e.g. AAPL, TSLA, MSFT):", "AAPL")
period = st.selectbox("Select Time Period:", ["1mo", "3mo", "6mo", "1y", "5y", "max"])

# Fetch data
data = yf.Ticker(symbol).history(period=period)

if data.empty:
    st.warning("Please check symbol, no data shown");
else:
    st.subheader(f"Show data for {symbol.upper()} ({period})")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))
    
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], mode='lines', name='20-day SMA'))
    
    fig.update_layout(
        title=f"{symbol.upper()}",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

    # Volume chart
    st.subheader("Trading Volume")
    vol_fig = go.Figure()
    vol_fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name="Volume"))
    vol_fig.update_layout(template="plotly_dark", xaxis_title="Date", yaxis_title="Volume")
    st.plotly_chart(vol_fig, use_container_width=True)
