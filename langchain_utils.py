from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
import streamlit as st


def load_prompt(file_path: str) -> str:
    """
    prompt를 불러오는 함수입니다.

    Args:
        file_path (str): 파일 경로

    Returns:
        str : prompt
    """
    with open(file_path, "r", encoding="utf-8") as file:
        prompt = file.read().strip()
    return prompt


def generate_prompt(file_path: str, prompt_variable: str) -> ChatPromptTemplate:
    """
    prompt template를 만드는 함수

    Args:
        file_path (str): 파일 경로
        prompt_variable (str): prompt안에 변수

    Returns:
        ChatPromptTemplate: prompt template
    """
    system_prompt = load_prompt(file_path)
    custom_prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(prompt_variable),
        ]
    )
    return custom_prompt


def generate_question(story, select):
    load_dotenv()

    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt_path = "prompts/generate_question.prompt"
    prompt = generate_prompt(prompt_path, "{story}, {select}")
    # prompt = generate_prompt(prompt_path, "{first_story}, {second_story}, {select}")

    st.session_state.select = "false"
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

    # question과 option들을 session_state에 저장
    question_idx = result["text"].find("1")
    st.session_state.question = result["text"][:question_idx]
    first_option_idx = result["text"].find("2", question_idx)
    st.session_state.first_option = result["text"][question_idx:first_option_idx]
    st.session_state.second_option = result["text"][first_option_idx:]
