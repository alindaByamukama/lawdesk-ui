import streamlit as st
from datetime import datetime, timezone, date
from api.cases import get_cases
from utils.session import logout, is_authenticated


def show():
    if not is_authenticated():
        st.session_state.page = "login"
        st.rerun()

    # Header
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("⚖️ LawDesk")
        st.caption(f"Welcome, {st.session_state.get('username', '')} 👋")
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign out"):
            logout()
            st.rerun()

    st.markdown("---")

    # Fetch all cases
    data = get_cases()
    if not data:
        st.error("Could not load cases. Please try again.")
        return

    cases = data.get("results", [])

    if not cases:
        st.info("No cases yet. Head to Cases to add your first matter.")
        if st.button("Go to Cases →"):
            st.session_state.page = "cases"
            st.rerun()
        return

    # Summary counts
    open_cases = [c for c in cases if c["status"] == "OPEN"]
    adjourned = [c for c in cases if c["status"] == "ADJOURNED"]
    today = date.today()
    upcoming = [
        c for c in cases
        if c.get("next_hearing_date") and
        0 <= (date.fromisoformat(c["next_hearing_date"][:10]) - today).days <= 7
    ]

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown("**Open matters**")
        st.markdown(f"<h3 style='margin:0'>{len(open_cases)}</h3>", unsafe_allow_html=True)
    with col2:
        st.markdown("**Adjourned**")
        st.markdown(f"<h3 style='margin:0'>{len(adjourned)}</h3>", unsafe_allow_html=True)
    with col3:
        st.markdown("**Hearings this week**")
        st.markdown(f"<h3 style='margin:0'>{len(upcoming)}</h3>", unsafe_allow_html=True)

    st.markdown("---")

    # Upcoming hearings table
    st.markdown("### Upcoming hearings")
    if upcoming:
        for c in sorted(upcoming,
                        key=lambda x: x["next_hearing_date"]):
            col_a, col_b, col_c, col_d = st.columns([2, 3, 3, 2])
            with col_a:
                st.caption(c.get("case_number") or "—")
            with col_b:
                st.caption(c["client"]["name"])
            with col_c:
                st.caption(c.get("court") or "—")
            with col_d:
                date_str = c["next_hearing_date"][:10]
                st.caption(date_str)
    else:
        st.caption("No hearings in the next 7 days.")

    col_nav1, col_nav2 = st.columns(2)
    with col_nav1:
        if st.button("View all cases →"):
            st.session_state.page = "cases"
            st.rerun()
    with col_nav2:
        if st.button("View all clients →"):
            st.session_state.page = "clients"
            st.rerun()