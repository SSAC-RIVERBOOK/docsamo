from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores.redis import Redis
from langchain_core.vectorstores import VectorStoreRetriever


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


def get_retriever(chapter_num: int, k_value=4):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    rds = Redis(
        redis_url="redis://localhost:6379/0",
        index_name=f"chapter{chapter_num}",
        embedding=embeddings,
    )
    retriever = rds.as_retriever(search_kwargs={"k": k_value})
    # retriever = VectorStoreRetriever(vectorstore=rds, search_type="similarity", search_kwargs={"k": k_value})

    return retriever


def generate_question(story, select, chapter_num=1) -> str:
    load_dotenv()
    llm = ChatOpenAI(model="gpt-4o-mini")
    retriever = get_retriever(chapter_num=chapter_num, k_value=1)
    prompt_path = "prompts/generate_question2.prompt"
    prompt = generate_prompt(prompt_path, "{story}, {select}, {context}")

    # prompt = generate_prompt(prompt_path, "{first_story}, {second_story}, {select}")
    chain = prompt | llm
    result = chain.invoke(
        {
            "story": story,
            "select": select,
            "context": retriever.invoke(story),
        }
    )
    return result.content


def generate_correct_solve(question, first_option, second_option, chapter_num=1):
    load_dotenv()

    llm = ChatOpenAI(model="gpt-4o-mini")
    retriever = get_retriever(chapter_num=chapter_num, k_value=3)
    prompt_path = "prompts/generate_correct.prompt"
    prompt = generate_prompt(
        prompt_path, "{question}, {first_option}, {second_option}, {context}"
    )

    chain = prompt | llm
    result = chain.invoke(
        {
            "question": question,
            "first_option": first_option,
            "second_option": second_option,
            "context": retriever.invoke(question),
        }
    )
    return result.content


def generate_wrong_solve(question, answer, chapter_num=1):
    load_dotenv()
    llm = ChatOpenAI(model="gpt-4o-mini")
    retriever = get_retriever(chapter_num=chapter_num, k_value=3)
    prompt_path = "prompts/generate_false_story.prompt"
    prompt = generate_prompt(prompt_path, "{question}, {answer}, {context}")

    chain = prompt | llm
    result = chain.invoke(
        {
            "question": question,
            "answer": answer,
            "context": retriever.invoke(question.replace("-", answer)),
        }
    )

    return result.content
