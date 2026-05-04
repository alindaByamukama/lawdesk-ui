import streamlit as st
from api.clients import get_clients, create_client
from utils.session import is_authenticated, logout


def show():
    if not is_authenticated():
        st.session_state.page = "login"
        st.rerun()

    # Header
    col_title, col_logout = st.columns([4, 1])
    with col_title:
        st.title("⚖️ LawDesk")
        st.caption("Clients")
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign out", key="clients_signout"):
            logout()
            st.rerun()

    st.markdown("---")

    # Navigation
    if st.button("← Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

    st.markdown("---")

    # Create client form
    with st.expander("➕ Add new client", expanded=False):
        with st.form("create_client_form", clear_on_submit=True):
            name = st.text_input("Full name *", placeholder="e.g. B. Namusoke")
            phone = st.text_input("Phone", placeholder="e.g. 0772000000")
            email = st.text_input("Email", placeholder="e.g. namusoke@email.com")
            address = st.text_area("Address", placeholder="e.g. Kampala, Uganda")
            submitted = st.form_submit_button("Save client", type="primary")

        if submitted:
            if not name.strip():
                st.error("Client name is required.")
            else:
                result = create_client({
                    "name": name.strip(),
                    "phone": phone.strip() or None,
                    "email": email.strip() or None,
                    "address": address.strip() or None,
                })
                if result and result.get("id"):
                    st.success(f"Client '{result['name']}' created.")
                    st.rerun()
                else:
                    st.error("Could not create client. Please try again.")

    st.markdown("---")

    # Search
    search = st.text_input("Search clients", placeholder="Name, phone or email")

    # Fetch clients
    data = get_clients(search=search if search else None)
    if not data:
        st.error("Could not load clients.")
        return

    clients = data.get("results", [])
    total = data.get("count", 0)

    st.markdown(f"**{total} client(s) found**")
    st.markdown("---")

    if not clients:
        st.info("No clients found.")
        return

    for client in clients:
        col1, col2, col3, col4 = st.columns([3, 2, 3, 2])
        with col1:
            st.caption(client["name"])
        with col2:
            st.caption(client.get("phone") or "—")
        with col3:
            st.caption(client.get("email") or "—")
        with col4:
            st.caption(client.get("address") or "—")
        st.divider()