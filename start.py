import streamlit as st
from utils import show_menu, show_user_data, switch_page

st.set_page_config(page_title="맞춤법 용사, 마춤뺌 마왕", page_icon=None, layout="wide")

st.session_state.game_page = "start"

with st.container():
    st.title("맞춤법 용사, 마춤뻡 마왕")
    if st.button("시작"):
        switch_page("prolog")
    st.button("종료")

st.markdown(
    """
    <style>
    h1 {
        text-align: center;
        margin: 5vh;
    }
    .block-container {
        width: 100vw;
        max-width: 600px;
        height: 100vh;
        max-height: 450px;
        background-color: #f0f0f0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border-radius: 10px;
    }
    .st-emotion-cache-1jicfl2 {
        padding-left: 0rem;
        padding-right: 0rem;
    }
    .st-emotion-cache-1jicfl2 {
        padding: 0rem 0rem 0rem;
    }
    .row-widget.stButton {
        display: flex;
        justify-content: center;
    }
    .st-emotion-cache-8542t9 {
        gap: 0.2rem;
    }
    .st-emotion-cache-bm2z3a {
        display: flex;
        width: 100%;
        overflow: auto;
        -webkit-box-align: center;
        align-items: center;
        justify-content: center;
        flex-direction: row;
    }
    .st-emotion-cache-1vt4y43 {
        background-color: #D9D9D9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

show_menu(prev_page="", current_page=st.session_state.game_page)
show_user_data(["유형1", "유형2", "유형3"], [3, 7, 10], True, 400)
