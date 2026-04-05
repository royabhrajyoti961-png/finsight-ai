import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *
from utils.predictor import predict_spending

st.set_page_config(page_title="FinSight AI", layout="wide")
create_tables()

# 🌈 UI
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fef9c3, #dbeafe, #fbcfe8, #dcfce7);
    background-size: 400% 400%;
    animation: bg 10s ease infinite;
}
@keyframes bg {
    0% {background-position:0%}
    50% {background-position:100%}
    100% {background-position:0%}
}
.card {
    background: rgba(255,255,255,0.8);
    padding: 20px;
    border-radius: 20px;
}
.kpi {
    background: rgba(255,255,255,0.7);
    padding: 15px;
    border-radius: 15px;
}
.stButton>button {
    background: linear-gradient(270deg,#3b82f6,#22c55e,#a855f7,#ec4899);
    background-size:600% 600%;
    animation: btn 6s ease infinite;
    color:white;
    border-radius:12px;
}
@keyframes btn {
    0%{background-position:0%}
    50%{background-position:100%}
    100%{background-position:0%}
}
</style>
""", unsafe_allow_html=True)

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# ================= LOGIN =================
if st.session_state.user is None:
    st.title("🔐 FinSight AI Login")

    col1,col2 = st.columns(2)

    with col1:
        st.subheader("Login")
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login"):
            user = login(u,p)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid")

    with col2:
        st.subheader("Register")
        ru = st.text_input("New Username")
        rp = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register(ru,rp):
                st.success("Registered!")
            else:
                st.warning("User exists")

# ================= APP =================
else:
    user_id = st.session_state.user[0]

    menu = st.sidebar.radio("Menu", ["Dashboard","Add","Transactions"])

    data = get_transactions(user_id)
    df = pd.DataFrame(data, columns=["ID","User","Amount","Category","Note","Date"])

    # DASHBOARD
    if menu == "Dashboard":
        if not df.empty:
            total = df["Amount"].sum()
            avg = df["Amount"].mean()

            c1,c2 = st.columns(2)
            c1.markdown(f'<div class="kpi">Total ₹ {total}</div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="kpi">Avg ₹ {avg}</div>', unsafe_allow_html=True)

            fig = px.pie(df, names="Category", values="Amount")
            st.plotly_chart(fig)

            trend = df.groupby("Date")["Amount"].sum().reset_index()
            fig2 = px.line(trend, x="Date", y="Amount")
            st.plotly_chart(fig2)

            pred = predict_spending(df)
            if pred:
                st.markdown(f'<div class="card">Predicted ₹ {pred}</div>', unsafe_allow_html=True)

    # ADD
    elif menu == "Add":
        amt = st.number_input("Amount", min_value=1.0)
        cat = st.selectbox("Category", ["Food","Travel","Shopping","Bills","Other"])
        note = st.text_input("Note")
        date = st.date_input("Date")

        if st.button("Add"):
            add_transaction(user_id, amt, cat, note, str(date))
            st.success("Added")
            st.rerun()

    # VIEW
    elif menu == "Transactions":
        st.dataframe(df)

        did = st.number_input("Delete ID", min_value=1)
        if st.button("Delete"):
            delete_transaction(did)
            st.warning("Deleted")
            st.rerun()

    if st.button("Logout"):
        st.session_state.user = None
        st.rerun()
