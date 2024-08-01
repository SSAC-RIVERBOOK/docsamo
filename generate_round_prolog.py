from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_utils import get_retriever
from redis_utils import get_key_events

### 라운드의 도입부 생성 ###


# 프롬프트 1 (문제3개 활용한 도입부 생성)
def generate_round_prolog(event1, event2, event3, chapter_num):
    load_dotenv()

    llm = ChatOpenAI(model="gpt-4o-mini")
    retriever = get_retriever(chapter_num=chapter_num, k_value=2)
    prompt = PromptTemplate.from_template(
        """
    너는 이야기의 도입부를 만들어내는 역할을 담당하는 작가야.
    Use the following pieces of retrieved context and events to write <도입부> of story.
    인물의 관계를 잘 인지하고 도입부를 작성해.
    어떻게 작성해야 할지 모르겠다면, 모르겠다고 말해
    한국어로 대답해줘.

    #Rules
    You must follow below rules, if you won't you will get penalty.
    - 사건의 실마리를 언급하라.
    - 반드시 <Introduction>에 <event>의 결말이 포함 되어서는 안된다.
    - "let's think step by step"
    - ensure that your answer is unbiased and avoids relying on stereotypes.
    - answer a question in a natural, human-like manner
    - Anwer in Korean.
    - 제약사항 : 8줄 이내로 작성해라.

    #Example
    event1
    옛날에 흥부와 놀부라는 형제가 살았어요. 형인 놀부는 마음씨가 고약한 심술쟁이 였고, 동생 흥부는 마음씨가 착한 사람이었어요.  그러던 어느날 놀부와흥부의 부모님이 돌아가셨어요.
    
    event2
    놀부는 집안 재산을 모두 차지하고는 흥부네 식구를 내쫓아 버렸어요.
    “이제부터는 각자 살아가도록 하자”
    
    event3
    흥부는 결국 놀부에게 쫓겨나고,낡은 초가집에 살림을 차렸어요
    
    Introduction
    흥부와 놀부라는 형제가 살았어요. 형인 놀부는 마음씨가 고약한 심술쟁이였고, 동생 흥부는 마음씨가 착한 사람이었어요. 그러던 어느 날, 두 형제에게 사건이 벌어지고, 두 형제의 운명은 크게 엇갈리기 시작하는데...

    #Context
    {context1}
    {context2}
    {context3}
    
    #Answer
    event1
    {event1}

    event2
    {event2}

    event3
    {event3}

    Introduction"""
    )

    chain = prompt | llm

    response = chain.invoke(
        {
            "event1": event1,
            "event2": event2,
            "event3": event3,
            "context1": retriever.invoke(event1),
            "context2": retriever.invoke(event2),
            "context3": retriever.invoke(event3),
        }
    )
    print(response.content)


if __name__ == "__main__":
    load_dotenv()
    data = get_key_events(1, 4)
    generate_round_prolog(data[0], data[1], data[2], 1)
