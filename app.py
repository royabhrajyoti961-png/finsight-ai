import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *
from utils.predictor import predict_future, generate_insights
from utils.ai_advisor import generate_ai_advice

# ================= CONFIG =================
st.set_page_config(page_title="FinSight SaaS", layout="wide")
create_tables()

# ================= THEME =================
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# ================= COLORS =================
if st.session_state.theme == "light":
    bg = "linear-gradient(135deg, #f9fafb, #eef2ff, #fdf2f8)"
    card = "rgba(255,255,255,0.7)"
    text = "#111827"
    hover = "rgba(0,0,0,0.05)"
else:
    bg = "linear-gradient(135deg, #0f172a, #1e293b)"
    card = "rgba(30,41,59,0.7)"
    text = "#f1f5f9"
    hover = "rgba(255,255,255,0.1)"

# ================= SVG ICONS =================
dashboard_icon = """<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/>
<rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>"""

add_icon = """<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>"""

trans_icon = """<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
<path d="M21 12H3"/><path d="M7 16l-4-4 4-4"/></svg>"""

ai_icon = """<svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
<circle cx="12" cy="12" r="10"/><path d="M8 15h8"/></svg>"""

# ================= UI =================
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

section[data-testid="stSidebar"] {{
    background: {card};
    backdrop-filter: blur(20px);
}}

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

.stButton>button {{
    border-radius: 12px;
    padding: 10px 16px;
    border: none;
    background: {"#111827" if st.session_state.theme=="light" else "#e2e8f0"};
    color: {"white" if st.session_state.theme=="light" else "#111827"};
}}

.fade {{
    animation: fadeIn 0.6s ease-in-out;
}}

@keyframes fadeIn {{
    from {{opacity: 0;}}
    to {{opacity: 1;}}
}}

/* FOOTER */
.footer {{
    position: fixed;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    font-size: 13px;
    color: #6b7280;
    background: {card};
    backdrop-filter: blur(10px);
    padding: 8px 16px;
    border-radius: 12px;
}}

</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= AUTH =================
if st.session_state.user is None:

    st.markdown("<h2>💼 FinSight SaaS</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            user = login_user(u, p)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        u = st.text_input("New Username")
        p = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register_user(u, p):
                st.success("Account created")
            else:
                st.error("Username exists")

# ================= MAIN =================
else:
    user_id = st.session_state.user[0]

    st.sidebar.button("🌗 Theme", on_click=toggle_theme)
    st.sidebar.markdown("### 💼 FinSight")

    menu = st.sidebar.radio("Navigation", ["Dashboard", "Add Expense", "Transactions", "AI Advisor"])

    data = get_expenses(user_id)
    df = pd.DataFrame(data, columns=["ID","User","Amount","Category","Note","Date"])

    # ================= HEADINGS WITH ICON =================
    if menu == "Dashboard":
        st.markdown(f"{dashboard_icon} <h2>Dashboard</h2>", unsafe_allow_html=True)

    elif menu == "Add Expense":
        st.markdown(f"{add_icon} <h2>Add Expense</h2>", unsafe_allow_html=True)

    elif menu == "Transactions":
        st.markdown(f"{trans_icon} <h2>Transactions</h2>", unsafe_allow_html=True)

    elif menu == "AI Advisor":
        st.markdown(f"{ai_icon} <h2>AI Advisor</h2>", unsafe_allow_html=True)

    # ================= DASHBOARD =================
    if menu == "Dashboard":
        if not df.empty:
            st.plotly_chart(px.pie(df, names="Category", values="Amount"), use_container_width=True)

            daily, future = predict_future(df)
            if daily is not None:
                fig = px.line(daily, x="Date", y="Amount")
                if future is not None:
                    fig.add_scatter(x=future["Date"], y=future["Predicted"], name="Prediction")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No expenses yet")

    # ================= ADD =================
    elif menu == "Add Expense":
        amt = st.number_input("Amount", min_value=1.0)
        cat = st.selectbox("Category", ["Food","Travel","Shopping","Bills","Other"])
        note = st.text_input("Note")
        date = st.date_input("Date")

        if st.button("Add"):
            add_expense(user_id, amt, cat, note, str(date))
            st.success("Added")
            st.rerun()

    # ================= TRANSACTIONS =================
    elif menu == "Transactions":
        st.dataframe(df)

    # ================= AI =================
    elif menu == "AI Advisor":
        q = st.text_input("Ask AI")
        if st.button("Ask"):
            st.write(generate_ai_advice(df, q))

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

# ================= FOOTER =================
st.markdown("""
<div class="footer">
Developed with ❤️ by <b>ABHRAJYOTI ROY</b>
</div>
""", unsafe_allow_html=True)
