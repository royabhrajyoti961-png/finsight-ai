import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db import *
from utils.predictor import predict_spending

# Setup
st.set_page_config(page_title="FinSight AI", layout="wide")
create_table()

# Load CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("💰 FinSight AI - Smart Expense Tracker")

# Sidebar
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Add Transaction", "View Transactions"])

# Fetch Data
data = get_transactions()
df = pd.DataFrame(data, columns=["ID", "Amount", "Category", "Note", "Date"])

# Dashboard
if menu == "Dashboard":
    st.subheader("📊 Dashboard")

    if not df.empty:
        total = df["Amount"].sum()
        st.metric("Total Spending", f"₹ {total}")

        # Category Chart
        st.subheader("Category Breakdown")
        fig, ax = plt.subplots()
        df.groupby("Category")["Amount"].sum().plot(kind="pie", autopct='%1.1f%%', ax=ax)
        st.pyplot(fig)

        # Prediction
        prediction = predict_spending(df)
        if prediction:
            st.warning(f"⚠️ Predicted upcoming spending: ₹ {prediction}")

            if prediction > total:
                st.error("Overspending Alert! Reduce expenses 🚨")
        else:
            st.info("Add more data for AI prediction")

# Add Transaction
elif menu == "Add Transaction":
    st.subheader("➕ Add Transaction")

    amount = st.number_input("Amount", min_value=1.0)
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
    note = st.text_input("Note")
    date = st.date_input("Date")

    if st.button("Add"):
        add_transaction(amount, category, note, str(date))
        st.success("Transaction Added!")

# View Transactions
elif menu == "View Transactions":
    st.subheader("📜 All Transactions")

    if not df.empty:
        st.dataframe(df)

        delete_id = st.number_input("Enter ID to delete")
        if st.button("Delete"):
            delete_transaction(delete_id)
            st.warning("Deleted Successfully")
    else:
        st.info("No transactions yet")
