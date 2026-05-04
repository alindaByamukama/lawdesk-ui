import streamlit as st
from views import landing, login, dashboard, cases, case_detail

if "page" not in st.session_state:
    st.session_state.page = "landing"

if st.session_state.page == "landing":
    landing.show()
elif st.session_state.page == "login":
    login.show()
elif st.session_state.page == "dashboard":
    dashboard.show()
elif st.session_state.page == "cases":
    cases.show()
elif st.session_state.page == "case_detail":
    case_detail.show()