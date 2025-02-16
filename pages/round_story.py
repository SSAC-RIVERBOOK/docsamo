from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from redis_utils import get_key_events
from langchain_utils import get_retriever
import streamlit as st
from utils import switch_page

st.session_state.game_page = "round_story"
chapter, problem = st.session_state.chapter, st.session_state.problem


def generate_connection(first_story, second_story, chapter_num):
    load_dotenv()

    llm = ChatOpenAI(name="gpt-4o-mini")
    retriever = get_retriever(chapter_num=chapter_num, k_value=2)
    prompt = PromptTemplate.from_template(
        """
    #역할
    - context를 참고해서 "first_story"와 "second_story" 두 개의 이야기 사이에 들어갈 <중간 이야기>를 만들어라.
    - <중간 이야기>를 작성 시, 초등학교 저학년에게 설명하듯이 친절하게 작성하라.
    - <중간 이야기>를 작성 시, 초등학교 저학년이 이해하기 쉬운 단어를 사용하라.

    #예시
    1.
    first_story
    옛날에 흥부와 놀부라는 형제가 살았어요. 형인 놀부는 마음씨가 고약한 심술쟁이 였고, 동생 흥부는 마음씨가 착한 사람이었어요.  그러던 어느날 놀부와 흥부의 부모님이 돌아가셨어요. 

    second_story 
    “이제부터는 각자 살아가도록 하자”. 놀부는 집안 재산을 모두 차지하고는 흥부네 식구를 내쫓아 버렸어요. 

    <중간이야기>
    부모님이 돌아가신 후, 형제는 큰 슬픔에 잠겼습니다. 시간이 지나면서 놀부는 재산을 독차지하려는 마음을 품었습니다. 흥부는 형과 함께 유산을 나누고 서로 돕길 원했지만, 놀부는 자신의 계획을 고수했습니다. 결국, 흥부는 형의 마음을 돌릴 수 없었고, 두 사람 사이에는 갈등이 깊어졌습니다.

    2.
    first_story
    “형님, 곡식이 있으면 좀 나누어 주세요. 흥부가 놀부에게 말했어요” “예끼 이놈! 너 줄 곡식 없어! 당장 내집에서 나가!” 놀부는 몽둥이를 휘두르며 흥부를 쫓아 냈어 흥부는 부랴부랴 부엌으로 도망갔어요. 부엌에는 놀부의 아내가 밥을 푸고 있었어요. “ 아니 어딜 함부로 들어오는 거예요?” 놀부의 아내가 흥부를 내쫓았어요.

    second_story
    흥부는 계속해서 어려운 상황 속에서 생계를 위해 애쓰는 가운데 친형 놀부에게 외면 받은 사실에 괴로움을 겪는다. 흥부네 가족들은 나날이 생활고가 심해진다.

    <중간이야기>
    놀부네 집에서 매몰차게 거절당한 흥부는 울면서 집에 왔습니다. "아버지! 밥 가지고 왔어요?" 아내와 아이들이 흥부에게 물어봤어요. 흥부는 놀부의 외면에 눈물을 흘렸고 가족들은 모두 슬픔에 잠겼습니다.


    #주의사항
    - <중간 이야기> 생성 시 아래의 주의사항을 반드시 지켜라. 그렇지 않으면 패널티를 줄 것이다.
    - first_story와 second_story의 내용이 들어가지 않도록 해라. 
    - 주어진 두 이야기가 자연스럽게 이어지도록 작성해라.
    - "let's think step by step"
    - 더 나은 답변을 하면 $100의 보상이 보상이 있습니다.
    - ensure that your answer is unbiased and avoids relying on stereotypes.
    - answer a question in a natural, human-like manner
    - 제약사항 : 6줄 이내로 작성해라. 

    #Context
    {context1}
    {context2}

    #Answer
    first_story : {first_story}

    second_story: : {second_story}

    <중간 이야기>"""
    )
    chain = prompt | llm
    # first_story = '으앙! 아버지 배고파요! 아이들은 매일매일 울어 댔어요 "놀부형님께 가서 먹을 것 좀 얻어 오겠소"'
    # second_story = "“형님, 곡식이 있으면 좀 나누어 주세요. 흥부가 놀부에게 말했어요” “예끼 이놈! 너 줄 곡식 없어! 당장 내집에서 나가!” 놀부는 몽둥이를 휘두르며 흥부를 쫓아 냈어 흥부는 부랴부랴 부엌으로 도망갔어요. 부엌에는 놀부의 아내가 밥을 푸고 있었어요. “ 아니 어딜 함부로 들어오는 거예요?” 놀부의 아내가 흥부를 내쫓았어요."
    response = chain.invoke(
        {
            "first_story": first_story,
            "second_story": second_story,
            "context1": retriever.invoke(first_story),
            "context2": retriever.invoke(second_story),
        }
    )

    return response.content


# 예시 chapter1 key event 2, 3


if st.session_state.problem == 3:
    st.write("라운드 클리어~")
    if st.button("라운드 선택 화면으로 가기"):
        st.session_state.problem = 1
        st.session_state.question = None
        switch_page("round_select")
else:
    data = get_key_events(problem, problem + 2, chapter_num=chapter)
    response = generate_connection(data[0], data[1], chapter_num=chapter)
    st.write(response)
    if st.button("다음 문제로 이동하기"):
        st.session_state.question = None
        st.session_state.problem += 1
        switch_page("round_game")
