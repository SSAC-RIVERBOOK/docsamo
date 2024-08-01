from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate

from redis_utils import get_key_events

### 라운드의 도입부 생성 ###


# 프롬프트 1 (문제3개 활용한 도입부 생성)
def generate_round_prolog(event1, event2, event3):
    load_dotenv()

    llm = ChatOpenAI(model="gpt-4o-mini")

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

    ***[도입부]***"""
    )

    chain = (
        {
            "event1": RunnablePassthrough(),
            "event2": RunnablePassthrough(),
            "event3": RunnablePassthrough(),
        }
        | prompt
        | llm
    )

    response = chain.invoke({"event1": event1, "event2": event2, "event3": event3})
    print(response.content)


if __name__ == "__main__":
    data = get_key_events(1, 4)
    generate_round_prolog(data[0], data[1], data[2])
