import streamlit as st
from api.cases import get_cases, update_case_status
from utils.session import is_authenticated, logout


def show():
    if not is_authenticated():
        st.session_state.page = "login"
        st.rerun()

    # Header
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("⚖️ LawDesk")
        st.caption("Cases")
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign out", key="cases_signout"):
            logout()
            st.rerun()

    st.markdown("---")

    # Navigation
    col_nav1, col_nav2 = st.columns([1, 5])
    with col_nav1:
        if st.button("← Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown("---")

    # Filters
    with st.expander("Search & filter", expanded=True):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            search = st.text_input("Search", placeholder="Client name or case number")
        with col_b:
            status = st.selectbox("Status", ["All", "OPEN", "ADJOURNED", "PENDING", "CLOSED"])
        with col_c:
            ordering = st.selectbox("Sort by", ["Newest first", "Hearing date"])

    # Fetch cases
    params = {}
    if search:
        params["search"] = search
    if status != "All":
        params["status"] = status

    ordering_map = {
        "Newest first": "-created_at",
        "Hearing date": "next_hearing_date"
    }
    params["ordering"] = ordering_map[ordering]

    data = get_cases(**params)

    if not data:
        st.error("Could not load cases.")
        return

    cases = data.get("results", [])
    total = data.get("count", 0)

    st.markdown(f"**{total} case(s) found**")
    st.markdown("---")

    if not cases:
        st.info("No cases match your search.")
        return

    # Cases table
    for case in cases:
        col1, col2, col3, col4, col5 = st.columns([2, 3, 3, 2, 2])
        with col1:
            st.caption(case.get("case_number") or "—")
        with col2:
            st.caption(case["client"]["name"])
        with col3:
            st.caption(case.get("court") or "—")
        with col4:
            date_str = case["next_hearing_date"][:10] if case.get("next_hearing_date") else "—"
            st.caption(date_str)
        with col5:
            if st.button(case["status"], key=f"case_{case['id']}"):
                st.session_state.selected_case = case["id"]
                st.session_state.page = "case_detail"
                st.rerun()

    st.markdown("---")
    st.caption(f"Showing {len(cases)} of {total} cases")