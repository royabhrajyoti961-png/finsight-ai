
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *
from utils.predictor import predict_future, generate_insights

# ================= CONFIG =================
st.set_page_config(page_title="FinSight AI", layout="wide")
create_tables()

# ================= 🍎 APPLE UI =================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>

/* 🍎 FONT */
* {
    font-family: 'Poppins', sans-serif !important;
}

/* 🌈 SOFT BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #f9fafb, #eef2ff, #fdf2f8);
}

/* 💎 GLASS CARD */
.card {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(20px);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}

/* ✨ CARD HOVER */
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.08);
}

/* 🧊 KPI TEXT */
.kpi-title {
    font-size: 14px;
    color: #6b7280;
}

.kpi-value {
    font-size: 26px;
    font-weight: 600;
}

/* 🔘 BUTTON */
.stButton>button {
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    padding: 10px 16px;
    color: #111827;
    transition: 0.3s;
}

/* ✨ BUTTON HOVER */
.stButton>button:hover {
    background: #111827;
    color: white;
    transform: scale(1.04);
}

/* 📦 SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(20px);
}

/* ✏️ INPUT */
input {
    border-radius: 10px !important;
}

/* 📊 FADE ANIMATION */
.fade {
    animation: fadeIn 0.8s ease-in-out;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= AUTH =================
if st.session_state.user is None:

    st.markdown("<h2 class='fade'>💼 FinSight AI</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.user = user
                st.success("Welcome back ✨")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created 🎉")
            else:
                st.error("Username exists")

# ================= MAIN =================
else:
    user_id = st.session_state.user[0]

    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("", ["Dashboard", "Add Expense", "Transactions"])

    data = get_expenses(user_id)
    df = pd.DataFrame(data, columns=["ID","User","Amount","Category","Note","Date"])

    st.markdown("<h2 class='fade'>📊 Dashboard</h2>", unsafe_allow_html=True)

    # ================= DASHBOARD =================
    if menu == "Dashboard":

        if not df.empty:

            total = df["Amount"].sum()
            avg = df["Amount"].mean()

            c1, c2 = st.columns(2)

            c1.markdown(f"""
            <div class="card fade">
                <div class="kpi-title">Total Spending</div>
                <div class="kpi-value">₹ {total}</div>
            </div>
            """, unsafe_allow_html=True)

            c2.markdown(f"""
            <div class="card fade">
                <div class="kpi-title">Average Spending</div>
                <div class="kpi-value">₹ {avg:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

            # PIE
            fig = px.pie(df, names="Category", values="Amount")
            st.plotly_chart(fig, use_container_width=True)

            # TREND + PREDICTION
            daily, future = predict_future(df)

            if daily is not None:
                fig2 = px.line(daily, x="Date", y="Amount")

                if future is not None:
                    fig2.add_scatter(
                        x=future["Date"],
                        y=future["Predicted"],
                        mode="lines+markers",
                        name="Prediction"
                    )

                st.plotly_chart(fig2, use_container_width=True)

            # INSIGHTS
            st.subheader("🧠 Insights")
            for insight in generate_insights(df):
                st.markdown(f"<div class='card fade'>{insight}</div>", unsafe_allow_html=True)

        else:
            st.info("No expenses yet")

    # ================= ADD =================
    elif menu == "Add Expense":

        st.markdown("<h3 class='fade'>⚡ Quick Add</h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        amount = col1.number_input("Amount", min_value=1.0)
        category = col2.selectbox("Category", ["Food","Travel","Shopping","Bills","Other"])
        note = col3.text_input("Note")

        date = st.date_input("Date")

        if st.button("Add Expense"):
            add_expense(user_id, amount, category, note, str(date))
            st.success("Added ✨")
            st.rerun()

    # ================= TRANSACTIONS =================
    elif menu == "Transactions":

        st.markdown("<h3 class='fade'>📋 Transactions</h3>", unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True)

        delete_id = st.number_input("Delete ID", min_value=1)

        if st.button("Delete"):
            delete_expense(delete_id)
            st.warning("Deleted")
            st.rerun()

    # ================= LOGOUT =================
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
