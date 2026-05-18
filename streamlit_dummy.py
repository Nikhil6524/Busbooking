import requests
import streamlit as st

AUTH_BASE = "http://127.0.0.1:8001"
BUSINESS_BASE = "http://127.0.0.1:8000"


st.set_page_config(page_title="Auth Cookie Test", layout="centered")

st.title("AuthBackend to Backend Cookie Test")
st.caption("Logs in to AuthBackend, then calls Backend using the same session cookies.")

if "session" not in st.session_state:
    st.session_state.session = requests.Session()

session = st.session_state.session

with st.form("register_form"):
    st.subheader("Register (AuthBackend)")
    reg_name = st.text_input("Name", value="Test User")
    reg_email = st.text_input("Email", value="user@example.com", key="reg_email")
    reg_phone = st.text_input("Phone", value="9999999999")
    reg_password = st.text_input("Password", type="password", key="reg_password")
    reg_role = st.text_input("Role", value="customer")
    reg_submitted = st.form_submit_button("Register")

    if reg_submitted:
        try:
            response = session.post(
                f"{AUTH_BASE}/auth/register",
                json={
                    "name": reg_name,
                    "email": reg_email,
                    "phone": reg_phone,
                    "password": reg_password,
                    "role": reg_role
                },
                timeout=5
            )
        except requests.RequestException as exc:
            st.error(f"Registration request failed: {exc}")
        else:
            st.write("Status:", response.status_code)
            st.json(response.json() if response.content else {})

with st.form("login_form"):
    st.subheader("Login (AuthBackend)")
    email = st.text_input("Email", value="user@example.com")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        try:
            response = session.post(
                f"{AUTH_BASE}/auth/login",
                json={"email": email, "password": password},
                timeout=5
            )
        except requests.RequestException as exc:
            st.error(f"Login request failed: {exc}")
        else:
            st.write("Status:", response.status_code)
            st.json(response.json() if response.content else {})
            st.write("Cookies after login:", session.cookies.get_dict())

st.divider()

st.subheader("Call Backend /profile")
if st.button("Call /profile"):
    try:
        response = session.get(f"{BUSINESS_BASE}/profile", timeout=5)
    except requests.RequestException as exc:
        st.error(f"Profile request failed: {exc}")
    else:
        st.write("Status:", response.status_code)
        st.json(response.json() if response.content else {})

st.divider()

st.subheader("Call Backend /profile/token")
if st.button("Call /profile/token"):
    try:
        response = session.get(f"{BUSINESS_BASE}/profile/token", timeout=5)
    except requests.RequestException as exc:
        st.error(f"Token request failed: {exc}")
    else:
        st.write("Status:", response.status_code)
        st.json(response.json() if response.content else {})

st.divider()

st.subheader("Logout (AuthBackend)")
if st.button("Logout"):
    try:
        response = session.post(f"{AUTH_BASE}/auth/logout", timeout=5)
    except requests.RequestException as exc:
        st.error(f"Logout request failed: {exc}")
    else:
        st.write("Status:", response.status_code)
        st.json(response.json() if response.content else {})
        st.write("Cookies after logout:", session.cookies.get_dict())
