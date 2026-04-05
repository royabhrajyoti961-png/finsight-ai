import streamlit as st
from utils.db import *

st.set_page_config(page_title="FinSight AI", layout="centered")
create_tables()

# 🌈 PREMIUM LIGHT TEXTURED BACKGROUND
st.markdown("""
<style>

/* 🌈 Background */
.stApp {
    background: linear-gradient(135deg, #fef9c3, #dbeafe, #fbcfe8, #dcfce7);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
}

/* Gradient animation */
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Glass Card */
.card {
    background: rgba(255,255,255,0.75);
    padding: 40px;
    border-radius: 25px;
    backdrop-filter: blur(15px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.1);
}

/* Heading */
.title {
    font-size: 32px;
    font-weight: bold;
    text-align: center;
    color: #1e293b;
}

/* Input fields */
input {
    border-radius: 12px !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#3b82f6,#22c55e,#a855f7);
    color: white;
    border-radius: 12px;
    padding: 12px;
    font-weight: bold;
    border: none;
}

/* Center box */
.container {
    display: flex;
    justify-content: center;
    margin-top: 80px;
}

</style>
""", unsafe_allow_html=True)

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# ================= LOGIN / REGISTER UI =================
if st.session_state.user is None:

    st.markdown('<div class="container">', unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('<div class="title">🔐 Login</div>', unsafe_allow_html=True)

        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login(login_user, login_pass)
            if user:
                st.session_state.user = user
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.markdown('<div class="title">📝 Register</div>', unsafe_allow_html=True)

        reg_user = st.text_input("Create Username", key="reg_user")
        reg_pass = st.text_input("Create Password", type="password", key="reg_pass")

        if st.button("Register"):
            success = register(reg_user, reg_pass)
            if success:
                st.success("Account Created!")
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
        <h3>🚀 Dashboard Coming Next</h3>
        <p>You have successfully logged in.</p>
    </div>
    """, unsafe_allow_html=True)
