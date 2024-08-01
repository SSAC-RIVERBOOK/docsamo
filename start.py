import streamlit as st
from utils import show_menu, switch_page

st.session_state.game_page = "start"

with st.container():
    st.title("맞춤법 용사, 마춤뻡 마왕")
    if st.button("시작"):
        switch_page("prolog")
    st.button("종료")

show_menu(prev_page="", current_page=st.session_state.game_page)
