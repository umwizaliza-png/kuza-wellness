import streamlit as st

st.set_page_config(
    page_title="Kuza Wellness | Patient Navigation",
    page_icon="🌿",
    layout="centered",
)

PAGES = [
    "Welcome",
    "Trust & consent",
    "Your needs",
    "Find care",
    "Choose an option",
    "Next steps",
]

FACILITIES = [
    {
        "name": "Kamembe Health Centre",
        "area": "Kamembe",
        "services": ["General consultation", "Maternal health", "Child health"],
        "wait": "30–45 min",
        "slots": ["09:00", "11:30", "14:00"],
        "description": "Sample option for exploring general and family health services.",
    },
    {
        "name": "Rusizi District Hospital",
        "area": "Rusizi",
        "services": ["General consultation", "Laboratory", "Maternal health"],
        "wait": "45–75 min",
        "slots": ["10:00", "13:00", "15:00"],
        "description": "Sample hospital option for exploring several service types.",
    },
    {
        "name": "Gihundwe Health Centre",
        "area": "Gihundwe",
        "services": ["General consultation", "Child health", "Immunisation"],
        "wait": "20–40 min",
        "slots": ["08:30", "12:00", "14:30"],
        "description": "Sample option for general, child health, and immunisation services.",
    },
]

DEFAULTS = {
    "page": "Welcome",
    "consent": False,
    "area": "Kamembe",
    "service": "General consultation",
    "facility": None,
    "slot": None,
}

for key, default in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown(
    """
    <style>
    .block-container {max-width: 900px; padding-top: 1.5rem; padding-bottom: 3rem}
    .kw-hero {
        padding: 1.5rem; border-radius: 18px;
        background: linear-gradient(120deg,#e8f5e9,#e3f2fd);
        border: 1px solid #d8e8e2;
    }
    .kw-brand {font-size:.82rem; letter-spacing:.13em; font-weight:800; color:#28745d}
    .kw-hero h1 {font-size:2.05rem; line-height:1.18; margin:.45rem 0 .65rem; color:#173b32}
    .kw-hero p {margin:0; color:#35544c}
    .kw-small {font-size:.82rem; color:#697782}
    div.stButton>button {border-radius:10px; min-height:2.6rem}
    </style>
    <div class="kw-hero">
      <div class="kw-brand">KUZA WELLNESS</div>
      <h1>Healthcare navigation, with community support</h1>
      <p>Explore care options with guidance from a Community Health Volunteer (CHV).</p>
    </div>
    <div class="kw-small">VIS prototype · Illustrative demo data · Not a live booking or medical service</div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.caption("YOUR JOURNEY")
nav = st.columns(6)
for i, page_name in enumerate(PAGES):
    with nav[i]:
        label = f"✓ {i + 1}" if PAGES.index(st.session_state.page) > i else str(i + 1)
        if st.button(label, key=f"nav{i}", help=page_name, use_container_width=True):
            st.session_state.page = page_name
            st.rerun()

idx = PAGES.index(st.session_state.page)
st.caption(f"Step {idx + 1} of {len(PAGES)} · **{st.session_state.page}**")
st.progress((idx + 1) / len(PAGES))


def go(page_name):
    st.session_state.page = page_name
    st.rerun()


def reset():
    for key, value in DEFAULTS.items():
        st.session_state[key] = value
    st.rerun()


if st.session_state.page == "Welcome":
    st.subheader("Find your next healthcare step")
    st.write(
        "Finding care can be confusing when you are unsure which facility offers "
        "the service you need or what to do next. Kuza Wellness is being designed "
        "to help people explore options with support from a trusted community health volunteer."
    )
    st.info(
        "A CHV can explain the service and help you navigate options within the CHV's "
        "authorised role. A CHV does not diagnose conditions or replace a qualified healthcare professional."
    )
    with st.container(border=True):
        st.markdown("**What you can do in this demo**")
        st.markdown(
            "- Understand the service before deciding whether to continue\n"
            "- Choose a preferred area and service type\n"
            "- Explore sample facility information\n"
            "- See how a proposed community-to-facility pathway could work\n"
            "- Review a possible next step without making a real booking"
        )
    st.button(
        "Continue to trust & consent →",
        type="primary",
        use_container_width=True,
        on_click=go,
        args=("Trust & consent",),
    )

elif st.session_state.page == "Trust & consent":
    st.subheader("The Moment of Truth: trust & consent")
    st.warning(
        "Critical design question: will a person trust the CHV-assisted service enough to continue?"
    )
    with st.container(border=True):
        st.markdown("### Before you decide")
        st.write(
            "The CHV's proposed role is to explain Kuza Wellness, listen to your navigation "
            "needs, and help you understand available options. Clinical assessment and "
            "treatment remain the responsibility of qualified health professionals."
        )
        st.markdown("**Your choices matter**")
        st.write(
            "You can ask questions, decline to share information, choose not to use CHV "
            "support, or stop at any time. You should not be pressured to continue."
        )
        st.markdown("**In this demonstration**")
        st.write(
            "You do not need to provide your name, phone number, ID number, or private "
            "medical details. Your selections demonstrate the app flow; they are not sent to a clinic."
        )
        st.markdown("**For a real service**")
        st.write(
            "Before collecting personal information, Kuza Wellness would need to explain "
            "what is collected, why it is needed, who can access it, and how it is protected. "
            "The service would also need approved procedures agreed with the relevant CHW "
            "programme and receiving health facilities."
        )
        st.session_state.consent = st.checkbox(
            "I understand this is a demonstration and choose to continue using sample information.",
            value=st.session_state.consent,
            key="consent_checkbox",
        )
        a, b = st.columns(2)
        with a:
            if st.button("I do not want to continue", use_container_width=True):
                st.session_state.consent = False
                st.session_state.page = "Welcome"
                st.rerun()
        with b:
            if st.button(
                "I understand — continue →",
                type="primary",
                use_container_width=True,
            ):
                if st.session_state.consent:
                    go("Your needs")
                else:
                    st.error("Please select the checkbox if you choose to continue.")
    st.caption(
        "Testing prompt: ask a participant, “Would you feel comfortable asking a CHV "
        "for help with this process? Why or why not?” Record their actual response."
    )

elif st.session_state.page == "Your needs":
    st.subheader("Tell us what would help you")
    st.write(
        "Choose only what is needed to explore options. Do not enter identifying "
        "or private medical information."
    )
    st.session_state.area = st.selectbox(
        "Preferred area",
        ["Kamembe", "Gihundwe", "Other / not sure"],
        index=["Kamembe", "Gihundwe", "Other / not sure"].index(st.session_state.area),
    )
    st.session_state.service = st.selectbox(
        "Type of service",
        [
            "General consultation",
            "Maternal health",
            "Child health",
            "Laboratory",
            "Immunisation",
        ],
        index=[
            "General consultation",
            "Maternal health",
            "Child health",
            "Laboratory",
            "Immunisation",
        ].index(st.session_state.service),
    )
    st.info(
        "A real service would require secure data handling, verified facility information, "
        "and appropriate consent procedures."
    )
    st.button(
        "Show care options →",
        type="primary",
        use_container_width=True,
        on_click=go,
        args=("Find care",),
    )

elif st.session_state.page == "Find care":
    st.subheader("Explore healthcare options")
    st.info(
        "Demo only: facility names, services, wait estimates, and time slots are illustrative, not live or verified."
    )
    matches = [
        facility
        for facility in FACILITIES
        if st.session_state.service in facility["services"]
        and (
            st.session_state.area == "Other / not sure"
            or facility["area"] == st.session_state.area
        )
    ]
    if not matches:
        matches = [
            facility
            for facility in FACILITIES
            if st.session_state.service in facility["services"]
        ]
        st.warning(
            "No sample option matched that exact area. Other illustrative options "
            "are shown so you can test the flow."
        )

    st.caption(f"{len(matches)} sample option(s) for: {st.session_state.service}")
    for facility in matches:
        with st.container(border=True):
            st.markdown(f"### {facility['name']}")
            st.caption(facility["description"])
            a, b = st.columns(2)
            with a:
                st.markdown("**Area**")
                st.write(facility["area"])
                st.markdown("**Services in this demo**")
                st.write(", ".join(facility["services"]))
            with b:
                st.markdown("**Illustrative wait**")
                st.write(facility["wait"])
                st.markdown("**Example times**")
                st.write(", ".join(facility["slots"]))
            if st.button(
                "Review this option →",
                key=f"select_{facility['name']}",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.facility = facility["name"]
                st.session_state.slot = None
                go("Choose an option")

    st.caption(
        "A live service would need verified provider data, clear timestamps, "
        "and a process for correcting outdated information."
    )

elif st.session_state.page == "Choose an option":
    st.subheader("Review your preferred option")
    facility = next(
        (item for item in FACILITIES if item["name"] == st.session_state.facility),
        None,
    )
    if not facility:
        st.info("Choose a sample facility before reviewing an option.")
        st.button("Back to care options", on_click=go, args=("Find care",))
    else:
        with st.container(border=True):
            st.markdown(f"### {facility['name']}")
            st.write(f"**Service selected:** {st.session_state.service}")
            st.write(f"**Area:** {facility['area']}")
            st.warning(
                "These example times are not live availability. Selecting one does not book an appointment."
            )
            st.session_state.slot = st.radio(
                "Example appointment time",
                facility["slots"],
                horizontal=True,
            )
            st.text_area(
                "Questions you would ask the CHV (optional)",
                placeholder="For example: How can I confirm the facility is open?",
            )
            st.checkbox(
                "I understand this is not a real booking.",
                value=True,
                key="booking_ack",
            )
            st.button(
                "Review next steps →",
                type="primary",
                use_container_width=True,
                on_click=go,
                args=("Next steps",),
            )

else:
    st.subheader("Your next step")
    if st.session_state.facility:
        st.success("You have reviewed a sample care option.")
        st.markdown(f"**Facility option:** {st.session_state.facility}")
        st.markdown(
            f"**Example time selected:** {st.session_state.slot or 'Not selected'}"
        )
    else:
        st.info(
            "You have reached the end of the demo. Return to the facility list "
            "to explore sample options."
        )

    st.markdown("### How the proposed community-to-clinic pathway would work")
    pathway = [
        ("1. Patient", "The patient identifies a need and chooses whether to seek navigation support."),
        ("2. CHV", "A recognised CHV explains available options and supports navigation within the CHV's authorised role."),
        ("3. Kuza Wellness", "The platform helps the patient understand the next step and identify a suitable facility using verified information in a future live service."),
        ("4. Health facility", "The patient attends or contacts the facility. Qualified facility staff decide on assessment, treatment, and clinical follow-up."),
        ("5. Follow-up", "If the patient agrees and the approved programme permits it, the CHV may support follow-up or help the patient understand the next step."),
    ]
    for title, description in pathway:
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(description)

    st.markdown("### What must be agreed before this can operate")
    st.markdown(
        "- The relevant CHW programme and health centre must approve the CHV's role in the workflow.\n"
        "- Facilities must agree how referrals are received, assessed, escalated, and acknowledged.\n"
        "- CHV and facility responsibilities must be clear; CHVs do not make clinical decisions.\n"
        "- Patient consent, privacy, data access, and follow-up procedures must be established."
    )
    st.warning(
        "This is a proposed workflow for future validation. This prototype does not "
        "send referrals, contact CHVs or clinics, access clinical records, reserve appointments, "
        "store patient records, or replace professional medical advice."
    )
    st.button("Restart demo", type="primary", use_container_width=True, on_click=reset)

st.divider()
st.caption(
    "Prototype purpose: explore whether the CHV explanation, consent step, and path "
    "to healthcare options feel understandable and trustworthy."
)
st.caption(
    "For a medical emergency, seek urgent local medical help rather than relying on this prototype."
)
