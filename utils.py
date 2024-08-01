import streamlit as st
import datetime
from typing import Optional, List
import streamlit as st
import pandas as pd
import altair as alt


def switch_page(page_name: str):
    """
    streamlit의 multipage간의 이동을
    사이드 바가 아닌 버튼 등으로 이용하기 위한 함수입니다.
    streamlit run으로 실행되는 main app의 이름은 page 변수에 저장 되며,
    main app을 교체할시 같이 바꾸어야 합니다.
    이동할 페이지 파일들은 main app과 같은 위치에 있는 pages 디렉토리에 존재해야 합니다.
    함수 작동 시, st.session_state.prev_page가 자동 갱신 됩니다.
    Args:
        page_name (str): 이동할 페이지 이름(.py 빼고)

    Raises:
        RerunException: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    from streamlit.runtime.scriptrunner import RerunData, RerunException
    from streamlit.source_util import get_pages

    def standardize_name(name: str) -> str:
        """
        switch_page에서 입력받은 page_name을 정규화 하기 위한 함수입니다.
        _를 \\s 로 교체 후 소문자로 바꾸어 반환합니다.
        Args:
            name (str): switch_page 함수의 page_name argument

        Returns:
            str: 정규화된 page_name
        """
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("navigator.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config.get("page_name", "")) == page_name:
            st.session_state.prev_page = st.session_state.game_page
            raise RerunException(
                RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [
        standardize_name(config.get("page_name", "")) for config in pages.values()
    ]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


def show_sidebar() -> None:
    """
    설정 및 분석 페이지로 이동하기 위해 사용되는
    사이드바를 불러옵니다.
    """
    with st.sidebar:
        if st.button("user"):
            switch_page("user")
        if st.button("user_analysis"):
            switch_page("user_analysis")
        if st.button("settings"):
            switch_page("settings")


def start_service() -> None:
    """
    stateful한 웹사이트를 위해 session_state에 저장할 변수를 초기화 하기위한 함수입니다.
    """
    if "service_started" not in st.session_state:
        st.session_state.service_started = True
        st.session_state.count = 0
        st.session_state.last_updated = datetime.time(0, 0)
        st.session_state.celsius = 50.0


def show_menu(
    prev_page: str,
    current_page: str = "",
    height: Optional[int] = None,
    border: bool = False,
) -> None:
    """
    st.siderbar.container()를 이용해 사이드 바의 독립된 공간에
    페이지 이동, 지난 대화 보기, 설정 페이지 이동 버튼을 생성하는 함수입니다.
    height를 지정하여 일정 길이 이상이 되면 스크롤이 되도록 할 수 있습니다.
    border를 True로 두어 공간을 테두리로 감쌀 수 있습니다.

    Args:
        prev_page (str): _description_
        current_page (str, optional): _description_. Defaults to "".
        height (Optional[int], optional): _description_. Defaults to None.
        border (bool, optional): _description_. Defaults to False.
    """
    in_game_list = set(
        [
            "start",
            "prolog",
            "chapter",
            "round_select",
            "round_game",
            "round_win",
            "round_lose",
        ]
    )
    page_name_mapper = {
        "start": "시작화면",
        "prolog": "게임소개",
        "chapter": "챕터 선택",
        "round_select": "라운드 선택",
        "round_game": "라운드 게임",
        "round_win": "라운드 승리",
        "round_lose": "라운드 패배",
    }
    with st.sidebar.container(border=border, height=height):
        st.header("메뉴")
        if current_page not in set(["start", "prolog"]):
            if st.button("1. 메인 화면으로 이동", use_container_width=True):
                switch_page("start")

            if st.button(
                f"2. 이전 ({page_name_mapper[prev_page]}) 화면으로 이동",
                use_container_width=True,
            ):
                switch_page(prev_page)

            if current_page in in_game_list:
                st.button("3. 지난 대화 보기", use_container_width=True)

        if st.button("4. 설정", use_container_width=True):
            switch_page("settings")


def get_chart(
    category: list,
    value: list,
    valueuse_container_width: bool,
):
    """
    도넛 차트를 만드는 차트

    Args:
        category (list): _description_
        value (list): _description_
        valueuse_container_width (bool): _description_
    """
    # category: 유형 value: 값
    source = pd.DataFrame({"category": category, "value": value})

    chart = (
        alt.Chart(source)
        .mark_arc(innerRadius=0)
        .encode(
            theta=alt.Theta(field="value", type="quantitative"),
            color=alt.Color(field="category", type="nominal"),
        )
    )
    st.altair_chart(chart, theme="streamlit", use_container_width=True)


def show_user_data(
    category: list,
    value: list,
    border: bool = False,
    height: Optional[int] = None,
    # chart에 category, value 값 넣을 예정
) -> None:
    """
    st.siderbar.container()를 이용해 사이드 바의 독립된 공간에
    사용자의 풀이 기록을 분석한 결과를 보여주는 공간을 생성하는 함수입니다.
    height를 지정하여 일정 길이 이상이 되면 스크롤이 되도록 할 수 있습니다.
    border를 True로 두어 공간을 테두리로 감쌀 수 있습니다.

    Args:
        category (list): _description_
        value (list): _description_
        border (bool, optional): _description_. Defaults to False.
        height (Optional[int], optional): _description_. Defaults to None.
    """
    with st.sidebar.container(border=border, height=height):
        st.header("사용자 데이터 분석")
        st.subheader("강점")
        get_chart(category, value, True)  # 강점
        st.subheader("약점")
        get_chart(category, value, True)  # 약점


def show_user_status(
    user_name: str, page_name: str, border: bool = False, height: Optional[int] = None
):
    """
    st.siderbar.container()를 이용해 사이드 바의 독립된 공간에
    사용자의 진행 상황을 보여주는 공간을 생성하는 함수입니다.
    height를 지정하여 일정 길이 이상이 되면 스크롤이 되도록 할 수 있습니다.
    border를 True로 두어 공간을 테두리로 감쌀 수 있습니다.

    Args:
        user_name (str): _description_
        page_name (str): _description_
        border (bool, optional): _description_. Defaults to False.
        height (Optional[int], optional): _description_. Defaults to None.
    """
    with st.sidebar.container(border=border, height=height):
        st.header("사용자 정보")
        st.write(f"사용자: {user_name}")
        st.write(f"마지막 진행 상황: {page_name}")


def increment_counter(increment_value: int = 1) -> None:
    """
    statefulness를 확인하기 위한 예시 함수입니다.
    session_state의 count 값을 변화시킵니다.

    Args:
        increment_value (int): count에 더해질 값. Defaults to 1.
    """
    st.session_state.count += increment_value


def update_counter() -> None:
    """
    statefulness를 확인하기 위한 예시 함수입니다.
    session_state의 count, last_updated 값들을 변화시킵니다.
    """
    st.session_state.count += st.session_state.increment_value
    st.session_state.last_updated = st.session_state.update_time
