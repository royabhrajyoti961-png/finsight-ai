import streamlit as st
from utils.db import *

st.set_page_config(page_title="FinSight AI", layout="centered")
create_tables()

# 🌈 ULTRA PREMIUM CSS (ANIMATED BG + BUTTONS)
st.markdown("""
<style>

/* 🌈 BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #fef9c3, #dbeafe, #fbcfe8, #dcfce7);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

/* 🌈 ANIMATION */
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* 💎 GLASS CARD */
.card {
    background: rgba(255,255,255,0.75);
    padding: 40px;
    border-radius: 25px;
    backdrop-filter: blur(15px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.1);
    transition: 0.3s;
}

/* ✨ HOVER CARD */
.card:hover {
    transform: translateY(-5px);
}

/* 🔐 TITLE */
.title {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
    color: #1e293b;
}

/* 🧾 INPUT */
input {
    border-radius: 12px !important;
}

/* 🚀 DYNAMIC BUTTON */
.stButton>button {
    background: linear-gradient(270deg, #3b82f6, #22c55e, #a855f7, #ec4899);
    background-size: 600% 600%;
    animation: buttonGradient 8s ease infinite;
    color: white;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px;
    border: none;
    transition: 0.3s;
}

/* ✨ BUTTON ANIMATION */
@keyframes buttonGradient {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* 🌟 BUTTON HOVER */
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(168,85,247,0.5);
}

/* 📦 CENTER */
.container {
    display: flex;
    justify-content: center;
    margin-top: 80px;
}

/* SIDEBAR LIGHT */
section[data-testid="stSidebar"] {
    background: #ffffff;
}

</style>
""", unsafe_allow_html=True)

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# ================= LOGIN / REGISTER =================
if st.session_state.user is None:

    st.markdown('<div class="container">', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # LOGIN
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('<div class="title">🔐 Login</div>', unsafe_allow_html=True)

        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login(login_user, login_pass)
            if user:
                st.session_state.user = user
                st.success("Login Successful 🎉")
                st.rerun()
            else:
                st.error("Invalid Credentials")

        st.markdown('</div>', unsafe_allow_html=True)

    # REGISTER
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('<div class="title">📝 Register</div>', unsafe_allow_html=True)

        reg_user = st.text_input("Create Username", key="reg_user")
        reg_pass = st.text_input("Create Password", type="password", key="reg_pass")

        if st.button("Register"):
            success = register(reg_user, reg_pass)
            if success:
                st.success("Account Created 🚀")
            else:
                st.warning("Username already exists")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= AFTER LOGIN =================
else:
    st.success(f"Welcome {st.session_state.user[1]} 🎉")

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()

    st.markdown("""
    <div class="card">
        <h3>🚀 Dashboard Ready</h3>
        <p>This UI is now hackathon-level premium.</p>
    </div>
    """, unsafe_allow_html=True)
