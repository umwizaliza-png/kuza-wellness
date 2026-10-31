import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="Kuza Wellness | Healthcare Navigation",
    page_icon="🌿",
    layout="centered",
)

PAGES = ["Welcome", "Trust & consent", "Your needs", "Find care",
         "Review option", "Next steps", "Follow-up"]

FACILITIES = [
    {
        "name": "Kamembe Health Centre", "area": "Kamembe",
        "services": ["General consultation", "Maternal health", "Child health"],
        "hours": "Illustrative hours: 08:00–17:00",
        "description": "Sample option for exploring general and family health services.",
    },
    {
        "name": "Rusizi District Hospital", "area": "Rusizi",
        "services": ["General consultation", "Laboratory", "Maternal health"],
        "hours": "Illustrative hours: 08:00–17:00",
        "description": "Sample hospital option for exploring several service types.",
    },
    {
        "name": "Gihundwe Health Centre", "area": "Gihundwe",
        "services": ["General consultation", "Child health", "Immunisation"],
        "hours": "Illustrative hours: 08:00–17:00",
        "description": "Sample option for general, child health, and immunisation services.",
    },
]

DEFAULTS = {
    "page": "Welcome",
    "mode": "Self-navigation",
    "consent": False,
    "area": "Kamembe",
    "service": "General consultation",
    "facility": None,
    "followup_date": date.today() + timedelta(days=30),
    "followup_service": "Follow-up consultation",
    "followup_notes": "",
    "reminder_choice": "Show reminder in this demo",
    "followup_status": "Planned",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.markdown("""
<style>
.block-container {max-width: 900px; padding-top: 1.4rem; padding-bottom: 3rem}
.kw-hero {padding:1.4rem;border-radius:18px;background:linear-gradient(120deg,#e8f5e9,#e3f2fd);border:1px solid #d8e8e2}
.kw-brand {font-size:.8rem;letter-spacing:.13em;font-weight:800;color:#28745d}
.kw-hero h1 {font-size:2rem;line-height:1.18;margin:.4rem 0 .6rem;color:#173b32}
.kw-hero p {margin:0;color:#35544c}
.kw-small {font-size:.82rem;color:#697782}
</style>
<div class="kw-hero">
 <div class="kw-brand">KUZA WELLNESS</div>
 <h1>Healthcare navigation and continuity of care</h1>
 <p>Find care independently or with community support, and keep track of your next step.</p>
</div>
<div class="kw-small">VIS prototype · Illustrative demo data · Not a live booking or medical service</div>
""", unsafe_allow_html=True)

st.write("")
st.caption("YOUR JOURNEY")
nav = st.columns(len(PAGES))
for i, page_name in enumerate(PAGES):
    with nav[i]:
        label = f"✓ {i+1}" if PAGES.index(st.session_state.page) > i else str(i+1)
        if st.button(label, key=f"nav_{i}", help=page_name, use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

idx = PAGES.index(st.session_state.page)
st.caption(f"Step {idx+1} of {len(PAGES)} · **{st.session_state.page}**")
st.progress((idx+1)/len(PAGES))


def go(page):
    st.session_state.page = page
    st.rerun()


def reset():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    st.rerun()


if st.session_state.page == "Welcome":
    st.subheader("How would you like to use Kuza Wellness?")
    st.write("Choose the navigation option that best suits your needs.")
    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("### 📱 Navigate myself")
            st.write("For people who can access a smartphone and prefer to explore healthcare options independently.")
            if st.button("Choose self-navigation", type="primary", use_container_width=True):
                st.session_state.mode = "Self-navigation"
                go("Trust & consent")
    with right:
        with st.container(border=True):
            st.markdown("### 🤝 Get help from a CHV")
            st.write("For people who prefer personal guidance or face digital access or navigation barriers.")
            if st.button("Choose CHV assistance", use_container_width=True):
                st.session_state.mode = "CHV-assisted navigation"
                go("Trust & consent")
    st.info("Both pathways use the same healthcare navigation journey. A CHV supports navigation within their authorised role; clinical decisions remain with qualified health professionals.")
    st.caption("Future access channels could include SMS, USSD or voice support for people without smartphones. These are not part of this prototype.")

elif st.session_state.page == "Trust & consent":
    st.subheader("Trust, choice and consent")
    st.write(f"**Selected pathway:** {st.session_state.mode}")
    if st.session_state.mode == "CHV-assisted navigation":
        st.write("A recognised Community Health Volunteer (CHV) may explain the service, listen to your navigation needs and help you understand options within the CHV's authorised role.")
    else:
        st.write("You can explore the sample healthcare options independently. You may ask a CHV or another trusted person for help at any point if you prefer.")
    with st.container(border=True):
        st.markdown("**Your choices matter**")
        st.write("You can ask questions, decline to share information, change your mind or stop at any time. You should not be pressured to continue.")
        st.markdown("**Privacy in this demonstration**")
        st.write("Do not enter your name, phone number, identification number or private medical details. Your selections are used only to demonstrate this app flow.")
        st.markdown("**For a real service**")
        st.write("Personal information, reminders and any referral process would require clear consent, privacy safeguards, approved procedures and appropriate health-system collaboration.")
        st.session_state.consent = st.checkbox("I understand this is a demonstration and choose to continue using sample information.", value=st.session_state.consent)
        if st.button("Continue →", type="primary", use_container_width=True):
            if st.session_state.consent:
                go("Your needs")
            else:
                st.error("Please select the checkbox if you choose to continue.")
    if st.button("Return to welcome"):
        go("Welcome")

elif st.session_state.page == "Your needs":
    st.subheader("What healthcare service are you looking for?")
    st.write("Choose only what is needed to explore sample options.")
    st.session_state.area = st.selectbox("Preferred area", ["Kamembe", "Gihundwe", "Other / not sure"])
    st.session_state.service = st.selectbox("Type of service", [
        "General consultation", "Maternal health", "Child health", "Laboratory", "Immunisation"
    ])
    st.info("This prototype does not assess symptoms or recommend treatment. If you have urgent or severe symptoms, seek urgent medical care.")
    st.button("Find care options →", type="primary", use_container_width=True, on_click=go, args=("Find care",))

elif st.session_state.page == "Find care":
    st.subheader("Explore healthcare options")
    st.warning("Demo only: facility names, services and hours are illustrative, not verified or live.")
    matches = [f for f in FACILITIES if st.session_state.service in f["services"] and
               (st.session_state.area == "Other / not sure" or f["area"] == st.session_state.area)]
    if not matches:
        matches = [f for f in FACILITIES if st.session_state.service in f["services"]]
        st.info("No sample option matched the selected area. Other illustrative options are shown for demonstration.")
    for f in matches:
        with st.container(border=True):
            st.markdown(f"### {f['name']}")
            st.write(f"**Area:** {f['area']}")
            st.write(f"**Services shown:** {', '.join(f['services'])}")
            st.write(f"**Hours:** {f['hours']}")
            st.caption(f["description"])
            if st.button(f"Review {f['name']}", key=f"facility_{f['name']}", type="primary", use_container_width=True):
                st.session_state.facility = f["name"]
                go("Review option")
    st.caption("A live service would need verified facility information, timestamps and a process for updating inaccurate details.")

elif st.session_state.page == "Review option":
    st.subheader("Review your selected option")
    if not st.session_state.facility:
        st.info("Please select a facility first.")
        st.button("Back to options", on_click=go, args=("Find care",))
    else:
        f = next((x for x in FACILITIES if x["name"] == st.session_state.facility), None)
        st.success(f"Selected sample facility: {st.session_state.facility}")
        st.write(f"**Service:** {st.session_state.service}")
        st.write(f"**Area:** {f['area'] if f else 'Not specified'}")
        st.warning("This is not an appointment booking. Contact the facility directly to confirm services, opening hours and appointment arrangements.")
        st.button("See next steps →", type="primary", use_container_width=True, on_click=go, args=("Next steps",))

elif st.session_state.page == "Next steps":
    st.subheader("Your next step")
    st.success("You have explored a sample healthcare option.")
    st.write(f"**Navigation pathway:** {st.session_state.mode}")
    st.write(f"**Facility option:** {st.session_state.facility or 'Not selected'}")
    st.markdown("### Proposed community-to-clinic pathway")
    pathway = [
        ("1. Patient", "Identifies a need and chooses independent or CHV-assisted navigation."),
        ("2. CHV (when requested)", "Supports navigation within the CHV's authorised role; this step is optional for self-navigation."),
        ("3. Kuza Wellness", "Helps the user understand options using verified information in a future live service."),
        ("4. Health facility", "Qualified facility staff assess the patient and decide on care and any next appointment."),
        ("5. Follow-up", "The patient records the next appointment they were advised to attend and can review the plan later."),
    ]
    for heading, description in pathway:
        with st.container(border=True):
            st.markdown(f"**{heading}**")
            st.write(description)
    st.info("A next appointment should be based on advice from the treating healthcare professional or the facility—not generated by Kuza Wellness.")
    st.button("Set up a follow-up plan →", type="primary", use_container_width=True, on_click=go, args=("Follow-up",))

else:
    st.subheader("Follow-up and next appointment")
    st.write("Use this demonstration to record a next appointment date that a healthcare professional or facility has already recommended.")
    st.warning("Kuza Wellness does not determine when you need another appointment. Confirm the date and instructions with your healthcare provider.")
    with st.container(border=True):
        st.markdown("### Your follow-up plan")
        st.session_state.followup_service = st.selectbox(
            "Follow-up service",
            ["Follow-up consultation", "Maternal health follow-up", "Child health follow-up",
             "Laboratory result review", "Other follow-up"],
        )
        st.session_state.followup_date = st.date_input(
            "Next appointment date (as advised by the facility)",
            value=st.session_state.followup_date,
            min_value=date.today(),
        )
        st.session_state.followup_notes = st.text_area(
            "Non-sensitive notes or instructions (optional)",
            placeholder="Example: Bring the appointment card. Do not enter private medical details.",
        )
        st.session_state.reminder_choice = st.radio(
            "Reminder preference",
            ["Show reminder in this demo", "I do not want a reminder"],
        )
        if st.button("Save follow-up plan in this demo", type="primary", use_container_width=True):
            st.session_state.followup_status = "Planned"
            st.success("Your follow-up plan is displayed below for this demo. It is not sent to a clinic or stored in a patient record.")
    st.markdown("### Follow-up summary")
    with st.container(border=True):
        st.write(f"**Status:** {st.session_state.followup_status}")
        st.write(f"**Date:** {st.session_state.followup_date.strftime('%d %B %Y')}")
        st.write(f"**Service:** {st.session_state.followup_service}")
        st.write(f"**Facility:** {st.session_state.facility or 'Confirm with your healthcare provider'}")
        st.write(f"**Reminder:** {st.session_state.reminder_choice}")
        if st.session_state.followup_notes:
            st.write(f"**Your note:** {st.session_state.followup_notes}")
        st.caption("This summary is held only in the current app session. It is not a real reminder, appointment confirmation or clinical record.")
    status = st.selectbox("Update demo status", ["Planned", "Attended", "Need to reschedule", "Missed"])
    if st.button("Update status"):
        st.session_state.followup_status = status
        st.success("Demo status updated.")
        st.rerun()
    st.markdown("### Future development")
    st.write("A production version could offer opt-in SMS or app reminders, rescheduling guidance and facility-confirmed appointments. This would require secure storage, consent, messaging integration and participating facility workflows.")
    st.button("Start a new navigation journey", on_click=reset, type="primary", use_container_width=True)

st.divider()
st.caption("Kuza Wellness is a healthcare navigation prototype, not a medical advice, diagnosis, treatment or emergency service.")
