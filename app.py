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
