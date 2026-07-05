import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# पेज सेटअप
st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")

st.title("📈 Stock Trade Summary Dashboard")

# साईडबार - इनपुट
ticker = st.sidebar.text_input("स्टॉक सिम्बॉल टाका (उदा. TCS.NS)", "TCS.NS")
timeframe = st.sidebar.selectbox("Timeframe निवडा", ["5m", "15m", "1h", "1d", "1wk"])

# डेटा फेंचिंग फंक्शन
@st.cache_data(ttl=300)
def fetch_data(symbol, period):
    try:
        stock = yf.Ticker(symbol)
        # डेटासाठी योग्य कालावधी
        df = stock.history(period="1mo", interval=period)
        return df
    except Exception as e:
        return None

# मुख्य लॉजिक
if st.sidebar.button("Analyze"):
    data = fetch_data(ticker, timeframe)

    if data is None or data.empty:
        st.error(f"क्षमस्व, {ticker} साठी डेटा उपलब्ध नाही. कृपया सिम्बॉल तपासा (उदा. TCS.NS) आणि इंटरनेट कनेक्शन चेक करा.")
    else:
        # टेक्निकल ॲनालिसिस (Moving Average)
        data['SMA20'] = data['Close'].rolling(window=20).mean()
        
        last_price = data['Close'].iloc[-1]
        last_sma20 = data['SMA20'].iloc[-1]
        
        # ॲनालिसिस स्टेटस
        if last_price > last_sma20 * 1.02:
            status = "🔥 Strong"
            color = "green"
        elif last_price > last_sma20:
            status = "📈 Neutral-Strong"
            color = "blue"
        elif last_price < last_sma20 * 0.98:
            status = "❄️ Weak"
            color = "red"
        else:
            status = "⚖️ Neutral"
            color = "orange"

        # डॅशबोर्ड डिस्प्ले
        st.subheader(f"{ticker} साठी ॲनालिसिस")
        col1, col2 = st.columns(2)
        col1.metric("Current Status", status)
        col2.metric("Last Price", f"₹ {last_price:.2f}")

        # ग्राफ
        fig = px.line(data, y=['Close', 'SMA20'], title="Price vs SMA20")
        st.plotly_chart(fig, use_container_width=True)
        
        st.write("डेटा प्रीव्ह्यू:")
        st.dataframe(data.tail())

else:
    st.info("स्टॉक सिम्बॉल टाकून 'Analyze' बटणावर क्लिक करा.")
