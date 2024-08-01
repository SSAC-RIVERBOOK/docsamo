import streamlit as st
from langchain_utils import generate_correct_solve
from langchain.chains import LLMChain
from utils import switch_page, show_menu

st.session_state.game_page = "round_win"

result = generate_correct_solve(
    st.session_state.question,
    st.session_state.first_option,
    st.session_state.second_option,
)
st.write(result)

if st.button("이어서 진행해볼까요?"):
    switch_page("round_story")

show_menu(st.session_state.prev_page)
