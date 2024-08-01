import streamlit as st
from langchain_utils import generate_wrong_solve
from utils import switch_page, show_menu

# 페이지 이름 저장
st.session_state.game_page = "round_lose"

# 선택한 정답이 뭔지 구분 -> 나중에 버튼이 생기면 없어질 부분
if st.session_state.select == "true":
    answer = st.session_state.first_option
else:
    answer = st.session_state.second_option

result = generate_wrong_solve(st.session_state.question, answer)
st.write(result)

if st.button("다시 한번 풀어보기"):
    switch_page("round_game")

show_menu(st.session_state.prev_page)
