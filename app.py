import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *
from utils.predictor import predict_spending
# CONFIG
st.set_page_config(page_title="FinSight", layout="wide")
create_tables()

# 🎨 CORPORATE UI (POPPINS)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">
<style>

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* Background */
.stApp {
    background: #f8fafc;
}

/* Header */
.header {
    font-size: 32px;
    font-weight: 700;
    color: #1e293b;
}

/* Card */
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}

/* Button */
.stButton>button {
    background: #2563eb;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-weight: 500;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #ffffff;
}

</style>
""", unsafe_allow_html=True)

# SESSION
if "user" not in st.session_state:
    st.session_state.user = None

# ================= AUTH =================
if st.session_state.user is None:

    st.markdown('<div class="header">💼 FinSight Expense Manager</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    # LOGIN
    with tab1:
        st.subheader("Login")

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.user = user
                st.success("Welcome back!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # REGISTER
    with tab2:
        st.subheader("Register")

        new_user = st.text_input("Username", key="reg_user")
        new_pass = st.text_input("Password", type="password", key="reg_pass")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created!")
            else:
                st.error("Username already exists")

# ================= APP =================
else:
    user_id = st.session_state.user[0]

    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Menu", ["Dashboard", "Add Expense", "Transactions"])

    data = get_expenses(user_id)
    df = pd.DataFrame(data, columns=["ID","User","Amount","Category","Note","Date"])

    st.markdown('<div class="header">📊 Dashboard</div>', unsafe_allow_html=True)

    # DASHBOARD
    if menu == "Dashboard":
        if not df.empty:
            total = df["Amount"].sum()
            avg = df["Amount"].mean()

            c1, c2 = st.columns(2)

            c1.markdown(f'<div class="card">Total Spend: ₹ {total}</div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="card">Average Spend: ₹ {avg}</div>', unsafe_allow_html=True)

            fig = px.pie(df, names="Category", values="Amount")
            st.plotly_chart(fig, use_container_width=True)

            trend = df.groupby("Date")["Amount"].sum().reset_index()
            fig2 = px.line(trend, x="Date", y="Amount")
            st.plotly_chart(fig2, use_container_width=True)

    # ADD
    elif menu == "Add Expense":
        st.subheader("Add Expense")

        amount = st.number_input("Amount", min_value=1.0)
        category = st.selectbox("Category", ["Food","Travel","Shopping","Bills","Other"])
        note = st.text_input("Note")
        date = st.date_input("Date")

        if st.button("Add Expense"):
            add_expense(user_id, amount, category, note, str(date))
            st.success("Expense added!")
            st.rerun()

    # VIEW
    elif menu == "Transactions":
        st.subheader("All Transactions")
        st.dataframe(df, use_container_width=True)

        delete_id = st.number_input("Delete ID", min_value=1)

        if st.button("Delete"):
            delete_expense(delete_id)
            st.warning("Deleted")
            st.rerun()

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
