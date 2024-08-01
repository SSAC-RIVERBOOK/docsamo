import streamlit as st
from langchain_utils import generate_question
from utils import switch_page, show_menu
from redis_utils import get_key_events
import random

# 페이지 이름 저장
st.session_state.game_page = "round_game"

# question, first_option, second_option 초기화
if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.first_option = "1"
    st.session_state.second_option = "2"

if st.session_state.prev_page != "round_lose" and st.session_state.question is None:
    # 예시 chapter1 key event 2
    problem = st.session_state.problem
    chapter = st.session_state.chapter
    data = get_key_events(problem, problem + 1, chapter)
    randint = random.randint(0, 1)
    mapper = {0: "false", 1: "true"}
    st.session_state.select = mapper[randint]

    result = generate_question(data[0], st.session_state.select)

    question_idx = result.find("1")
    st.session_state.question = result[8:question_idx]
    first_option_idx = result.find("2", question_idx)
    st.session_state.first_option = result[question_idx:first_option_idx]
    st.session_state.second_option = result[first_option_idx:]


st.write(st.session_state.question)
st.write(st.session_state.first_option)
st.write(st.session_state.second_option)

if st.button(f"{st.session_state.first_option}"):
    if st.session_state.select == "true":
        switch_page("round_win")
    else:
        switch_page("round_lose")
if st.button(f"{st.session_state.second_option}"):
    if st.session_state.select == "true":
        switch_page("round_lose")
    else:
        switch_page("round_win")

show_menu(st.session_state.prev_page)
