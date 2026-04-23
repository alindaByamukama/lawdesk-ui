import streamlit as st
from api.auth import refresh_token


def is_authenticated() -> bool:
    return bool(
        st.session_state.get("access") and
        st.session_state.get("refresh")
    )


def logout():
    for key in ["access", "refresh", "username", "page"]:
        st.session_state.pop(key, None)
    st.session_state.page = "landing"


def _redirect_to_login():
    st.warning("Your session has expired. Please sign in again.")
    for key in ["access", "refresh"]:
        st.session_state.pop(key, None)
    st.session_state.page = "login"
    st.rerun()


def authenticated_request(method: str, url: str, **kwargs) -> dict | None:
    """
    Makes an authenticated API request.
    Automatically retries once with a refreshed token on 401.
    Redirects to login if refresh also fails.
    
    Usage:
        data = authenticated_request("get", f"{BASE_URL}/api/cases/")
        data = authenticated_request("post", f"{BASE_URL}/api/cases/", json={...})
    """
    import requests

    access = st.session_state.get("access")
    refresh = st.session_state.get("refresh")

    if not access or not refresh:
        _redirect_to_login()
        return None

    headers = kwargs.pop("headers", {})
    headers["Authorization"] = f"Bearer {access}"

    try:
        response = getattr(requests, method)(url, headers=headers, timeout=10, **kwargs)

        if response.status_code == 401:
            # Try to refresh
            new_access = refresh_token(refresh)
            if not new_access:
                _redirect_to_login()
                return None

            # Retry with new token
            st.session_state.access = new_access
            headers["Authorization"] = f"Bearer {new_access}"
            response = getattr(requests, method)(url, headers=headers, timeout=10, **kwargs)

        if response.status_code in (200, 201):
            return response.json()

        return {"error": response.status_code, "detail": response.text}

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
        return None