import streamlit as st
from utils import show_menu, switch_page

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
