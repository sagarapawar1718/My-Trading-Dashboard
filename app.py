import streamlit as st
import yfinance as yf
import pandas_ta as ta # तांत्रिक इंडिकेटर्ससाठी

st.set_page_config(layout="wide")
st.title("📊 TradingView Style Analysis Dashboard")

ticker = st.sidebar.text_input("स्टॉक सिम्बॉल (उदा. RELIANCE.NS)", "RELIANCE.NS")
timeframe = st.sidebar.selectbox("Timeframe", ["5m", "15m", "1h", "1d"])

def get_technical_analysis(df):
    # RSI (Relative Strength Index)
    df['RSI'] = ta.rsi(df['Close'], length=14)
    # 20 EMA
    df['EMA20'] = ta.ema(df['Close'], length=20)
    # MACD
    macd = ta.macd(df['Close'])
    df = pd.concat([df, macd], axis=1)
    return df

if st.sidebar.button("Analyze"):
    df = yf.download(ticker, period="1mo", interval=timeframe)
    df = get_technical_analysis(df)
    
    curr_price = df['Close'].iloc[-1]
    rsi = df['RSI'].iloc[-1]
    ema20 = df['EMA20'].iloc[-1]
    
    # TradingView सारखे लॉजिक
    signals = 0
    if rsi < 30: signals += 1 # Buy signal
    elif rsi > 70: signals -= 1 # Sell signal
    
    if curr_price > ema20: signals += 1
    else: signals -= 1

    # Summary
    st.subheader("Technical Summary")
    if signals > 0:
        st.success("Strong Buy / Strong")
    elif signals < 0:
        st.error("Strong Sell / Weak")
    else:
        st.warning("Neutral")

    st.write(f"RSI: {rsi:.2f} | EMA20: {ema20:.2f}")
