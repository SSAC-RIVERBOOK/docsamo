import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
import streamlit as st


### 라운드의 도입부 생성 ###


# 프롬프트 1 (문제3개 활용한 도입부 생성)
def generate_round_prolog(event1, event2, event3, full_story):
    load_dotenv()

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-4o-mini")

    prompt = PromptTemplate.from_template(
        """
    [페르소나]
    - 너는 '유명한 스토리텔러'이다. 
    - 초등학교 저학년에게 설명하듯이 친절하게 작성해.
    - 아이들이 이해하기 쉬운 단어를 사용해.
    - 너는 밝고 긍정적인 생각을 한다.

    [역할]
    - 라운드의 <도입부>를 작성해라. 

    [참고사항]
    - 1개의 <라운드>는 3개의 <사건>들로 구성된다.

    [<도입부> 작성시 주의사항]
    - 사용자가 다음 이야기를 궁금해하게금 글을 작성해.
    - 사건의 실마리를 언급해라.
    - 요약한 내용에 라운드의 결말을 포함한다면 패널티를 줄거야.

    [예시1]
    ***event1***
    옛날에 흥부와 놀부라는 형제가 살았어요. 형인 놀부는 마음씨가 고약한 심술쟁이 였고, 동생 흥부는 마음씨가 착한 사람이었어요.  그러던 어느날 놀부와흥부의 부모님이 돌아가셨어요.
    ***event2***
    놀부는 집안 재산을 모두 차지하고는 흥부네 식구를 내쫓아 버렸어요.
    “이제부터는 각자 살아가도록 하자”
    ***event3***
    흥부는 결국 놀부에게 쫓겨나고,낡은 초가집에 살림을 차렸어요

    ***도입부***
    흥부와 놀부라는 형제가 살았어요. 형인 놀부는 마음씨가 고약한 심술쟁이였고, 동생 흥부는 마음씨가 착한 사람이었어요. 그러던 어느 날, 두 형제에게 사건이 벌어지고, 두 형제의 운명은 크게 엇갈리기 시작하는데...


    [주의사항]
    <도입부> 생성 시 아래의 주의사항을 반드시 지켜라. 그렇지 않으면 패널티를 줄 것이다.
    - "let's think step by step"
    - 더 나은 답변을 하면 $100의 보상이 보상이 있습니다.
    - ensure that your answer is unbiased and avoids relying on stereotypes.
    - answer a question in a natural, human-like manner
    - 제약사항 : 8줄 이내로 작성해라.


    ***[입력]***
    event1 : {event1}

    event2 : {event1}

    event3 : {event3}
    
    ***[참고 이야기]***
    full_story

    ***[도입부]***"""
    )

    chain = (
        {
            "event1": RunnablePassthrough(),
            "event2": RunnablePassthrough(),
            "event3": RunnablePassthrough(),
            "full_story": RunnablePassthrough(),
        }
        | prompt
        | llm
    )

    response = chain.invoke(
        {"event1": event1, "event2": event2, "event3": event3, "full_story": full_story}
    )
    print(response.content)


event1 = "몽룡은 책을 읽으면서도 불안한 마음을 감추지 못하고 여러 번 앉았다 일어났다 하며 안절부절합니다. 그의 아버지인 부사는 몽룡의 열심히 공부하는 모습을 보고 기특하게 여깁니다. 그러나 몽룡은 자신의 마음속에 있는 춘향에 대한 그리움으로 인해 공부에 집중할 수 없는 상황입니다."
event2 = "몽룡은 방자에게 춘향을 만나고 싶다는 마음을 드러냅니다. 방자는 몽룡에게 부모를 속이는 것이 옳지 않다고 경고하며, 춘향의 집에 몰래 가는 방법을 제안합니다. 방자는 몽룡이 아버지의 눈을 피하면서 춘향을 만날 수 있도록 도와주기로 결심합니다. 몽룡은 방자의 제안을 듣고 고민하지만, 결국 춘향을 만나고 싶다는 마음이 우세해집니다."
event3 = '몽룡은 드디어 춘향의 집에 도착하게 되고, 두 사람은 감정을 나누며 서로의 존재에 대한 기쁨을 표현합니다. 몽룡은 춘향에게 "내가 오늘 밤에 찾아올 줄 몰랐더냐?"라고 말하며 서로의 마음을 확인합니다. 그들은 함께 시간을 보내며 사랑의 감정을 나누고, 아버지와의 관계에 대한 고민도 나누게 됩니다. 이 순간은 두 사람의 사랑이 더욱 깊어지는 계기가 됩니다.'


def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return content


file_path = "./full_story.txt"
content = read_file(file_path)
# print(content)

generate_round_prolog(event1, event2, event3, content)
