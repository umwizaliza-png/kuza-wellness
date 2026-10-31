import streamlit as st
from datetime import date, timedelta, datetime
import uuid

st.set_page_config(page_title="Kuza Wellness", page_icon="🌿", layout="wide")

# DEMONSTRATION ONLY: data is held in Streamlit session state, not a shared database.
# Sample facilities, capacities and bookings are illustrative, not live availability.

FACILITIES = {
    "Kamembe Health Centre": {
        "district": "Rusizi",
        "sector": "Kamembe",
        "services": ["General consultation", "Maternal health", "Child health"],
        "daily_capacity": 30,
        "slots": {"09:00": 10, "10:00": 10, "11:30": 10},
    },
    "Rusizi District Hospital": {
        "district": "Rusizi",
        "sector": "Gihundwe",
        "services": ["General consultation", "Laboratory", "Maternal health"],
        "daily_capacity": 30,
        "slots": {"10:00": 10, "13:00": 10, "15:00": 10},
    },
    "Gihundwe Health Centre": {
        "district": "Rusizi",
        "sector": "Gihundwe",
        "services": ["General consultation", "Child health", "Immunisation"],
        "daily_capacity": 20,
        "slots": {"08:30": 7, "12:00": 7, "14:30": 6},
    },
}

SERVICES = [
    "General consultation",
    "Maternal health",
    "Child health",
    "Laboratory",
    "Immunisation",
]

TEXT = {
    "English": {
        "patient": "Patient application",
        "staff": "Facility staff dashboard",
        "district": "District",
        "sector": "Sector",
        "service": "Healthcare service",
        "date": "Appointment date",
        "search": "Find available appointments",
        "results": "Available healthcare facilities",
        "remaining": "appointments remaining",
        "choose": "View facility and choose a time",
        "book": "Confirm demo booking",
        "appointments": "My appointments (this demo session)",
        "confirmed": "Your demo appointment is confirmed",
        "emergency": "For a medical emergency, seek urgent medical care. Do not wait for an online appointment.",
        "demo": "DEMO ONLY — sample facilities, capacity and bookings. Not connected to live facilities, a shared database or SMS.",
    },
    "Kinyarwanda": {
        "patient": "Urubuga rw'umurwayi",
        "staff": "Imicungire y'ikigo nderabuzima",
        "district": "Akarere",
        "sector": "Umurenge",
        "service": "Serivisi y'ubuvuzi",
        "date": "Itariki yo kwivuza",
        "search": "Shaka ibihe byo kwivuza bihari",
        "results": "Ibigo nderabuzima bifite ibihe bihari",
        "remaining": "ibihe byo kwivuza bisigaye",
        "choose": "Reba ikigo uhitemo igihe",
        "book": "Emeza ubusabe bwo kwivuza",
        "appointments": "Ibihe byanjye byo kwivuza (muri iyi demo)",
        "confirmed": "Ubusabe bwo kwivuza bwemejwe muri iyi demo",
        "emergency": "Mu gihe cy'ubutabazi bwihutirwa, jya kwa muganga byihuse. Ntutegereze gahunda yo kuri murandasi.",
        "demo": "IGERAGEZA GUSA — ibigo, ubushobozi n'ubusabe ni ingero. Ntabwo bihujwe n'ibigo nyabyo, ububiko rusange cyangwa SMS.",
    },
}


def init_state():
    defaults = {
        "language": "English",
        "service": SERVICES[0],
        "district": "Rusizi",
        "sector": "All sectors",
        "appointment_date": date.today() + timedelta(days=1),
        "selected_facility": None,
        "selected_slot": None,
        "show_results": False,
        "demo_bookings": [],
        "daily_capacity": {
            name: data["daily_capacity"] for name, data in FACILITIES.items()
        },
        "slot_capacity": {
            name: data["slots"].copy() for name, data in FACILITIES.items()
        },
        "followup_date": date.today() + timedelta(days=30),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value.copy() if isinstance(value, (dict, list)) else value


def booked_count(facility, day=None, slot=None, service=None):
    count = 0
    for booking in st.session_state.demo_bookings:
        if booking["facility"] != facility or booking["status"] != "Confirmed":
            continue
        if day is not None and booking["date"] != str(day):
            continue
        if slot is not None and booking["slot"] != slot:
            continue
        if service is not None and booking["service"] != service:
            continue
        count += 1
    return count


def capacity_summary(facility, day, slot=None):
    daily_capacity = st.session_state.daily_capacity[facility]
    daily_booked = booked_count(facility, day=day)
    daily_remaining = max(0, daily_capacity - daily_booked)

    if slot is None:
        return daily_capacity, daily_booked, daily_remaining

    slot_capacity = st.session_state.slot_capacity[facility][slot]
    slot_booked = booked_count(facility, day=day, slot=slot)
    slot_remaining = max(0, slot_capacity - slot_booked)
    return slot_capacity, slot_booked, min(slot_remaining, daily_remaining)


def facility_remaining(facility_name, day):
    """Return the number bookable, constrained by daily and all slot capacities."""
    _, _, daily_left = capacity_summary(facility_name, day)
    slot_total_left = sum(
        capacity_summary(facility_name, day, slot)[2]
        for slot in st.session_state.slot_capacity[facility_name]
    )
    return min(daily_left, slot_total_left)


init_state()
T = TEXT[st.session_state.language]

# Header and safety notices.
st.markdown(
    """
    <div style="padding:1.1rem 1.4rem;border-radius:16px;
    background:linear-gradient(120deg,#e8f5e9,#e3f2fd);">
      <div style="font-weight:800;letter-spacing:.08em;color:#245c4a">
        KUZA WELLNESS
      </div>
      <h1 style="margin:.25rem 0;color:#173b32">
        Healthcare navigation and appointment access
      </h1>
      <p style="margin:0;color:#314d47">
        Find participating care options, understand availability and plan your next step.
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(T["demo"])
st.info(T["emergency"])

_, language_column = st.columns([3, 1])
with language_column:
    language = st.selectbox(
        "Language / Ururimi",
        ["English", "Kinyarwanda"],
        index=["English", "Kinyarwanda"].index(st.session_state.language),
    )
    st.session_state.language = language

T = TEXT[st.session_state.language]
portal = st.radio(
    "Choose your access",
    [T["patient"], T["staff"]],
    horizontal=True,
)
is_staff = portal == T["staff"]
st.divider()

if not is_staff:
    # -------------------- PATIENT APPLICATION --------------------
    st.subheader(T["patient"])
    st.write(
        "Explore sample services and facilities. Only participating facilities "
        "with published slots would appear in a live service."
    )

    with st.container(border=True):
        col_service, col_location, col_date = st.columns(3)

        with col_service:
            service = st.selectbox(
                T["service"],
                SERVICES,
                index=SERVICES.index(st.session_state.service),
            )
            st.session_state.service = service

        with col_location:
            district = st.selectbox(T["district"], ["Rusizi"], index=0)
            st.session_state.district = district
            sectors = ["All sectors", "Kamembe", "Gihundwe"]
            sector = st.selectbox(
                T["sector"],
                sectors,
                index=sectors.index(st.session_state.sector),
            )
            st.session_state.sector = sector

        with col_date:
            appointment_date = st.date_input(
                T["date"],
                value=st.session_state.appointment_date,
                min_value=date.today(),
                max_value=date.today() + timedelta(days=7),
            )
            st.session_state.appointment_date = appointment_date

        search_clicked = st.button(
            T["search"],
            type="primary",
            use_container_width=True,
        )

    if search_clicked:
        st.session_state.show_results = True
        st.session_state.selected_facility = None
        st.session_state.selected_slot = None

    # Show search results only when the user has searched or returned from details.
    if st.session_state.selected_facility is None:
        if st.session_state.show_results:
            st.subheader(T["results"])
            matches = []

            for name, facility in FACILITIES.items():
                if st.session_state.service not in facility["services"]:
                    continue
                if (
                    st.session_state.sector != "All sectors"
                    and facility["sector"] != st.session_state.sector
                ):
                    continue

                remaining = facility_remaining(
                    name, st.session_state.appointment_date
                )
                matches.append((name, facility, remaining))

            if not matches:
                st.info(
                    "No sample facilities match these filters. "
                    "Try another service or sector."
                )

            for name, facility, remaining in matches:
                with st.container(border=True):
                    card_info, card_action = st.columns([3, 1])

                    with card_info:
                        st.markdown(f"### {name}")
                        st.write(
                            f"**Location:** {facility['district']} District, "
                            f"{facility['sector']} Sector"
                        )
                        st.write(f"**Service:** {st.session_state.service}")
                        st.write(
                            f"**Daily capacity:** "
                            f"{st.session_state.daily_capacity[name]}"
                        )
                        st.write(f"**{T['remaining']}:** {remaining}")

                    with card_action:
                        if remaining == 0:
                            st.error("Fully booked")
                        elif remaining <= 5:
                            st.warning("Limited availability")
                        else:
                            st.success("More slots available")

                        choose_clicked = st.button(
                            T["choose"],
                            key=f"details_{name}",
                            disabled=remaining == 0,
                            use_container_width=True,
                        )
                        if choose_clicked:
                            st.session_state.selected_facility = name
                            st.session_state.selected_slot = None
                            st.rerun()

    # IMPORTANT: facility details are outside the "no facility selected" block.
    # This allows the selected facility to appear after the button triggers rerun.
    if st.session_state.selected_facility is not None:
        name = st.session_state.selected_facility
        facility = FACILITIES[name]

        if st.button("← Change facility"):
            st.session_state.selected_facility = None
            st.session_state.selected_slot = None
            st.rerun()

        st.divider()
        st.subheader("Facility details and appointment selection")
        st.markdown(f"### {name}")
        st.write(
            f"**Location:** {facility['district']} District, "
            f"{facility['sector']} Sector"
        )
        st.write(f"**Selected service:** {st.session_state.service}")
        st.write(
            f"**Appointment date:** "
            f"{st.session_state.appointment_date.strftime('%d %B %Y')}"
        )

        daily_capacity, daily_booked, daily_left = capacity_summary(
            name, st.session_state.appointment_date
        )
        st.metric(
            "Daily appointments remaining",
            daily_left,
            f"{daily_booked} booked of {daily_capacity}",
        )

        available_slots = []
        slot_columns = st.columns(
            len(st.session_state.slot_capacity[name])
        )

        for index, slot in enumerate(st.session_state.slot_capacity[name]):
            slot_capacity, slot_booked, slot_left = capacity_summary(
                name, st.session_state.appointment_date, slot
            )
            with slot_columns[index]:
                st.metric(
                    slot,
                    f"{slot_left} left",
                    f"{slot_booked}/{slot_capacity} booked",
                )
            if slot_left > 0 and daily_left > 0:
                available_slots.append(slot)

        if available_slots:
            chosen = st.radio(
                "Select an appointment time",
                available_slots,
                horizontal=True,
                key="patient_slot_choice",
            )
            st.session_state.selected_slot = chosen
            st.caption(
                "Selecting a time does not reserve it. Capacity is checked "
                "again when you confirm the demo booking."
            )

            with st.form("demo_booking_form"):
                patient_label = st.text_input(
                    "Patient name or demo label",
                    placeholder="Use a fictional name for this demonstration",
                )
                st.caption(
                    "Do not enter real identity numbers or sensitive medical information."
                )
                submitted = st.form_submit_button(
                    T["book"],
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                _, _, daily_left_now = capacity_summary(
                    name, st.session_state.appointment_date
                )
                _, _, slot_left_now = capacity_summary(
                    name, st.session_state.appointment_date, chosen
                )

                if daily_left_now < 1 or slot_left_now < 1:
                    st.error(
                        "This appointment time is no longer available. "
                        "Please select another time or date."
                    )
                else:
                    reference = "KZ-" + uuid.uuid4().hex[:8].upper()
                    st.session_state.demo_bookings.append(
                        {
                            "reference": reference,
                            "patient": patient_label.strip() or "Demo patient",
                            "facility": name,
                            "service": st.session_state.service,
                            "date": str(st.session_state.appointment_date),
                            "slot": chosen,
                            "status": "Confirmed",
                            "created": datetime.now().isoformat(timespec="minutes"),
                        }
                    )
                    st.session_state.last_reference = reference
                    st.session_state.selected_facility = None
                    st.session_state.selected_slot = None
                    st.session_state.show_results = True
                    st.success(f"{T['confirmed']} — {reference}")
                    st.rerun()
        else:
            st.warning(
                "No appointment times remain for this date. Try another date "
                "within the next seven days or another facility."
            )

    # Session-only bookings: there is no real patient account or sign-in.
    st.divider()
    st.subheader(T["appointments"])
    st.caption(
        "Bookings shown here were created in this browser session. "
        "This is not a private patient account."
    )

    if st.session_state.demo_bookings:
        for booking in st.session_state.demo_bookings:
            with st.container(border=True):
                st.write(f"**{booking['reference']}** — {booking['status']}")
                st.write(
                    f"{booking['facility']} | {booking['service']} | "
                    f"{booking['date']} at {booking['slot']}"
                )
                if (
                    booking["status"] == "Confirmed"
                    and st.button(
                        "Cancel demo booking",
                        key=f"cancel_{booking['reference']}",
                    )
                ):
                    booking["status"] = "Cancelled"
                    st.success(
                        "Demo booking cancelled. Its capacity has been released."
                    )
                    st.rerun()
    else:
        st.caption("No demo bookings in this session yet.")

    # Community support and follow-up planning retained from the earlier prototype.
    with st.expander("Community support and follow-up planning"):
        st.markdown("**Choose your navigation pathway**")
        mode = st.radio(
            "How would you like to navigate?",
            ["Self-navigation", "CHV-assisted navigation"],
            horizontal=True,
        )
        if mode == "CHV-assisted navigation":
            st.info(
                "A Community Health Volunteer may help explain options within "
                "their authorised role. CHVs do not replace qualified health professionals."
            )
        else:
            st.info(
                "You can explore independently and request community support if you choose."
            )

        st.checkbox(
            "I understand this is a demonstration and choose to continue "
            "using sample information.",
            key="navigation_consent",
        )
        st.markdown("#### Follow-up plan")
        st.write(
            "Only record a follow-up date already recommended by a healthcare professional."
        )
        st.selectbox(
            "Follow-up service",
            [
                "Follow-up consultation",
                "Maternal health follow-up",
                "Child health follow-up",
                "Laboratory result review",
                "Other follow-up",
            ],
        )
        st.date_input(
            "Follow-up date",
            value=st.session_state.followup_date,
            min_value=date.today(),
            key="followup_date_input",
        )
        st.text_area("Non-sensitive notes (optional)")
        st.radio(
            "Reminder preference",
            ["Show reminder in this demo", "I do not want a reminder"],
        )
        st.caption(
            "This is a session-only plan, not a real reminder or clinical record."
        )

else:
    # -------------------- FACILITY STAFF DASHBOARD --------------------
    st.subheader(T["staff"])
    st.warning(
        "DEMO STAFF AREA — this selector is not authentication. A real deployment "
        "must use secure staff accounts, role-based permissions and "
        "facility-specific access controls."
    )

    facility_name = st.selectbox(
        "Select sample facility", list(FACILITIES.keys())
    )
    selected_day = st.date_input(
        "Manage appointment date",
        value=date.today() + timedelta(days=1),
        min_value=date.today(),
        max_value=date.today() + timedelta(days=7),
        key="staff_date",
    )

    st.markdown(f"### {facility_name}")
    daily_capacity, daily_booked, daily_remaining = capacity_summary(
        facility_name, selected_day
    )

    metric_one, metric_two, metric_three = st.columns(3)
    metric_one.metric("Daily capacity", daily_capacity)
    metric_two.metric("Booked", daily_booked)
    metric_three.metric("Remaining", daily_remaining)

    with st.form("capacity_form"):
        new_daily = st.number_input(
            "Set daily capacity",
            min_value=0,
            max_value=500,
            value=int(daily_capacity),
            step=1,
        )
        st.markdown("#### Individual appointment-slot capacity")
        new_slot_capacities = {}
        slot_columns = st.columns(
            len(st.session_state.slot_capacity[facility_name])
        )

        for index, slot in enumerate(
            st.session_state.slot_capacity[facility_name]
        ):
            with slot_columns[index]:
                new_slot_capacities[slot] = st.number_input(
                    f"{slot} capacity",
                    min_value=0,
                    max_value=200,
                    value=int(
                        st.session_state.slot_capacity[facility_name][slot]
                    ),
                    step=1,
                    key=f"cap_{facility_name}_{slot}",
                )

        save_capacity = st.form_submit_button("Save demo capacity")

        if save_capacity:
            if sum(new_slot_capacities.values()) > new_daily:
                st.error(
                    "The sum of individual slot capacities cannot exceed "
                    "the daily capacity."
                )
            elif any(
                new_slot_capacities[slot]
                < booked_count(facility_name, day=selected_day, slot=slot)
                for slot in new_slot_capacities
            ):
                st.error(
                    "A slot capacity cannot be reduced below the number "
                    "already booked for this date."
                )
            elif new_daily < daily_booked:
                st.error(
                    "Daily capacity cannot be reduced below the number "
                    "already booked for this date."
                )
            else:
                st.session_state.daily_capacity[facility_name] = int(new_daily)
                st.session_state.slot_capacity[facility_name] = {
                    slot: int(capacity)
                    for slot, capacity in new_slot_capacities.items()
                }
                st.success("Demo capacity settings updated for this session.")
                st.rerun()

    st.markdown("#### Confirmed bookings for this facility and date")
    facility_bookings = [
        booking
        for booking in st.session_state.demo_bookings
        if booking["facility"] == facility_name
        and booking["date"] == str(selected_day)
        and booking["status"] == "Confirmed"
    ]

    if facility_bookings:
        for booking in facility_bookings:
            with st.container(border=True):
                st.write(
                    f"**{booking['reference']}** | {booking['patient']} | "
                    f"{booking['service']} | {booking['slot']}"
                )
                st.caption("Demo booking only. No real patient record is stored.")
    else:
        st.caption(
            "No confirmed demo bookings for this facility and date in the current session."
        )

    st.markdown("#### Capacity by appointment time")
    for slot in st.session_state.slot_capacity[facility_name]:
        slot_capacity, slot_booked, slot_remaining = capacity_summary(
            facility_name, selected_day, slot
        )
        st.write(
            f"**{slot}:** {slot_booked} booked / {slot_capacity} capacity / "
            f"{slot_remaining} remaining"
        )

st.divider()
st.caption(
    "Kuza Wellness prototype • Sample facility and capacity data only • "
    "Not a live booking service, clinical system or source of medical advice."
)
