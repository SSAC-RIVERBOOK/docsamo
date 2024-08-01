import streamlit as st
from utils import show_menu, switch_page

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
            switch_page("round")
    with col6:
        st.button("선녀와 나무꾼")

show_menu(st.session_state.prev_page)
