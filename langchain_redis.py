from langchain_community.document_loaders import TextLoader
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import (
    ChatOpenAI,
)
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables.base import RunnableSerializable
from dotenv import load_dotenv
import redis

load_dotenv()

# RecursiveCharacterTextSplitter 통해 가져온 정보를 chunk 로 쪼개기
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# 프롬프트 설정
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

# llm 모델 입력
llm = ChatOpenAI(model_name="gpt-4o-mini")

chain = prompt | llm


# 함수화
def get_3key_events(
    number: int, splitter: CharacterTextSplitter, chain: RunnableSerializable
):
    load_dotenv()

    response = TextLoader(
        f"/mnt/c/Users/User/Desktop/SSAC/team/docsamo-develop/호준's 춘향전 텍스트파일/춘향전{number}편.txt"
    )
    data = response.load()

    splits = splitter.split_documents(data)
    response = chain.invoke(splits)

    return response


# response 타입 찍어보고 아래에 redis의 어떤 메소드 종류를 사용할 지 정할 수 있다.
result = get_3key_events(1, splitter, chain)
print(result)
print(type(result.content))

# print(get_3key_events(number=7, splitter=splitter, chain=chain))
# 1~7편까지 들어갈 반복문(따로 바깥에서 get_3key_events 가 실행되게끔)

r = redis.Redis(host="localhost", port=6379, db=0)
r.set("chapter1_key_event", result.content)
print(r.get("chapter1_key_event").decode("utf-8"))


# 핵심사건 3가지 생성 후 임베딩하지 않고 redis에 저장하는 형식입니다.
# 이 때 get_3key_events 의 number에 들어갈 인풋을 반복문으로 돌려야하고 함수밖에서 할지 안에서 할지 정해야합니다.
