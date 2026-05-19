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
            try:
                st.json(response.json() if response.content else {})
            except ValueError:
                st.write(response.text)

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
            try:
                st.json(response.json() if response.content else {})
            except ValueError:
                st.write(response.text)
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
        try:
            st.json(response.json() if response.content else {})
        except ValueError:
            st.write(response.text)

st.divider()

st.subheader("Call Backend /profile/token")
if st.button("Call /profile/token"):
    try:
        response = session.get(f"{BUSINESS_BASE}/profile/token", timeout=5)
    except requests.RequestException as exc:
        st.error(f"Token request failed: {exc}")
    else:
        st.write("Status:", response.status_code)
        try:
            st.json(response.json() if response.content else {})
        except ValueError:
            st.write(response.text)

st.divider()

st.subheader("Logout (AuthBackend)")
if st.button("Logout"):
    try:
        response = session.post(f"{AUTH_BASE}/auth/logout", timeout=5)
    except requests.RequestException as exc:
        st.error(f"Logout request failed: {exc}")
    else:
        st.write("Status:", response.status_code)
        try:
            st.json(response.json() if response.content else {})
        except ValueError:
            st.write(response.text)
        st.write("Cookies after logout:", session.cookies.get_dict())

st.divider()

st.subheader("Bookings")
with st.form("create_booking_form"):
    schedule_id = st.number_input("Schedule ID", min_value=1, step=1, value=1, key="booking_schedule_id")
    seat_number = st.text_input("Seat Number", value="1", key="booking_seat_number")
    create_booking_submit = st.form_submit_button("Create Booking")

    if create_booking_submit:
        try:
            response = session.post(
                f"{BUSINESS_BASE}/bookings",
                json={
                    "schedule_id": schedule_id,
                    "seat_number": seat_number
                },
                timeout=5
            )
        except requests.RequestException as exc:
            st.error(f"Create booking request failed: {exc}")
        else:
            st.write("Status:", response.status_code)
            try:
                st.json(response.json() if response.content else {})
            except ValueError:
                st.write(response.text)

with st.form("cancel_booking_form"):
    booking_id = st.text_input("Booking ID (UUID)")
    cancel_booking_submit = st.form_submit_button("Cancel Booking")

    if cancel_booking_submit:
        if not booking_id:
            st.error("Booking ID is required")
        else:
            try:
                response = session.delete(
                    f"{BUSINESS_BASE}/bookings/{booking_id}",
                    timeout=5
                )
            except requests.RequestException as exc:
                st.error(f"Cancel booking request failed: {exc}")
            else:
                st.write("Status:", response.status_code)
                try:
                    st.json(response.json() if response.content else {})
                except ValueError:
                    st.write(response.text)

st.subheader("Booking History")
if st.button("Load Booking History"):
    try:
        response = session.get(f"{BUSINESS_BASE}/bookings/history", timeout=5)
    except requests.RequestException as exc:
        st.error(f"Booking history request failed: {exc}")
    else:
        st.write("Status:", response.status_code)
        try:
            st.json(response.json() if response.content else {})
        except ValueError:
            st.write(response.text)

st.divider()

st.subheader("Search Buses")
bus_name_query = st.text_input("Bus Name", key="bus_name_query")
bus_fuzzy = st.checkbox("Fuzzy match", value=False)
if st.button("Search"):
    if not bus_name_query:
        st.error("Bus name is required")
    else:
        try:
            response = session.get(
                f"{BUSINESS_BASE}/buses/search",
                params={"name": bus_name_query, "fuzzy": bus_fuzzy},
                timeout=5
            )
        except requests.RequestException as exc:
            st.error(f"Bus search request failed: {exc}")
        else:
            st.write("Status:", response.status_code)
            try:
                st.json(response.json() if response.content else {})
            except ValueError:
                st.write(response.text)

st.divider()

st.subheader("Admin: Add/Update Bus")
with st.form("admin_bus_form"):
    bus_mode = st.selectbox("Mode", ["Create", "Update"], key="bus_mode")
    bus_id = st.number_input("Bus ID", min_value=1, step=1, value=1, disabled=(bus_mode == "Create"))
    owner_id = st.text_input("Owner ID", disabled=(bus_mode == "Create"))
    bus_name = st.text_input("Bus Name")
    bus_number = st.text_input("Bus Number")
    bus_type = st.text_input("Bus Type")
    total_seats = st.number_input("Total Seats", min_value=1, value=40)
    operator_name = st.text_input("Operator Name")
    amenities = st.text_input("Amenities")
    bus_submit = st.form_submit_button("Save Bus")

    if bus_submit:
        payload = {
            "owner_id": owner_id or None,
            "bus_name": bus_name or None,
            "bus_number": bus_number or None,
            "bus_type": bus_type or None,
            "total_seats": total_seats,
            "operator_name": operator_name or None,
            "amenities": amenities or None
        }
        if bus_mode == "Create":
            payload["owner_id"] = None
        try:
            if bus_mode == "Update":
                if not bus_id:
                    st.error("Bus ID is required for update")
                    response = None
                else:
                    response = session.put(
                        f"{BUSINESS_BASE}/admin/update",
                        json={
                            "entity": "bus",
                            "id": bus_id,
                            "data": payload
                        },
                        timeout=5
                    )
            else:
                response = session.post(
                    f"{BUSINESS_BASE}/admin/add",
                    json={
                        "entity": "bus",
                        "data": payload
                    },
                    timeout=5
                )
        except requests.RequestException as exc:
            st.error(f"Admin bus request failed: {exc}")
        else:
            if response is not None:
                st.write("Status:", response.status_code)
                try:
                    st.json(response.json() if response.content else {})
                except ValueError:
                    st.write(response.text)

st.divider()

st.subheader("Admin: Add/Update Route")
with st.form("admin_route_form"):
    route_mode = st.selectbox("Mode", ["Create", "Update"], key="route_mode")
    route_id = st.number_input("Route ID", min_value=1, step=1, value=1, disabled=(route_mode == "Create"))
    route_bus_id = st.number_input("Bus ID", min_value=1, step=1, value=1)
    source = st.text_input("Source")
    destination = st.text_input("Destination")
    distance = st.number_input("Distance", min_value=0.0, value=0.0, step=0.1)
    duration = st.text_input("Duration")
    route_submit = st.form_submit_button("Save Route")

    if route_submit:
        payload = {
            "bus_id": route_bus_id or None,
            "source": source or None,
            "destination": destination or None,
            "distance": distance,
            "duration": duration or None
        }
        try:
            if route_mode == "Update":
                if not route_id:
                    st.error("Route ID is required for update")
                    response = None
                else:
                    response = session.put(
                        f"{BUSINESS_BASE}/admin/update",
                        json={
                            "entity": "route",
                            "id": route_id,
                            "data": payload
                        },
                        timeout=5
                    )
            else:
                response = session.post(
                    f"{BUSINESS_BASE}/admin/add",
                    json={
                        "entity": "route",
                        "data": payload
                    },
                    timeout=5
                )
        except requests.RequestException as exc:
            st.error(f"Admin route request failed: {exc}")
        else:
            if response is not None:
                st.write("Status:", response.status_code)
                try:
                    st.json(response.json() if response.content else {})
                except ValueError:
                    st.write(response.text)

st.divider()

st.subheader("Admin: Add/Update Schedule")
with st.form("admin_schedule_form"):
    schedule_mode = st.selectbox("Mode", ["Create", "Update"], key="schedule_mode")
    schedule_id = st.number_input("Schedule ID", min_value=1, step=1, value=1, disabled=(schedule_mode == "Create"))
    schedule_bus_id = st.number_input("Bus ID", min_value=1, step=1, value=1, key="schedule_bus_id")
    schedule_route_id = st.number_input("Route ID", min_value=1, step=1, value=1, key="schedule_route_id")
    departure_time = st.text_input("Departure Time (YYYY-MM-DD HH:MM:SS)")
    arrival_time = st.text_input("Arrival Time (YYYY-MM-DD HH:MM:SS)")
    journey_date = st.text_input("Journey Date (YYYY-MM-DD)")
    price = st.number_input("Price", min_value=0.0, value=0.0, step=0.5)
    available_seats = st.number_input("Available Seats", min_value=0, value=0)
    status = st.text_input("Status", value="active")
    schedule_submit = st.form_submit_button("Save Schedule")

    if schedule_submit:
        payload = {
            "bus_id": schedule_bus_id or None,
            "route_id": schedule_route_id or None,
            "departure_time": departure_time or None,
            "arrival_time": arrival_time or None,
            "journey_date": journey_date or None,
            "price": price,
            "available_seats": available_seats,
            "status": status or None
        }
        try:
            if schedule_mode == "Update":
                if not schedule_id:
                    st.error("Schedule ID is required for update")
                    response = None
                else:
                    response = session.put(
                        f"{BUSINESS_BASE}/admin/update",
                        json={
                            "entity": "schedule",
                            "id": schedule_id,
                            "data": payload
                        },
                        timeout=5
                    )
            else:
                response = session.post(
                    f"{BUSINESS_BASE}/admin/add",
                    json={
                        "entity": "schedule",
                        "data": payload
                    },
                    timeout=5
                )
        except requests.RequestException as exc:
            st.error(f"Admin schedule request failed: {exc}")
        else:
            if response is not None:
                st.write("Status:", response.status_code)
                try:
                    st.json(response.json() if response.content else {})
                except ValueError:
                    st.write(response.text)

st.divider()

st.subheader("Admin: Delete")
with st.form("admin_delete_form"):
    delete_entity = st.selectbox("Entity", ["bus", "route", "schedule"], key="delete_entity")
    delete_id = st.number_input("ID", min_value=1, step=1, value=1)
    delete_submit = st.form_submit_button("Delete")

    if delete_submit:
        if not delete_id:
            st.error("ID is required for delete")
        else:
            try:
                response = session.delete(
                    f"{BUSINESS_BASE}/admin/delete",
                    json={
                        "entity": delete_entity,
                        "id": delete_id
                    },
                    timeout=5
                )
            except requests.RequestException as exc:
                st.error(f"Admin delete request failed: {exc}")
            else:
                st.write("Status:", response.status_code)
                try:
                    st.json(response.json() if response.content else {})
                except ValueError:
                    st.write(response.text)
