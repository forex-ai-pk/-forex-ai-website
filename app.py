import streamlit as st

st.set_page_config(page_title="Forex AI Analyzer", page_icon="📈", layout="centered")

st.markdown("""
<style>
body { background-color: #121212; }
.card { background: #1E1E1E; padding: 20px; border-radius: 15px; margin-top: 20px; }
.buy { color: #00FF88; } .sell { color: #FF4444; }
</style>
""", unsafe_allow_html=True)

st.title("Forex AI Analyzer - Calm Companion")
st.caption("Educational only - Not financial advice. Trading is risky.")

uploaded = st.file_uploader("Upload chart screenshot (MT5/TradingView)", type=["png","jpg","jpeg"])
pair = st.text_input("Pair / Timeframe", "EURUSD H1")

if st.button("🔍 Analyze Chart"):
    if uploaded is None:
        st.warning("Pehle chart upload karo bhai")
    else:
        st.image(uploaded, caption="Your Chart")
        st.markdown("---")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Analysis Result (Demo Logic)")
        
        # YAHAN AAP KI STRATEGY LAGI HUI HAI
        st.markdown("""
        **Detected Pattern:** Hammer (from your notebook)
        **Bias:** <span class='buy'>Possible BUY - 72% Confidence</span>
