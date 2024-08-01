# 춘향전 1~7편을 load > split > index_name='chapter{x}'로 vectorstore에 저장 => RAG 준비 완료
from typing import List
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.redis import Redis
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSerializable
from dotenv import load_dotenv
import redis


def get_split_docuemnts(num: int, text_splitter: CharacterTextSplitter):
    # 문서 로드
    loader = TextLoader(f"./folktales/춘향전{num}편.txt")
    documents = loader.load()
    # 문서 분할
    split_documents = text_splitter.split_documents(documents)
    return split_documents


def store_to_vectorstore(num, split_documents, embeddings) -> None:
    # 분할된 문서들을 vectorstore에 저장
    Redis.from_documents(
        documents=split_documents,
        embedding=embeddings,
        redis_url="redis://localhost:6379/0",
        index_name=f"chapter{num}",
    )
    return


def get_3key_events(split_documents, chain: RunnableSerializable) -> List[str]:
    response = chain.invoke(split_documents)
    return response.content.split("\n\n")


def store_to_db(num, sub_num, key_event) -> None:
    # db 객체 생성
    r = redis.Redis(host="localhost", port=6379, db=0)
    # db 에 저장
    r.set(f"chapter{num}_key_event{sub_num}", key_event)
    return


def main(num, text_splitter, embeddings, chain):
    # 문서 로드 및 분할
    split_documents = get_split_docuemnts(num=num, text_splitter=text_splitter)
    # 분할된 문서를 RAG를 위해 vectorstore에 저장
    store_to_vectorstore(num, split_documents, embeddings)
    # 분할된 문서를 입력으로 사용해서 핵심 사건 3개 생성
    key_events = get_3key_events(split_documents=split_documents, chain=chain)
    for idx, key_event in enumerate(key_events, start=1):
        # 핵심 사건을 db에 저장
        store_to_db(num=num, sub_num=idx, key_event=key_event)


if __name__ == "__main__":
    load_dotenv()
    # 문서 분할기 생성
    text_splitter = CharacterTextSplitter(
        # 텍스트를 분할할 때 사용할 구분자를 지정합니다. 기본값은 "\n\n"입니다.
        # separator=" ",
        # 분할된 텍스트 청크의 최대 크기를 지정합니다.
        chunk_size=1000,
        # 분할된 텍스트 청크 간의 중복되는 문자 수를 지정합니다.
        chunk_overlap=100,
        # 텍스트의 길이를 계산하는 함수를 지정합니다.
        length_function=len,
        # 구분자가 정규식인지 여부를 지정합니다.
        is_separator_regex=False,
    )

    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    prompt = PromptTemplate.from_template(
        """[Instruction]
    You are an assistant for story telling tasks. 
    Use the following pieces of retrieved context to describe 3 key events. 
    If you cannot describe, just say that you cannot. 
    Answer in Korean.

    #Example:
    ### 사건 1: 몽룡과 방자의 대화
    몽룡은 방자에게 남원 고을의 경치에 대해 묻습니다. 방자는 다양한 경치를 설명하며, 특히 광한루와 오작교를 추천합니다. 몽룡은 그곳으로 나가자고 결심하고, 방자는 몽룡의 결정을 걱정하며 경고하지만 결국 몽룡은 나귀를 준비하라고 지시합니다.

    ### 사건 2: 광한루에서의 만남
    몽룡은 광한루에 도착하여 주변 경치를 감상합니다. 그때, 그는 그네를 뛰는 아름다운 처녀를 발견하고 그녀에게 매료됩니다. 방자는 그 처녀가 누구인지 묻자, 몽룡은 그녀가 범상한 여자가 아니라고 확신합니다. 방자는 그 처녀가 퇴기 월매의 딸 춘향이라고 알려주고, 몽룡은 춘향을 불러오고 싶어 하지만 방자는 그럴 수 없다고 말합니다.

    ### 사건 3: 춘향의 답장
    몽룡은 춘향에게 편지를 보내고, 방자는 그 편지를 전달합니다. 춘향은 몽룡의 편지를 읽고 감격하여 답장을 쓰기로 결심합니다. 그녀는 자신의 마음을 담아 몽룡에게 답장을 보내고, 그 안에는 몽룡에 대한 사랑과 기대가 담겨 있습니다.

    #Context: 
    {context} 

    #Answer:"""
    )

    llm = ChatOpenAI(model="gpt-4o-mini")

    chain = prompt | llm

    for idx in range(1, 8):
        main(num=idx, text_splitter=text_splitter, embeddings=embeddings, chain=chain)
    # # 데이터 확인
    # r = redis.Redis(host="localhost",port=6379, db=0)
    # for idx in range(1, 8):
    #     for sub_idx in range(1, 4):
    #         print(r.get(f"chapter{idx}_key_event{sub_idx}").decode("utf-8"))
