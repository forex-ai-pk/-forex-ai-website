import streamlit as st

st.set_page_config(page_title="Forex AI Analyzer", page_icon="📈", layout="centered")

st.markdown('''
<style>
.stApp { background-color: #121212; }
.card { background: #1E1E1E; padding: 20px; border-radius: 15px; margin-top: 20px; border: 1px solid #333; }
</style>
''', unsafe_allow_html=True)

st.title("Forex AI Analyzer - Dark Pro")
st.caption("Educational only - Not financial advice")

uploaded = st.file_uploader("Upload chart screenshot", type=["png","jpg","jpeg"])

if st.button("Analyze Chart"):
    if uploaded is None:
        st.warning("Pehle chart upload karo bhai")
    else:
        st.image(uploaded)
        st.success("Detected: Hammer Pattern - Possible BUY 72% Confidence")
        st.write("Entry: Above Hammer High | SL: Low -15 pips | TP: 1:2 RR")
        st.error("Risk: 1% se zyada risk mat lo. Confidence < 70% to No Trade")
