# ================= MAIN =================
else:
    user_id = st.session_state.user[0]

    # 🌗 Theme Toggle
    st.sidebar.button("🌗 Toggle Theme", on_click=toggle_theme)

    st.sidebar.title("Navigation")
    # Define options once to ensure consistency
    menu_options = ["Dashboard", "Add Expense", "Transactions", "AI Advisor"]
    menu = st.sidebar.radio("", menu_options)

    # Fetch fresh data every rerun
    data = get_expenses(user_id)
    df = pd.DataFrame(data, columns=["ID","User","Amount","Category","Note","Date"])

    # ================= DASHBOARD =================
    if menu == "Dashboard":
        st.markdown("<h2 class='fade'>📊 Dashboard</h2>", unsafe_allow_html=True)
        # ... (rest of your dashboard code)

    # ================= ADD =================
    elif menu == "Add Expense":
        st.markdown("<h3 class='fade'>⚡ Quick Add</h3>", unsafe_allow_html=True)
        # ... (rest of your add code)

    # ================= TRANSACTIONS =================
    # FIXED: Removed the extra spaces in the string comparison
    elif menu == "Transactions": 
        st.markdown("<h3 class='fade'>📋 Transactions</h3>", unsafe_allow_html=True)

        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            delete_id = st.number_input("Enter ID to Delete", min_value=1)
            if st.button("Delete"):
                delete_expense(delete_id)
                st.warning(f"Transaction {delete_id} deleted!")
                st.rerun()
        else:
            st.info("No transaction history found.")

    # ================= AI ADVISOR =================
    elif menu == "AI Advisor":
        # ... (rest of your AI Advisor code)
