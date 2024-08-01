import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import streamlit as st
from langchain_utils import generate_prompt
from utils import switch_page, show_menu
from langchain_core.runnables import RunnablePassthrough
from redis_utils import get_key_events
import random

# 페이지 이름 저장
st.session_state.game_page = "round_game"

# question, first_option, second_option 초기화
if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.first_option = "1"
    st.session_state.second_option = "2"


def generate_question(story, select) -> str:
    load_dotenv()
    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt_path = "prompts/generate_question2.prompt"
    prompt = generate_prompt(prompt_path, "{story}, {select}")

    # prompt = generate_prompt(prompt_path, "{first_story}, {second_story}, {select}")
    chain = (
        {
            "story": RunnablePassthrough(),
            "select": RunnablePassthrough(),
        }
        | prompt
        | llm
    )
    result = chain.invoke(
        {
            "story": story,
            "select": select,
        }
    )
    return result.content
    # question과 option들을 session_state에 저장
    # question_idx = result.content.find("1")
    # st.session_state.question = result.content[:question_idx]
    # first_option_idx = result.content.find("2", question_idx)
    # st.session_state.first_option = result.content[question_idx:first_option_idx]
    # st.session_state.second_option = result.content[first_option_idx:]


if st.session_state.prev_page != "round_lose" and st.session_state.question is None:
    # 예시 chapter1 key event 2
    data = get_key_events(2, 3)  # redis 에시 데이터 가져오기
    randint = random.randint(0, 1)
    mapper = {0: "false", 1: "true"}
    st.session_state.select = mapper[randint]
    # data[0] 대신에 핵심 사건 하드코딩
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
