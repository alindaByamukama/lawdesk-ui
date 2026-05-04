import streamlit as st
from api.cases import get_case, update_case_status
from api.notes import get_notes, add_note
from utils.session import is_authenticated, logout


STATUS_OPTIONS = ["OPEN", "ADJOURNED", "PENDING", "CLOSED"]


def show():
    if not is_authenticated():
        st.session_state.page = "login"
        st.rerun()

    case_id = st.session_state.get("selected_case")
    if not case_id:
        st.session_state.page = "cases"
        st.rerun()

    # Header
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("⚖️ LawDesk")
        st.caption("Case detail")
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign out", key="detail_signout"):
            logout()
            st.rerun()

    st.markdown("---")

    # Navigation
    if st.button("← Back to cases"):
        st.session_state.page = "cases"
        st.rerun()

    st.markdown("---")

    # Fetch case
    case = get_case(case_id)
    if not case:
        st.error("Could not load case.")
        return

    # Case header
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f"### {case.get('case_number') or 'No case number'}")
        st.markdown(f"**Client:** {case['client']['name']}")
        st.markdown(f"**Court:** {case.get('court') or '—'}")
        hearing = case.get('next_hearing_date')
        st.markdown(f"**Next hearing:** {hearing[:10] if hearing else '—'}")
    with col_b:
        current_status = case.get("status", "OPEN")
        new_status = st.selectbox(
            "Status",
            STATUS_OPTIONS,
            index=STATUS_OPTIONS.index(current_status),
            key="status_select"
        )
        if new_status != current_status:
            result = update_case_status(case_id, new_status)
            if result:
                st.success(f"Status updated to {new_status}")
                st.rerun()
            else:
                st.error("Could not update status.")

    st.markdown("---")

    # Notes section
    st.markdown("### Notes")

    # Add note form
    with st.form("add_note_form", clear_on_submit=True):
        note_body = st.text_area("Add a note", placeholder="e.g. Hearing adjourned to next month. Client informed.")
        submitted = st.form_submit_button("Save note", type="primary")

    if submitted:
        if not note_body.strip():
            st.warning("Note cannot be empty.")
        else:
            result = add_note(case_id, note_body.strip())
            if result:
                st.success("Note saved.")
                st.rerun()
            else:
                st.error("Could not save note.")

    # Notes list
    notes_data = get_notes(case_id)
    if not notes_data:
        st.info("No notes yet for this case.")
        return

    notes = notes_data.get("results", [])

    if not notes:
        st.info("No notes yet for this case.")
        return

    for note in notes:
        with st.container():
            col_body, col_date = st.columns([5, 1])
            with col_body:
                st.markdown(note["body"])
            with col_date:
                st.caption(note["created_at"][:10])
            st.divider()