import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *
from utils.predictor import predict_future, generate_insights
from utils.ai_advisor import generate_ai_advice

# ================= CONFIG =================
st.set_page_config(page_title="FinSight SaaS", layout="wide")
create_tables()

# ================= THEME SYSTEM =================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# ================= 🍎 APPLE UI =================
if st.session_state.theme == "light":
    bg = "linear-gradient(135deg, #f9fafb, #eef2ff, #fdf2f8)"
    card = "rgba(255,255,255,0.7)"
    text = "#111827"
else:
    bg = "linear-gradient(135deg, #0f172a, #1e293b)"
    card = "rgba(30,41,59,0.7)"
    text = "#f1f5f9"

st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
* {{
    font-family: 'Poppins', sans-serif !important;
}}

.stApp {{
    background: {bg};
    color: {text};
}}

/* Glass Card */
.card {{
    background: {card};
    backdrop-filter: blur(20px);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.08);
    margin-bottom: 15px;
    transition: 0.3s;
}}

.card:hover {{
    transform: translateY(-6px);
}}

/* KPI */
.kpi-title {{
    font-size: 14px;
    opacity: 0.7;
}}

.kpi-value {{
    font-size: 26px;
    font-weight: 600;
}}

/* Buttons */
.stButton>button {{
    border-radius: 12px;
    padding: 10px 16px;
    border: none;
    background: {"#111827" if st.session_state.theme=="light" else "#e2e8f0"};
    color: {"white" if st.session_state.theme=="light" else "#111827"};
    transition: 0.3s;
}}

.stButton>button:hover {{
    transform: scale(1.05);
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: {card};
    backdrop-filter: blur(20px);
}}

/* Fade Animation */
.fade {{
    animation: fadeIn 0.7s ease-in-out;
}}

@keyframes fadeIn {{
    from {{opacity: 0;}}
    to {{opacity: 1;}}
}}

/* ===== FOOTER ===== */
.footer {{
    position: fixed;
    bottom: 12px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 13px;
    color: #6b7280;
    background: {card};
    backdrop-filter: blur(12px);
    padding: 8px 18px;
    border-radius: 14px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    z-index: 999;
}}

</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= AUTH =================
if st.session_state.user is None:

    st.markdown("<h2 class='fade'> ₹ FinSight SaaS Transaction App </h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.user = user
                st.success("Welcome ")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Account created ")
            else:
                st.error("Username exists")

# ================= MAIN =================
else:
    user_id = st.session_state.user[0]

    st.sidebar.button(" Toggle Theme", on_click=toggle_theme)

    st.sidebar.title("Navigation")
    menu = st.sidebar.radio("", ["₹ Dashboard", "₹ Add Expense", "₹ Transactions", "₹ AI Advisor"])

    data = get_expenses(user_id)
    df = pd.DataFrame(data, columns=["ID","User","Amount","Category","Note","Date"])

    st.markdown("<h2 class='fade'>₹ Dashboard</h2>", unsafe_allow_html=True)

    # ================= DASHBOARD =================
    if menu == "₹ Dashboard":

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

            fig = px.pie(df, names="Category", values="Amount")
            st.plotly_chart(fig, use_container_width=True)

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

            st.subheader(" Insights")
            for insight in generate_insights(df):
                st.markdown(f"<div class='card fade'>{insight}</div>", unsafe_allow_html=True)

        else:
            st.info("No expenses yet")

    # ================= ADD =================
    elif menu == "₹ Add Expense":

        st.markdown("<h3 class='fade'>₹ Quickly Add Your Expanses Here </h3>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        amount = col1.number_input("Amount", min_value=1.0)
        category = col2.selectbox("Category", ["Food","Travel","Shopping","Bills","Other"])
        note = col3.text_input("Note")

        date = st.date_input("Date")

        if st.button(" ₹ Add Expense"):
            add_expense(user_id, amount, category, note, str(date))
            st.success("Added ")
            st.rerun()

    # ================= TRANSACTIONS =================
    elif menu == "₹ Transactions":

        st.markdown("<h3 class='fade'>₹ Your Transactions & Expanses </h3>", unsafe_allow_html=True)

        st.dataframe(df, use_container_width=True)

        delete_id = st.number_input("Delete ID", min_value=1)

        if st.button("Delete"):
            delete_expense(delete_id)
            st.warning("Deleted")
            st.rerun()

    # ================= AI =================
    elif menu == "₹ AI Advisor":

        st.markdown("<h3 class='fade'> AI Financial Advisor</h3>", unsafe_allow_html=True)

        question = st.text_input("Ask AI")

        if st.button("Ask AI"):
            response = generate_ai_advice(df, question)
            st.markdown(f"<div class='card fade'>{response}</div>", unsafe_allow_html=True)

        st.subheader(" Automatic Advice")
        auto = generate_ai_advice(df)
        st.markdown(f"<div class='card fade'>{auto}</div>", unsafe_allow_html=True)

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

# ================= FOOTER =================
st.markdown("""
<div class="footer">
    Developed with ❤️ by <b>ABHRAJYOTI ROY</b>
</div>
""", unsafe_allow_html=True)
