import streamlit as st
from utils import show_menu, show_user_data, show_user_status, switch_page

st.set_page_config(page_title="맞춤법 용사, 마춤뺌 마왕", page_icon=None, layout="wide")

st.session_state.game_page = "prolog"

with st.container():
    st.header("게임 배경 설명")
    col1, col2 = st.columns(2, vertical_alignment="bottom")
    with col1:
        pass
    with col2:
        if st.button("다음"):
            switch_page("chapter")

show_menu(st.session_state.prev_page, st.session_state.game_page)
show_user_data(["유형1", "유형2", "유형3"], [3, 7, 10], True, 400)
show_user_status("이주배경어린이", "마지막 진행상황(챕터-라운드)", border=True)
