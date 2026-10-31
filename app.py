import streamlit as st
from datetime import date, timedelta, datetime
import uuid

st.set_page_config(page_title="Kuza Wellness", page_icon="🌿", layout="wide")

# DEMONSTRATION ONLY: data is held in Streamlit session state, not a shared database.
# Sample facilities/capacities are illustrative and are not live facility availability.

FACILITIES = {
    "Kamembe Health Centre": {
        "district": "Rusizi", "sector": "Kamembe",
        "services": ["General consultation", "Maternal health", "Child health"],
        "daily_capacity": 30,
        "slots": {"09:00": 10, "10:00": 10, "11:30": 10},
    },
    "Rusizi District Hospital": {
        "district": "Rusizi", "sector": "Gihundwe",
        "services": ["General consultation", "Laboratory", "Maternal health"],
        "daily_capacity": 30,
        "slots": {"10:00": 10, "13:00": 10, "15:00": 10},
    },
    "Gihundwe Health Centre": {
        "district": "Rusizi", "sector": "Gihundwe",
        "services": ["General consultation", "Child health", "Immunisation"],
        "daily_capacity": 20,
        "slots": {"08:30": 7, "12:00": 7, "14:30": 6},
    },
}
SERVICES = ["General consultation", "Maternal health", "Child health", "Laboratory", "Immunisation"]

TEXT = {
    "English": {
        "tagline": "Find care. Book ahead. Make your next step clearer.",
        "patient": "Patient application", "staff": "Facility staff dashboard", "language": "Language",
        "district": "District", "sector": "Sector", "service": "Healthcare service", "date": "Appointment date",
        "search": "Find available appointments", "results": "Available healthcare facilities",
        "remaining": "appointments remaining", "capacity": "Daily capacity", "times": "Available appointment times",
        "choose": "View facility and choose a time", "book": "Confirm demo booking", "appointments": "My appointments",
        "confirmed": "Your demo appointment is confirmed", "reference": "Booking reference",
        "emergency": "For a medical emergency, seek urgent medical care. Do not wait for an online appointment.",
        "demo": "DEMO ONLY — sample facilities, capacity and bookings. Not connected to live facilities, a shared database or SMS.",
    },
    "Kinyarwanda": {
        "tagline": "Shaka serivisi z'ubuzima. Bika igihe. Menya intambwe ikurikira.",
        "patient": "Urubuga rw'umurwayi", "staff": "Imicungire y'ikigo nderabuzima", "language": "Ururimi",
        "district": "Akarere", "sector": "Umurenge", "service": "Serivisi y'ubuvuzi", "date": "Itariki yo kwivuza",
        "search": "Shaka ibihe byo kwivuza bihari", "results": "Ibigo nderabuzima bifite ibihe bihari",
        "remaining": "ibihe byo kwivuza bisigaye", "capacity": "Ubushobozi bw'umunsi", "times": "Ibihe byo kwivuza bihari",
        "choose": "Reba ikigo uhitemo igihe", "book": "Emeza ubusabe bwo kwivuza", "appointments": "Ibihe byanjye byo kwivuza",
        "confirmed": "Ubusabe bwo kwivuza bwemejwe muri iyi demo", "reference": "Nomero y'ubusabe",
        "emergency": "Mu gihe cy'ubutabazi bwihutirwa, jya kwa muganga byihuse. Ntutegereze gahunda yo kuri murandasi.",
        "demo": "IGERAGEZA GUSA — ibigo, ubushobozi n'ubusabe ni ingero. Ntabwo bihujwe n'ibigo nyabyo, ububiko rusange cyangwa SMS.",
    },
}

# State is local to the current Streamlit session. It is not shared between users.
def init_state():
    defaults = {
        "language": "English", "portal": "Patient application", "district": "Rusizi",
        "sector": "All sectors", "service": SERVICES[0], "appointment_date": date.today() + timedelta(days=1),
        "selected_facility": None, "selected_slot": None, "demo_bookings": [],
        "daily_capacity": {name: data["daily_capacity"] for name, data in FACILITIES.items()},
        "slot_capacity": {name: data["slots"].copy() for name, data in FACILITIES.items()},
        "followup_date": date.today() + timedelta(days=30), "followup_service": "Follow-up consultation",
        "followup_notes": "", "followup_status": "Planned", "reminder_choice": "Show reminder in this demo",
        "mode": "Self-navigation", "consent": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, (dict, list)) else value

init_state()
T = TEXT[st.session_state.language]

st.markdown("""<div style="padding:1.1rem 1.4rem;border-radius:16px;background:linear-gradient(120deg,#e8f5e9,#e3f2fd);">
<div style="font-weight:800;letter-spacing:.08em;color:#245c4a">KUZA WELLNESS</div>
<h1 style="margin:.25rem 0;color:#173b32">Healthcare navigation and appointment access</h1>
<p style="margin:0;color:#314d47">Find participating care options, understand availability and plan your next step.</p></div>""", unsafe_allow_html=True)
st.warning(T["demo"])
st.info(T["emergency"])

left, right = st.columns([3, 1])
with right:
    st.session_state.language = st.selectbox("Language / Ururimi", ["English", "Kinyarwanda"], index=["English", "Kinyarwanda"].index(st.session_state.language))
T = TEXT[st.session_state.language]

st.session_state.portal = st.radio("Choose your access", [T["patient"], T["staff"]], horizontal=True)
is_staff = st.session_state.portal == T["staff"]
st.divider()


def booked_count(facility, day=None, slot=None, service=None):
    total = 0
    for booking in st.session_state.demo_bookings:
        if booking["facility"] != facility or booking["status"] != "Confirmed":
            continue
        if day is not None and booking["date"] != str(day):
            continue
        if slot is not None and booking["slot"] != slot:
            continue
        if service is not None and booking["service"] != service:
            continue
        total += 1
    return total


def capacity_summary(facility, day, slot=None):
    daily = st.session_state.daily_capacity[facility]
    daily_booked = booked_count(facility, day=day)
    daily_remaining = max(0, daily - daily_booked)
    if slot is None:
        return daily, daily_booked, daily_remaining
    cap = st.session_state.slot_capacity[facility][slot]
    slot_booked = booked_count(facility, day=day, slot=slot)
    return cap, slot_booked, max(0, min(cap - slot_booked, daily_remaining))


if not is_staff:
    st.subheader(T["patient"])
    st.write("Explore sample services and facilities. Only participating facilities with published slots would appear in a live service.")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.session_state.service = st.selectbox(T["service"], SERVICES, index=SERVICES.index(st.session_state.service))
        with c2:
            st.session_state.district = st.selectbox(T["district"], ["Rusizi"], index=0)
            sectors = ["All sectors", "Kamembe", "Gihundwe"]
            st.session_state.sector = st.selectbox(T["sector"], sectors, index=sectors.index(st.session_state.sector))
        with c3:
            st.session_state.appointment_date = st.date_input(T["date"], value=st.session_state.appointment_date,
                min_value=date.today(), max_value=date.today() + timedelta(days=7))
        search = st.button(T["search"], type="primary", use_container_width=True)

    if search or st.session_state.get("show_results", False):
        st.session_state.show_results = True

    if not st.session_state.selected_facility:
        st.subheader(T["results"])

        matches = []

        for name, facility in FACILITIES.items():
            if st.session_state.service not in facility["services"]:
                continue

            if st.session_state.sector != "All sectors" and facility["sector"] != st.session_state.sector:
                continue

            _, _, remaining = capacity_summary(
                name, st.session_state.appointment_date
            )

            matches.append((name, facility, remaining))

        if not matches:
            st.info("No sample facilities match these filters. Try another service or sector.")

        for name, facility, remaining in matches:
            with st.container(border=True):
                a, b = st.columns([3, 1])

                with a:
                    st.markdown(f"### {name}")
                    st.write(f"**Location:** {facility['district']} District, {facility['sector']} Sector")
                    st.write(f"**Service:** {st.session_state.service}")
                    st.write(f"**Daily capacity:** {st.session_state.daily_capacity[name]}")
                    st.write(f"**{T['remaining']}:** {remaining}")

                with b:
                    if remaining == 0:
                        st.error("Fully booked")
                    elif remaining <= 5:
                        st.warning("Limited availability")
                    else:
                        st.success("More slots available")

                    if st.button(
                        T["choose"],
                        key=f"details_{name}",
                        disabled=remaining == 0,
                        use_container_width=True
                    ):
                        st.session_state.selected_facility = name
                        st.session_state.selected_slot = None
                        st.rerun()
    if st.session_state.selected_facility:
    if st.button("← Change facility"):
        st.session_state.selected_facility = None
        st.session_state.selected_slot = None
        st.rerun()
if st.session_state.selected_facility:
        name = st.session_state.selected_facility
        facility = FACILITIES[name]
        st.divider()
        st.subheader("Facility details and appointment selection")
        st.markdown(f"### {name}")
        st.write(f"**Location:** {facility['district']} District, {facility['sector']} Sector")
        st.write(f"**Selected service:** {st.session_state.service}")
        st.write(f"**Appointment date:** {st.session_state.appointment_date.strftime('%d %B %Y')}")
        daily_cap, daily_booked, daily_remaining = capacity_summary(name, st.session_state.appointment_date)
        st.metric("Daily appointments remaining", daily_remaining, f"{daily_booked} booked of {daily_cap}")
        available_slots = []
        cols = st.columns(len(st.session_state.slot_capacity[name]))
        for idx, slot in enumerate(st.session_state.slot_capacity[name]):
            cap, count, remaining = capacity_summary(name, st.session_state.appointment_date, slot)
            with cols[idx]:
                st.metric(slot, f"{remaining} left", f"{count}/{cap} booked")
                if remaining > 0:
                    available_slots.append(slot)
        if available_slots:
            chosen = st.radio("Select an appointment time", available_slots, horizontal=True, key="patient_slot_choice")
            st.session_state.selected_slot = chosen
            st.caption("Selecting a time does not reserve it. Capacity is checked again when you confirm the demo booking.")
            with st.form("demo_booking_form"):
                patient_label = st.text_input("Patient name or demo label", placeholder="Use a fictional name for this demonstration")
                st.caption("Do not enter real identity numbers or sensitive medical information.")
                submitted = st.form_submit_button(T["book"], type="primary", use_container_width=True)
            if submitted:
                # Re-check capacity at submission time to avoid confirming a full slot.
                _, _, daily_left = capacity_summary(name, st.session_state.appointment_date)
                _, _, slot_left = capacity_summary(name, st.session_state.appointment_date, chosen)
                if daily_left < 1 or slot_left < 1:
                    st.error("This appointment time is no longer available. Please select another time or date.")
                else:
                    reference = "KZ-" + uuid.uuid4().hex[:8].upper()
                    st.session_state.demo_bookings.append({
                        "reference": reference, "patient": patient_label.strip() or "Demo patient",
                        "facility": name, "service": st.session_state.service,
                        "date": str(st.session_state.appointment_date), "slot": chosen,
                        "status": "Confirmed", "created": datetime.now().isoformat(timespec="minutes"),
                    })
                    st.session_state.last_reference = reference
                    st.success(f"{T['confirmed']} — {reference}")
                    st.rerun()
 else:
            st.warning("No appointment times remain for this date. Try another date within the next seven days or another facility.")

    st.divider()
    st.subheader(T["appointments"])
    mine = [b for b in st.session_state.demo_bookings if b.get("patient") == st.session_state.get("last_patient_label", b.get("patient"))]
    # In this demo session, show bookings created in this browser session.
    if st.session_state.demo_bookings:
        for booking in st.session_state.demo_bookings:
            with st.container(border=True):
                st.write(f"**{booking['reference']}** — {booking['status']}")
                st.write(f"{booking['facility']} | {booking['service']} | {booking['date']} at {booking['slot']}")
                if booking["status"] == "Confirmed" and st.button("Cancel demo booking", key=f"cancel_{booking['reference']}"):
                    booking["status"] = "Cancelled"
                    st.success("Demo booking cancelled. Its capacity has been released.")
                    st.rerun()
    else:
        st.caption("No demo bookings in this session yet.")

    # Preserve the original CHV navigation and follow-up concepts.
    with st.expander("Community support and follow-up planning"):
        st.markdown("**Choose your navigation pathway**")
        mode = st.radio("How would you like to navigate?", ["Self-navigation", "CHV-assisted navigation"], horizontal=True)
        if mode == "CHV-assisted navigation":
            st.info("A Community Health Volunteer may help explain options within their authorised role. CHVs do not replace qualified health professionals.")
        else:
            st.info("You can explore independently and request community support if you choose.")
        st.checkbox("I understand this is a demonstration and choose to continue using sample information.", key="navigation_consent")
        st.markdown("#### Follow-up plan")
        st.write("Only record a follow-up date already recommended by a healthcare professional.")
        st.session_state.followup_service = st.selectbox("Follow-up service", ["Follow-up consultation", "Maternal health follow-up", "Child health follow-up", "Laboratory result review", "Other follow-up"])
        st.session_state.followup_date = st.date_input("Follow-up date", value=st.session_state.followup_date, min_value=date.today(), key="followup_date_input")
        st.session_state.followup_notes = st.text_area("Non-sensitive notes (optional)", value=st.session_state.followup_notes)
        st.session_state.reminder_choice = st.radio("Reminder preference", ["Show reminder in this demo", "I do not want a reminder"])
        st.caption("This is a session-only plan, not a real reminder or clinical record.")

else:
    st.subheader(T["staff"])
    st.warning("DEMO STAFF AREA — this selector is not authentication. A real deployment must use secure staff accounts, role-based permissions and facility-specific access controls.")
    facility_name = st.selectbox("Select sample facility", list(FACILITIES.keys()))
    facility = FACILITIES[facility_name]
    selected_day = st.date_input("Manage appointment date", value=date.today() + timedelta(days=1),
        min_value=date.today(), max_value=date.today() + timedelta(days=7), key="staff_date")
    st.markdown(f"### {facility_name}")
    daily_cap, daily_booked, daily_remaining = capacity_summary(facility_name, selected_day)
    m1, m2, m3 = st.columns(3)
    m1.metric("Daily capacity", daily_cap)
    m2.metric("Booked", daily_booked)
    m3.metric("Remaining", daily_remaining)
    with st.form("capacity_form"):
        new_daily = st.number_input("Set daily capacity", min_value=0, max_value=500, value=int(daily_cap), step=1)
        st.markdown("#### Individual appointment-slot capacity")
        new_slot_caps = {}
        slot_cols = st.columns(len(st.session_state.slot_capacity[facility_name]))
        for idx, slot in enumerate(st.session_state.slot_capacity[facility_name]):
            with slot_cols[idx]:
                new_slot_caps[slot] = st.number_input(f"{slot} capacity", min_value=0, max_value=200,
                    value=int(st.session_state.slot_capacity[facility_name][slot]), step=1, key=f"cap_{facility_name}_{slot}")
        save = st.form_submit_button("Save demo capacity")
        if save:
            if sum(new_slot_caps.values()) > new_daily:
                st.error("The sum of individual slot capacities cannot exceed the daily capacity.")
            elif any(new_slot_caps[s] < booked_count(facility_name, day=selected_day, slot=s) for s in new_slot_caps):
                st.error("A slot capacity cannot be reduced below the number already booked for this date.")
            elif new_daily < daily_booked:
                st.error("Daily capacity cannot be reduced below the number already booked for this date.")
            else:
                st.session_state.daily_capacity[facility_name] = int(new_daily)
                st.session_state.slot_capacity[facility_name] = {s: int(v) for s, v in new_slot_caps.items()}
                st.success("Demo capacity settings updated for this session.")
                st.rerun()

    st.markdown("#### Confirmed bookings for this facility and date")
    facility_bookings = [b for b in st.session_state.demo_bookings if b["facility"] == facility_name and b["date"] == str(selected_day) and b["status"] == "Confirmed"]
    if facility_bookings:
        for booking in facility_bookings:
            with st.container(border=True):
                st.write(f"**{booking['reference']}** | {booking['patient']} | {booking['service']} | {booking['slot']}")
                st.caption("Demo booking only. No real patient record is stored.")
    else:
        st.caption("No confirmed demo bookings for this facility and date in the current session.")

    st.markdown("#### Capacity by appointment time")
    for slot in st.session_state.slot_capacity[facility_name]:
        cap, count, remaining = capacity_summary(facility_name, selected_day, slot)
        st.write(f"**{slot}:** {count} booked / {cap} capacity / {remaining} remaining")

st.divider()
st.caption("Kuza Wellness prototype • Sample facility and capacity data only • Not a live booking service, clinical system or source of medical advice.")
