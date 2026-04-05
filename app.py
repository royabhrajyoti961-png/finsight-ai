import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *
from utils.predictor import predict_spending

st.set_page_config(page_title="FinSight AI", layout="wide")
create_tables()

# ================= UI =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f0f9ff, #e0f2fe, #fdf2f8);
}
.kpi {
    background: rgba(255,255,255,0.7);
    padding: 20px;
    border-radius: 20px;
}
.card {
    background: rgba(255,255,255,0.8);
    padding: 20px;
    border-radius: 20px;
}
.stButton>button {
    background: linear-gradient(90deg,#3b82f6,#22c55e);
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 FinSight AI")

# ================= LOGIN =================
if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    menu = st.radio("Login / Register", ["Login", "Register"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if menu == "Register":
        if st.button("Register"):
            register(username, password)
            st.success("Registered! Now login")

    if menu == "Login":
        if st.button("Login"):
            user = login(username, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid credentials")

# ================= MAIN APP =================
else:
    user_id = st.session_state.user[0]

    menu = st.sidebar.radio("Menu", ["Dashboard", "Add", "Transactions", "AI Chat"])

    data = get_transactions(user_id)
    df = pd.DataFrame(data, columns=["ID","User","Amount","Category","Note","Date"])

    # ===== DASHBOARD =====
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
                st.markdown(f'<div class="card">Predicted Spend ₹ {pred}</div>', unsafe_allow_html=True)

    # ===== ADD =====
    elif menu == "Add":
        amount = st.number_input("Amount", min_value=1.0)
        category = st.selectbox("Category", ["Food","Travel","Shopping","Bills","Other"])
        note = st.text_input("Note")
        date = st.date_input("Date")

        if st.button("Add Expense"):
            add_transaction(user_id, amount, category, note, str(date))
            st.success("Added!")
            st.rerun()

    # ===== TRANSACTIONS =====
    elif menu == "Transactions":
        st.dataframe(df)

    # ===== AI CHAT =====
    elif menu == "AI Chat":
        st.subheader("🤖 Ask about your spending")

        query = st.text_input("Ask something")

        if query:
            if "total" in query.lower():
                st.write(f"You spent ₹ {df['Amount'].sum()}")
            elif "food" in query.lower():
                food = df[df["Category"]=="Food"]["Amount"].sum()
                st.write(f"You spent ₹ {food} on food")
            else:
                st.write("Try asking about total or food spending")
