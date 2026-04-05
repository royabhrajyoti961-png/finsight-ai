import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *
from utils.predictor import predict_spending

# ================= CONFIG =================
st.set_page_config(page_title="FinSight AI", layout="wide")
create_table()

# ================= ULTRA PREMIUM CSS =================
st.markdown("""
<style>

/* GLOBAL */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: light-pink ;
}

/* HEADER */
.header {
    font-size: 28px;
    font-weight: bold;
    padding: 10px 0;
}

/* KPI CARDS */
.kpi {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 18px;
    backdrop-filter: blur(12px);
    text-align: center;
    transition: 0.3s;
}

.kpi:hover {
    transform: translateY(-5px);
    box-shadow: 0 0 20px rgba(34,197,94,0.4);
}

/* GLASS CARD */
.card {
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 18px;
    backdrop-filter: blur(10px);
    margin-top: 10px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg,#22c55e,#4ade80);
    color: black;
    font-weight: bold;
    border-radius: 12px;
    padding: 12px;
    border: none;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 15px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.markdown('<div class="header">💰 FinSight AI Dashboard</div>', unsafe_allow_html=True)

# ================= NAV =================
menu = st.sidebar.radio("Navigation", ["🏠 Dashboard", "➕ Add Expense", "📜 Transactions"])

# ================= DATA =================
data = get_transactions()
df = pd.DataFrame(data, columns=["ID", "Amount", "Category", "Note", "Date"])

# ================= DASHBOARD =================
if menu == "🏠 Dashboard":

    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])

        total = df["Amount"].sum()
        avg = df["Amount"].mean()
        max_spend = df["Amount"].max()

        # KPI ROW
        c1, c2, c3 = st.columns(3)

        c1.markdown(f'<div class="kpi"><h4>Total Spend</h4><h2>₹ {total:.2f}</h2></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="kpi"><h4>Avg Spend</h4><h2>₹ {avg:.2f}</h2></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="kpi"><h4>Max Expense</h4><h2>₹ {max_spend:.2f}</h2></div>', unsafe_allow_html=True)

        st.markdown("---")

        # CHARTS + INSIGHTS LAYOUT
        col1, col2 = st.columns([2,1])

        with col1:
            st.subheader("📊 Financial Analytics")

            chart1 = px.pie(df, names="Category", values="Amount", hole=0.6)
            st.plotly_chart(chart1, use_container_width=True)

            trend = df.groupby("Date")["Amount"].sum().reset_index()
            chart2 = px.line(trend, x="Date", y="Amount", markers=True)
            st.plotly_chart(chart2, use_container_width=True)

        with col2:
            st.subheader("🤖 AI Insights")

            prediction = predict_spending(df)

            if prediction:
                st.markdown(f"""
                <div class="card">
                    <h4>Future Prediction</h4>
                    <p>₹ {prediction}</p>
                </div>
                """, unsafe_allow_html=True)

                if prediction > total:
                    st.error("🚨 Overspending Risk")

            # Smart insight
            if "Food" in df["Category"].values:
                food = df[df["Category"]=="Food"]["Amount"].sum()
                if food > total * 0.4:
                    st.warning("🍔 High food spending")

    else:
        st.info("No transactions yet")

# ================= ADD =================
elif menu == "➕ Add Expense":

    st.subheader("Add New Expense")

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
        st.success("Added!")
        st.rerun()

# ================= TRANSACTIONS =================
elif menu == "📜 Transactions":

    st.subheader("Transaction History")

    if not df.empty:
        st.dataframe(df, use_container_width=True)

        delete_id = st.number_input("Enter ID to delete", min_value=1)

        if st.button("Delete", use_container_width=True):
            delete_transaction(delete_id)
            st.warning("Deleted")
            st.rerun()
    else:
        st.info("No data")
