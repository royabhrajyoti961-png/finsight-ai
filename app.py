import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db import *
from utils.predictor import predict_spending

# Page setup
st.set_page_config(page_title="FinSight AI", layout="wide")

# Create DB automatically
create_table()

# Load CSS safely
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass  # prevents crash if CSS missing

st.title("💰 FinSight AI - Smart Expense Tracker")

# Sidebar
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Add Transaction", "View Transactions"])

# Load Data
data = get_transactions()
df = pd.DataFrame(data, columns=["ID", "Amount", "Category", "Note", "Date"])

# ================= DASHBOARD =================
if menu == "Dashboard":
    st.subheader("📊 Dashboard")

    if not df.empty:
        total = df["Amount"].sum()
        st.metric("Total Spending", f"₹ {total}")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Category Breakdown")
            fig, ax = plt.subplots()
            df.groupby("Category")["Amount"].sum().plot(
                kind="pie", autopct='%1.1f%%', ax=ax
            )
            st.pyplot(fig)

        with col2:
            st.subheader("Spending Trend")
            df["Date"] = pd.to_datetime(df["Date"])
            trend = df.groupby("Date")["Amount"].sum()

            fig2, ax2 = plt.subplots()
            trend.plot(ax=ax2)
            st.pyplot(fig2)

        # AI Prediction
        prediction = predict_spending(df)
        if prediction:
            st.warning(f"⚠️ Predicted upcoming spending: ₹ {prediction}")

            if prediction > total:
                st.error("🚨 Overspending Alert! Try reducing expenses")
        else:
            st.info("Add more data for AI prediction")

    else:
        st.info("No data yet. Add transactions!")

# ================= ADD =================
elif menu == "Add Transaction":
    st.subheader("➕ Add Transaction")

    amount = st.number_input("Amount", min_value=1.0)
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
    note = st.text_input("Note")
    date = st.date_input("Date")

    if st.button("Add Transaction"):
        add_transaction(amount, category, note, str(date))
        st.success("✅ Transaction Added!")
        st.rerun()

# ================= VIEW =================
elif menu == "View Transactions":
    st.subheader("📜 All Transactions")

    if not df.empty:
        st.dataframe(df)

        delete_id = st.number_input("Enter ID to delete", min_value=1)

        if st.button("Delete"):
            delete_transaction(delete_id)
            st.warning("Deleted Successfully")
            st.rerun()
    else:
        st.info("No transactions yet")
