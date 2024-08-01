import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_utils import generate_prompt
from langchain.chains import LLMChain
from utils import switch_page, show_menu

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-4o-mini")

prompt_path = "prompts/generate_false_story.prompt"
prompt = generate_prompt(prompt_path, "{question}, {answer}")

# 페이지 이름 저장
st.session_state.game_page = "round_lose"

question = st.session_state.question

# 선택한 정답이 뭔지 구분 -> 나중에 버튼이 생기면 없어질 부분
if st.session_state.select == "true":
    answer = st.session_state.first_option
else:
    answer = st.session_state.second_option

chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
result = chain({"question": question, "answer": answer})

st.write(result["text"])

if st.button("다시 한번 풀어보기"):
    switch_page("round_game")

show_menu(st.session_state.prev_page)
