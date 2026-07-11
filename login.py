import streamlit as st

st.set_page_config(
    page_title="AI Pharmacovigilance Login",
    page_icon="🔐",
    layout="centered"
)

st.markdown("""
<style>
.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b);
}

h1{
    color:white;
    text-align:center;
}

label{
    color:white !important;
}

.stTextInput label{
    color:white !important;
}

.stButton>button{
    width:100%;
    background:#2563eb;
    color:white;
    border-radius:10px;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔐 AI Pharmacovigilance Dashboard")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "admin" and password == "admin123":
        st.success("✅ Login Successful")
    else:
        st.error("❌ Invalid Username or Password")