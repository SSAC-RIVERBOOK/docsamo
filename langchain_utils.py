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
    custom_prompt = ChatPromptTemplate.from_messages(
        messages=[
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(prompt_variable),
        ]
    )
    return custom_prompt


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


def generate_correct_solve(question, first_option, second_option):
    load_dotenv()

    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt_path = "prompts/generate_correct.prompt"
    prompt = generate_prompt(prompt_path, "{question}, {first_option}, {second_option}")

    chain = prompt | llm
    result = chain.invoke(
        {
            "question": question,
            "first_option": first_option,
            "second_option": second_option,
        }
    )
    return result.content


def generate_wrong_solve(question, answer):
    load_dotenv()
    llm = ChatOpenAI(model="gpt-4o-mini")

    prompt_path = "prompts/generate_false_story.prompt"
    prompt = generate_prompt(prompt_path, "{question}, {answer}")

    chain = prompt | llm
    result = chain.invoke({"question": question, "answer": answer})

    return result.content
