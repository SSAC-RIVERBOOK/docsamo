import streamlit as st
from utils import show_menu, show_user_data, show_user_status, switch_page

st.set_page_config(page_title="맞춤법 용사, 마춤뺌 마왕", page_icon=None, layout="wide")

st.session_state.game_page = "prolog"

with st.container():
    st.title("게임 배경 설명")
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
        pass
    with col2:
        if st.button("다음"):
            switch_page("chapter")

st.markdown(
    """
    <style>
    h1 {
        text-align: center;
        margin-bottom: 19vh;
    }
    .block-container {
        width: 100vw;
        max-width: 816px;
        height: 100vh;
        max-height: 624px;
        background-color: #f0f0f0;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
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
        justify-content: flex-end;
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
        width: 150px;
        height: 100px;
        background-color: #D9D9D9;
        margin-right: 2vw;
        margin-bottom: 1vh;
    }
    .st-emotion-cache-ocqkz7 {
        display: flex;
        flex-wrap: wrap;
        -webkit-box-flex: 1;
        flex-grow: 1;
        -webkit-box-align: stretch;
        align-items: stretch;
        gap: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

show_menu(st.session_state.prev_page, st.session_state.game_page)
show_user_data(["유형1", "유형2", "유형3"], [3, 7, 10], True, 400)
show_user_status("이주배경어린이", "마지막 진행상황(챕터-라운드)", border=True)
