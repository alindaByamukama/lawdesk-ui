import streamlit as st
from views import landing, login, dashboard

if "page" not in st.session_state:
    st.session_state.page = "landing"

if st.session_state.page == "landing":
    landing.show()
elif st.session_state.page == "login":
    login.show()
elif st.session_state.page == "dashboard":
    dashboard.show()