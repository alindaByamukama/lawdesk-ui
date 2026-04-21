import streamlit as st

def show():
    st.set_page_config(page_title="LawDesk", page_icon="⚖️", layout="centered")

    st.title("⚖️ LawDesk")
    st.subheader("Case management for small legal practices in Uganda.")

    st.markdown("""
    ---
    Legal work runs on dates, notes, and files.  
    Most practitioners track these across notebooks, WhatsApp messages, and memory.  
    LawDesk brings them into one place.
    """)

    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.markdown("**Track**")
        st.markdown("### Cases & Clients")
    with col2:
        st.markdown("**Never miss**")
        st.markdown("### A hearing date")
    with col3:
        st.markdown("**Find anything**")
        st.markdown("### In seconds")

    st.markdown("---")
    st.markdown("### What you can do")

    st.markdown("""
    - **Manage clients** — store contact details, link to their matters  
    - **Track cases** — court, status, next hearing date at a glance  
    - **Add notes** — quick notes or detailed records per case  
    - **Filter and search** — find any case by client name, status, or date  
    """)

    st.markdown("---")

    col_a, col_b = st.columns([1, 3])
    with col_a:
        if st.button("Get Started →", type="primary"):
            st.session_state.page = "login"
            st.rerun()
    with col_b:
        st.caption("Already have an account? The button above takes you to login.")