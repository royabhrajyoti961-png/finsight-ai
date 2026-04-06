import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *
from utils.predictor import predict_future, generate_insights

# ================= CONFIG =================
st.set_page_config(page_title="FinSight AI", layout="wide")
create_tables()

# ================= PREMIUM UI =================
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>

/* 🔥 Force Poppins */
* {
    font-family: 'Poppins', sans-serif !important;
}

/* 🌈 Animated Background */
.stApp {
    background: linear-gradient(135deg, #fdfbfb, #ebedee, #e0f2fe, #fce7f3);
    background-size: 300% 300%;
    animation: gradientMove 12s ease infinite;
}

@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* 💎 Card */
.card {
    background: rgba(255,255,255,0.75);
    backdrop-filter: blur(12px);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

/* KPI */
.kpi {
    font-size: 20px;
    font-weight: 600;
}

/* 🚀 Button */
.stButton>button {
    background: linear-gradient(135deg, #6366f1, #3b82f6, #06b6d4);
    color: white;
    border-radius: 12px;
    padding: 10px;
    font-weight: 500;
    border: none;
}

.stButton>button:hover {
    transform: scale(1.05);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
}

</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= AUTH =================
if st.session_state.user is None:

    st.title("💼 FinSight AI")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.user = user
                st.success("Login Successful 🎉")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username", key="reg_user")
        new_pass = st.text_input("New Password", type="password", key="reg_pass")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created!")
            else:
                st.error("Username already exists")

# ================= MAIN =================
else:
    user_id = st.session_state.user[0]

    # 🌗 Theme Toggle
    dark_mode = st.sidebar.toggle("🌗 Dark Mode")

    if dark_mode:
        st.markdown("""
        <style>
        .stApp {background: #0f172a; color: white;}
        </style>
        """, unsafe_allow_html=True)

    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("Menu", ["Dashboard", "Add Expense", "Transactions"])

    data = get_expenses(user_id)
    df = pd.DataFrame(data, columns=["ID","User","Amount","Category","Note","Date"])

    st.title("📊 Dashboard")

    # ================= DASHBOARD =================
    if menu == "Dashboard":

        if not df.empty:

            total = df["Amount"].sum()
            avg = df["Amount"].mean()

            c1, c2 = st.columns(2)

            c1.markdown(f'<div class="card"><div class="kpi">💰 Total Spend</div><br>₹ {total}</div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="card"><div class="kpi">📊 Avg Spend</div><br>₹ {avg:.2f}</div>', unsafe_allow_html=True)

            # Pie Chart
            fig = px.pie(df, names="Category", values="Amount", title="Spending Distribution")
            st.plotly_chart(fig, use_container_width=True)

            # Prediction
            daily, future = predict_future(df)

            if daily is not None:
                fig2 = px.line(daily, x="Date", y="Amount", title="Spending Trend")

                if future is not None:
                    fig2.add_scatter(
                        x=future["Date"],
                        y=future["Predicted"],
                        mode='lines+markers',
                        name="Prediction"
                    )

                st.plotly_chart(fig2, use_container_width=True)

            # Insights
            st.subheader("🧠 Smart Insights")
            insights = generate_insights(df)

            for i in insights:
                st.info(i)

        else:
            st.warning("No data yet")

    # ================= ADD =================
    elif menu == "Add Expense":

        st.subheader("⚡ Quick Add Expense")

        col1, col2, col3 = st.columns(3)

        amount = col1.number_input("💰 Amount", min_value=1.0)
        category = col2.selectbox("📂 Category", ["Food","Travel","Shopping","Bills","Other"])
        note = col3.text_input("📝 Note")

        date = st.date_input("Date")

        if st.button("➕ Add Expense"):
            add_expense(user_id, amount, category, note, str(date))
            st.success("Added 🚀")
            st.rerun()

    # ================= TRANSACTIONS =================
    elif menu == "Transactions":

        st.subheader("📋 All Transactions")
        st.dataframe(df, use_container_width=True)

        delete_id = st.number_input("Enter ID to Delete", min_value=1)

        if st.button("Delete"):
            delete_expense(delete_id)
            st.warning("Deleted")
            st.rerun()

    # ================= LOGOUT =================
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()
