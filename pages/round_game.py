import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import streamlit as st
from langchain_utils import generate_prompt
from utils import switch_page

# question, first_option, second_option 초기화
if "question" not in st.session_state:
    st.session_state.question = None
    st.session_state.first_option = "1"
    st.session_state.second_option = "2"


def generate_question():
    load_dotenv()

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-4o-mini")

    prompt_path = "prompts/generate_question.prompt"
    prompt = generate_prompt(prompt_path, "{story}, {select}")
    # prompt = generate_prompt(prompt_path, "{first_story}, {second_story}, {select}")

    st.session_state.story = "사건 1: 몽룡과 방자의 대화 - 몽룡은 방자에게 남원 고을의 경치에 대해 물어봅니다. 방자는 다양한 경치를 설명하며, 특히 광한루와 오작교를 추천합니다. 몽룡은 그곳으로 나가기로 결심하고, 방자는 몽룡의 결정을 걱정하며 경고하지만 결국 몽룡은 나귀를 준비하라고 지시합니다"

    # first_story = "사건 1: 몽룡과 방자의 대화 - 몽룡은 방자에게 남원 고을의 경치에 대해 물어봅니다. 방자는 다양한 경치를 설명하며, 특히 광한루와 오작교를 추천합니다. 몽룡은 그곳으로 나가기로 결심하고, 방자는 몽룡의 결정을 걱정하며 경고하지만 결국 몽룡은 나귀를 준비하라고 지시합니다"
    # second_story = "사건 2: 광한루에서의 만남 - 몽룡은 광한루에 도착하여 경치를 감상하고, 그네를 뛰는 아름다운 처녀를 발견하고 매료됩니다. 방자가 그 처녀가 누구인지 묻자, 몽룡은 그녀가 범상한 여자가 아니라고 확신합니다. 방자는 그 처녀가 퇴기 월매의 딸 춘향이라고 알려주고, 몽룡은 춘향을 불러오고 싶어 하지만 방자는 그럴 수 없다고 말합니다."
    st.session_state.select = "false"
    chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    result = chain(
        {
            # "first_story": first_story,
            # "second_story": second_story,
            "story": st.session_state.story,
            "select": st.session_state.select,
        }
    )

    # question과 option들을 session_state에 저장
    question_idx = result["text"].find("1")
    st.session_state.question = result["text"][:question_idx]
    first_option_idx = result["text"].find("2", question_idx)
    st.session_state.first_option = result["text"][question_idx:first_option_idx]
    st.session_state.second_option = result["text"][first_option_idx:]


if st.session_state.prev_page != "round_lose" and st.session_state.question is None:
    generate_question()

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
