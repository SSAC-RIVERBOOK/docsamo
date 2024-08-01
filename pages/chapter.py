import streamlit as st
from utils import show_menu, show_user_data, show_user_status, switch_page

st.session_state.game_page = "chapter"

with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        st.button("홍길동전")
    with col2:
        st.button("별주부전")
    with col3:
        st.button("흥부와 놀부")

with st.container():
    col4, col5, col6 = st.columns(3)

    with col4:
        st.button("콩쥐팥쥐")
    with col5:
        if st.button("춘향전"):
            switch_page("round_select")
    with col6:
        st.button("선녀와 나무꾼")

st.markdown(
    """
    <style>
    .block-container {
        width: 100vw;
        max-width: 600px;
        height: 100vh;
        max-height: 600px;
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
        height: 200px;
        background-color: #D9D9D9;
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

show_menu(st.session_state.prev_page)
show_user_data(["유형1", "유형2", "유형3"], [3, 7, 10], True, 400)
show_user_status("이주배경어린이", "마지막 진행상황(챕터-라운드)", border=True)
