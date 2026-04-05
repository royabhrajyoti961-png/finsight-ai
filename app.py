import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *
from utils.predictor import predict_spending

# ================= PAGE CONFIG =================
st.set_page_config(page_title="FinSight AI", layout="wide")

create_table()

# ================= PREMIUM CSS =================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
}

/* KPI Cards */
.kpi {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    backdrop-filter: blur(10px);
}

/* Insight Card */
.card {
    background: rgba(255,255,255,0.07);
    padding: 20px;
    border-radius: 20px;
    margin-top: 10px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg,#22c55e,#4ade80);
    border-radius: 12px;
    font-weight: bold;
    color: black;
    padding: 12px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #020617;
}
</style>
""", unsafe_allow_html=True)

st.title("💰 FinSight AI")

# ================= SIDEBAR =================
menu = st.sidebar.radio("Navigation", ["Dashboard", "Add", "Transactions"])

# ================= DATA =================
data = get_transactions()
df = pd.DataFrame(data, columns=["ID", "Amount", "Category", "Note", "Date"])

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.subheader("📊 Smart Financial Dashboard")

    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])

        total = df["Amount"].sum()
        avg = df["Amount"].mean()
        max_spend = df["Amount"].max()

        # KPI CARDS
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="kpi">
                <h4>Total Spend</h4>
                <h2>₹ {round(total,2)}</h2>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="kpi">
                <h4>Avg Spend</h4>
                <h2>₹ {round(avg,2)}</h2>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="kpi">
                <h4>Max Expense</h4>
                <h2>₹ {round(max_spend,2)}</h2>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # CHARTS
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Category Distribution")
            fig = px.pie(df, names="Category", values="Amount", hole=0.5)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📈 Spending Trend")
            trend = df.groupby("Date")["Amount"].sum().reset_index()
            fig2 = px.line(trend, x="Date", y="Amount", markers=True)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # ================= AI INSIGHTS =================
        prediction = predict_spending(df)

        if prediction:
            st.markdown(f"""
            <div class="card">
                <h3>🤖 AI Prediction</h3>
                <p>At current pace, expected spend: <b>₹ {prediction}</b></p>
            </div>
            """, unsafe_allow_html=True)

            if prediction > total:
                st.error("🚨 Overspending risk detected!")

        # Smart Insights
        if "Food" in df["Category"].values:
            food = df[df["Category"]=="Food"]["Amount"].sum()
            if food > total * 0.4:
                st.warning("🍔 High food spending detected")

    else:
        st.info("No data available. Add transactions.")

# ================= ADD =================
elif menu == "Add":

    st.subheader("➕ Add Expense")

    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Amount", min_value=1.0)
        category = st.selectbox("Category", ["Food", "Travel", "Shopping", "Bills", "Other"])

    with col2:
        note = st.text_input("Note")
        date = st.date_input("Date")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🚀 Add Expense", use_container_width=True):
        add_transaction(amount, category, note, str(date))
        st.success("Added Successfully")
        st.rerun()

# ================= TRANSACTIONS =================
elif menu == "Transactions":

    st.subheader("📜 Transaction History")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        delete_id = st.number_input("Delete ID", min_value=1)

        if st.button("Delete", use_container_width=True):
            delete_transaction(delete_id)
            st.warning("Deleted")
            st.rerun()
    else:
        st.info("No transactions yet")
