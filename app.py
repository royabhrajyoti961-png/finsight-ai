import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *
from utils.predictor import predict_future, generate_insights

# ================= CONFIG =================
st.set_page_config(page_title="FinSight AI", layout="wide")
create_tables()

# ================= THEME =================
theme = st.sidebar.toggle("🌗 Dark Mode")

if theme:
    bg = "#0f172a"
    text = "#ffffff"
    card = "#1e293b"
else:
    bg = "#f8fafc"
    text = "#1e293b"
    card = "#ffffff"

# ================= UI =================
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap" rel="stylesheet">

<style>
html, body, [class*="css"] {{
    font-family: 'Poppins', sans-serif;
}}

.stApp {{
    background: {bg};
    color: {text};
}}

.card {{
    background: {card};
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
}}

.stButton>button {{
    background: #2563eb;
    color: white;
    border-radius: 10px;
    padding: 10px;
    font-weight: 500;
}}

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

# ================= MAIN APP =================
else:
    user_id = st.session_state.user[0]

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
            c1.markdown(f'<div class="card">💰 Total Spend: ₹ {total}</div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="card">📊 Avg Spend: ₹ {avg:.2f}</div>', unsafe_allow_html=True)

            # PIE CHART
            fig = px.pie(df, names="Category", values="Amount", title="Category Distribution")
            st.plotly_chart(fig, use_container_width=True)

            # 📈 TREND + PREDICTION
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

            # 🧠 INSIGHTS
            st.subheader("🧠 Smart Insights & Alerts")

            insights = generate_insights(df)

            for i in insights:
                st.info(i)

        else:
            st.warning("No data available. Add expenses to see analytics.")

    # ================= ADD =================
    elif menu == "Add Expense":

        st.subheader("⚡ Quick Add Expense")

        col1, col2, col3 = st.columns(3)

        amount = col1.number_input("Amount", min_value=1.0)
        category = col2.selectbox("Category", ["Food","Travel","Shopping","Bills","Other"])
        note = col3.text_input("Note")

        date = st.date_input("Date")

        if st.button("➕ Add Expense"):
            add_expense(user_id, amount, category, note, str(date))
            st.success("Added instantly 🚀")
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
