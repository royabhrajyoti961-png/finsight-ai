import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.db import *
from utils.predictor import predict_spending

# Page setup
st.set_page_config(page_title="FinSight AI", layout="wide")

# Create DB
create_table()

# Load CSS
try:
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass

st.title("💰 FinSight AI - Smart Expense Tracker")

# Sidebar
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Add Transaction", "View Transactions"])

# Load data
data = get_transactions()
df = pd.DataFrame(data, columns=["ID", "Amount", "Category", "Note", "Date"])

# ================= DASHBOARD =================
if menu == "Dashboard":
    st.markdown("## 💰 Financial Overview")

    if not df.empty:
        total = df["Amount"].sum()
        avg = df["Amount"].mean()
        count = len(df)

        # 🔥 Premium Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("💸 Total Spending", f"₹ {round(total,2)}")
        col2.metric("📊 Avg Transaction", f"₹ {round(avg,2)}")
        col3.metric("🧾 Transactions", count)

        st.markdown("---")

        # 🔥 Charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📊 Category Split")
            fig, ax = plt.subplots()
            df.groupby("Category")["Amount"].sum().plot(
                kind="pie",
                autopct='%1.1f%%',
                ax=ax
            )
            st.pyplot(fig)

        with col2:
            st.markdown("### 📈 Spending Trend")
            df["Date"] = pd.to_datetime(df["Date"])
            trend = df.groupby("Date")["Amount"].sum()

            fig2, ax2 = plt.subplots()
            trend.plot(ax=ax2, linewidth=3)
            st.pyplot(fig2)

        st.markdown("---")

        # 🤖 AI Insight Card
        prediction = predict_spending(df)

        if prediction:
            st.markdown(f"""
            <div class="card">
                <h3>🤖 AI Insight</h3>
                <p>You may spend approximately <b>₹ {prediction}</b> in upcoming days.</p>
            </div>
            """, unsafe_allow_html=True)

            if prediction > total:
                st.error("🚨 Overspending Alert: Reduce unnecessary expenses!")

        else:
            st.info("Add more transactions to unlock AI insights")

        # 🍔 Smart Category Insight
        if "Food" in df["Category"].values:
            food_spend = df[df["Category"]=="Food"]["Amount"].sum()
            if food_spend > total * 0.4:
                st.warning("🍔 You are spending too much on food!")

    else:
        st.markdown("""
        <div class="card">
            <h3>📭 No Data Yet</h3>
            <p>Add your first transaction to see insights.</p>
        </div>
        """, unsafe_allow_html=True)

# ================= ADD =================
elif menu == "Add Transaction":
    st.markdown("## ➕ Add Transaction")

    amount = st.number_input("Amount", min_value=1.0)
    category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])
    note = st.text_input("Note")
    date = st.date_input("Date")

    st.markdown("<br>", unsafe_allow_html=True)

    # 🔥 Premium Floating Style Button
    if st.button("➕ Add Transaction", use_container_width=True):
        add_transaction(amount, category, note, str(date))
        st.success("✅ Added Successfully!")
        st.rerun()

# ================= VIEW =================
elif menu == "View Transactions":
    st.subheader("📜 All Transactions")

    if not df.empty:
        st.dataframe(df)

        delete_id = st.number_input("Enter ID to delete", min_value=1)

        if st.button("Delete", use_container_width=True):
            delete_transaction(delete_id)
            st.warning("Deleted Successfully")
            st.rerun()
    else:
        st.info("No transactions yet")
