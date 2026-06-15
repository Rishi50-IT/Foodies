import streamlit as st
st.markdown("""
<style>

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #2d2d2d !important;
    background: #2d2d2d !important;
}

/* Inner sidebar container */
[data-testid="stSidebar"] > div:first-child {
    background-color: #2d2d2d !important;
    background: #2d2d2d !important;
    backdrop-filter: none !important;
    opacity: 1 !important;
}

/* Prevent transparency everywhere */
section[data-testid="stSidebar"] {
    opacity: 1 !important;
}

/* Make text visible */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Input boxes */
.stTextInput input {
    background-color: white !important;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)
