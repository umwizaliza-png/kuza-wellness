import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Kuza Wellness | Patient Navigation", page_icon="🌿", layout="centered")

FACILITIES = [
    {"name":"Kamembe Health Centre","area":"Kamembe","services":["General consultation","Maternal health","Child health"],"wait":"30–45 min","slots":["09:00","11:30","14:00"]},
    {"name":"Rusizi District Hospital","area":"Rusizi","services":["General consultation","Laboratory","Maternal health"],"wait":"45–75 min","slots":["10:00","13:00","15:00"]},
    {"name":"Gihundwe Health Centre","area":"Gihundwe","services":["General consultation","Child health","Immunisation"],"wait":"20–40 min","slots":["08:30","12:00","14:30"]},
]

# The original six steps are preserved. Follow-up is added as a seventh step.
PAGES = ["Welcome","Trust & consent","Your needs","Find care","Choose an option","Next steps","Follow-up"]

if "page" not in st.session_state: st.session_state.page = PAGES[0]
if "consent" not in st.session_state: st.session_state.consent = False
if "area" not in st.session_state: st.session_state.area = "Kamembe"
if "service" not in st.session_state: st.session_state.service = "General consultation"
if "facility" not in st.session_state: st.session_state.facility = None
if "slot" not in st.session_state: st.session_state.slot = None

# New fields for the two navigation pathways and follow-up feature.
if "mode" not in st.session_state: st.session_state.mode = "Self-navigation"
if "followup_date" not in st.session_state: st.session_state.followup_date = date.today() + timedelta(days=30)
if "followup_service" not in st.session_state: st.session_state.followup_service = "Follow-up consultation"
if "followup_notes" not in st.session_state: st.session_state.followup_notes = ""
if "followup_status" not in st.session_state: st.session_state.followup_status = "Planned"
if "reminder_choice" not in st.session_state: st.session_state.reminder_choice = "Show reminder in this demo"

# Original header design and wording are retained.
st.markdown("""<div style="padding:1.2rem;border-radius:16px;background:linear-gradient(120deg,#e8f5e9,#e3f2fd)">
<div style="font-weight:800;color:#245c4a">KUZA WELLNESS</div>
<h1 style="margin:.25rem 0;color:#173b32">Healthcare navigation, with community support</h1>
<p style="margin:0;color:#314d47">A CHV-assisted prototype to help people explore care options with more confidence.</p></div>""", unsafe_allow_html=True)
st.caption("VIS Module 7 prototype • Demo data only • Not a medical service or live booking system")

nav = st.columns(len(PAGES))
for i, page in enumerate(PAGES):
    with nav[i]:
        if st.button(str(i+1), key=f"nav{i}", help=page, use_container_width=True):
            st.session_state.page = page
            st.rerun()
st.caption(f"Current step: **{st.session_state.page}**")
st.progress((PAGES.index(st.session_state.page)+1)/len(PAGES))

def go(page):
    st.session_state.page = page
    st.rerun()

def reset():
    st.session_state.page = "Welcome"
    st.session_state.consent = False
    st.session_state.area = "Kamembe"
    st.session_state.service = "General consultation"
    st.session_state.facility = None
    st.session_state.slot = None
    st.session_state.mode = "Self-navigation"
    st.session_state.followup_date = date.today() + timedelta(days=30)
    st.session_state.followup_service = "Follow-up consultation"
    st.session_state.followup_notes = ""
    st.session_state.followup_status = "Planned"
    st.session_state.reminder_choice = "Show reminder in this demo"
    st.rerun()

if st.session_state.page == "Welcome":
    st.subheader("Find your next healthcare step")
    st.write("Kuza Wellness helps you explore healthcare options with support from a Community Health Volunteer (CHV). You remain in control of whether to continue.")

    # Added choice of navigation mode without removing the original welcome content.
    st.markdown("### How would you like to use Kuza Wellness?")
    mode_choice = st.radio(
        "Choose your preferred navigation pathway:",
        ["Navigate myself", "Get help from a CHV"],
        horizontal=True,
        index=0 if st.session_state.mode == "Self-navigation" else 1,
    )
    st.session_state.mode = "Self-navigation" if mode_choice == "Navigate myself" else "CHV-assisted navigation"

    if st.session_state.mode == "Self-navigation":
        st.info("You can explore healthcare options independently. You may still ask a CHV or trusted person for help if you want.")
    else:
        st.info("A CHV can help you understand the service and navigate available options. CHVs do not replace qualified healthcare professionals.")

    st.markdown("- Understand the service before sharing information\n- Choose what basic information to provide\n- Explore sample facilities and service options\n- Review possible next steps")
    st.button("Continue to trust & consent →", type="primary", use_container_width=True, on_click=go, args=("Trust & consent",))

elif st.session_state.page == "Trust & consent":
    st.subheader("The Moment of Truth: trust & consent")
    st.warning("This is the critical component being tested: would a person trust the navigation service enough to continue?")
    with st.container(border=True):
        st.markdown("### Before you continue")
        if st.session_state.mode == "CHV-assisted navigation":
            st.write("You have chosen CHV-assisted navigation. A CHV may explain the service and help you understand options within the CHV's authorised role.")
        else:
            st.write("You have chosen self-navigation. You can explore the options independently and may request community support at any point.")
        st.write("This demo helps you explore healthcare options. It does not send information to a clinic, make real appointments, or provide medical advice.")
        st.write("In a real service, you should be told what information is collected, why it is needed, who can access it, and how it is protected. You may stop at any time.")
        st.session_state.consent = st.checkbox("I understand this is a demonstration and choose to continue using sample information.", value=st.session_state.consent)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("I do not want to continue", use_container_width=True):
                st.session_state.consent = False
                st.session_state.page = "Welcome"
                st.rerun()
        with c2:
            if st.button("I understand — continue →", type="primary", use_container_width=True):
                if st.session_state.consent: go("Your needs")
                else: st.error("Select the checkbox if you want to continue.")
    st.caption('User-test prompt: “Would you actually take this step, or would you stop here? Why?” Record their actual words.')

elif st.session_state.page == "Your needs":
    st.subheader("Tell us what would help you")
    st.write("This demo uses minimal, non-identifying information. Do not enter names, phone numbers, ID numbers, or private medical details.")
    st.session_state.area = st.selectbox("Preferred area", ["Kamembe","Gihundwe","Other / not sure"])
    st.session_state.service = st.selectbox("Type of service", ["General consultation","Maternal health","Child health","Laboratory","Immunisation"])
    st.info("A real service would require secure data handling and verified facility information.")
    st.button("Show care options →", type="primary", use_container_width=True, on_click=go, args=("Find care",))

elif st.session_state.page == "Find care":
    st.subheader("Explore healthcare options")
    st.write("All facilities, wait estimates, and appointment slots below are illustrative demo records, not live or verified data.")
    matches = [f for f in FACILITIES if st.session_state.service in f["services"] and (st.session_state.area == "Other / not sure" or f["area"] == st.session_state.area)]
    if not matches:
        matches = [f for f in FACILITIES if st.session_state.service in f["services"]]
        st.info("No exact area match in the demo; showing other sample options.")
    for f in matches:
        with st.container(border=True):
            st.markdown(f"### {f['name']}")
            st.write(f"**Area:** {f['area']}  ")
            st.write(f"**Services:** {', '.join(f['services'])}")
            st.write(f"**Illustrative wait:** {f['wait']}")
            st.write(f"**Example appointment options:** {', '.join(f['slots'])}")
            if st.button(f"Select {f['name']}", key=f"choose_{f['name']}"):
                st.session_state.facility = f["name"]
                st.session_state.slot = None
                go("Choose an option")
    st.caption("A live service would need a reliable data source and a last-updated timestamp.")

elif st.session_state.page == "Choose an option":
    st.subheader("Review your preferred option")
    f = next((x for x in FACILITIES if x["name"] == st.session_state.facility), None)
    if not f:
        st.info("Choose a sample facility first.")
        st.button("Back to options", on_click=go, args=("Find care",))
    else:
        st.markdown(f"### {f['name']}")
        st.write(f"Service: **{st.session_state.service}**")
        st.write("These example slots do not book an appointment.")
        # Original appointment time selection is preserved.
        st.session_state.slot = st.radio("Example time", f["slots"], horizontal=True)
        st.text_area("Questions you would ask the CHV (optional)", placeholder="For example: Is this facility open today?")
        st.checkbox("I understand this is not a real booking.", value=True, key="booking_ack")
        st.button("Review next steps →", type="primary", use_container_width=True, on_click=go, args=("Next steps",))

elif st.session_state.page == "Next steps":
    st.subheader("Your next step")
    if st.session_state.facility:
        st.success("You have explored a sample care option.")
        st.write(f"**Option reviewed:** {st.session_state.facility}")
        st.write(f"**Example time selected:** {st.session_state.slot or 'Not selected'}")
        st.write(f"**Navigation pathway:** {st.session_state.mode}")
    else:
        st.info("You can return to the facility list and explore sample options.")
    st.markdown("### What would happen in a real service?")
    st.markdown("1. Confirm facility details and availability with an authorised provider.\n2. Decide whether you want help with the next step.\n3. Follow the provider’s instructions if you choose to attend.\n4. A CHV may offer an agreed follow-up while respecting your privacy and choice.")
    st.warning("This prototype does not contact clinics, reserve appointments, store patient records, or replace professional medical advice.")

    # Added proposed follow-up feature; the original next-step information remains.
    st.markdown("### Keep track of your next appointment")
    st.write("If a healthcare professional or facility gives you a follow-up date, you can record it in the next step.")
    st.button("Record a follow-up date →", type="primary", use_container_width=True, on_click=go, args=("Follow-up",))
    st.button("Restart demo", use_container_width=True, on_click=reset)

else:
    st.subheader("Follow-up and next appointment")
    st.write("Record a next appointment date that a healthcare professional or facility has already recommended.")
    st.warning("Kuza does not decide when you need another appointment. Confirm the date and instructions with your healthcare provider.")
    with st.container(border=True):
        st.session_state.followup_service = st.selectbox(
            "Follow-up service",
            ["Follow-up consultation", "Maternal health follow-up", "Child health follow-up", "Laboratory result review", "Other follow-up"],
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
            st.success("Follow-up plan displayed for this demo. It is not sent to a clinic or stored in a patient record.")

    st.markdown("### Follow-up summary")
    with st.container(border=True):
        st.write(f"**Status:** {st.session_state.followup_status}")
        st.write(f"**Date:** {st.session_state.followup_date.strftime('%d %B %Y')}")
        st.write(f"**Service:** {st.session_state.followup_service}")
        st.write(f"**Facility:** {st.session_state.facility or 'Confirm with your healthcare provider'}")
        st.write(f"**Previous example time:** {st.session_state.slot or 'Not selected'}")
        st.write(f"**Reminder preference:** {st.session_state.reminder_choice}")
        if st.session_state.followup_notes:
            st.write(f"**Note:** {st.session_state.followup_notes}")
        st.caption("This information is held only in the current app session. It is not a real reminder, appointment confirmation or clinical record.")

    new_status = st.selectbox("Update demo follow-up status", ["Planned", "Attended", "Need to reschedule", "Missed"])
    if st.button("Update follow-up status"):
        st.session_state.followup_status = new_status
        st.rerun()
    st.button("Start a new navigation journey", type="primary", use_container_width=True, on_click=reset)

st.divider()
st.markdown("**Prototype purpose:** test whether the CHV explanation, consent step, and path to healthcare options are understandable and trustworthy.")
st.caption("Safety: For a medical emergency, seek urgent local medical help rather than relying on this prototype.")
