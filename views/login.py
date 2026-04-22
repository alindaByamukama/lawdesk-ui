import streamlit as st
from api.auth import login

def show():
    st.title("⚖️ LawDesk")
    st.subheader("Sign in to your account")
    st.markdown("---")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", type="primary")

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            result = login(username, password)
            if result.get("access"):
                st.session_state.access = result["access"]
                st.session_state.refresh = result["refresh"]
                st.session_state.username = username
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")

    st.markdown("---")
    col_a, col_b = st.columns([1, 3])
    with col_a:
        if st.button("← Back"):
            st.session_state.page = "landing"
            st.rerun()