import streamlit as st
import datetime
from utils import (
    switch_page,
    show_sidebar,
    increment_counter,
    update_counter,
    start_service,
    show_menu,
)

st.set_page_config("choice page.")
print("choice session state:", st.session_state)
st.write("choice page")

st.title("Statefulness Example")
st.session_state.game_page = "choice"
# session_state 값 초기화
start_service()

# if 문을 이용해 직접적으로 변화
increment = st.button("1. st.button을 이용한 count 변화")
if increment:
    st.session_state.count += 1

# on_click 파라미터에 함수 입력
st.button("2. Callbacks를 이용한 count 변화", on_click=increment_counter)

# on_click 파라미터에 함수 입력 후, args 파라미터에 함수의 파라미터(arguments) 입력
increment_value = st.number_input("Enter a value", value=0, step=1)
st.button(
    "3. Args in Callbacks를 이용한 count 변화",
    on_click=increment_counter,
    args=(increment_value,),
)

# 위의 예시와 동일하지만, 함수에 딕셔너리로 전달해서 파라미터의 이름도 같이 전달
st.button(
    "4. Kwargs in Callbacks를 이용한 count 변화",
    on_click=increment_counter,
    kwargs=dict(increment_value=increment_value),
)

# form 내부에 key 파라미터를 이용해 두개의 session_state를 생성한 뒤, 함수 실행
with st.form(key="my_form"):
    st.time_input(
        label="Enter the time", value=datetime.datetime.now().time(), key="update_time"
    )
    st.number_input("Enter a value", value=0, step=1, key="increment_value")
    submit = st.form_submit_button(
        label="5. Forms & Callbacks를 이용한 count 변화", on_click=update_counter
    )

# widget에 key 파라미터를 이용해 session_state를 생성 및 갱신
st.slider(
    "6. Widget을 이용한 celsius 변화", min_value=-100.0, max_value=100.0, key="celsius"
)

st.write("Current Count = ", st.session_state.count)
st.write("Last Updated = ", st.session_state.last_updated)
st.write("Current Celsius = ", st.session_state.celsius)

if st.button("Temporary Home"):
    switch_page("navigator")

if st.button("story"):
    switch_page("story")

show_menu(st.session_state.prev_page, st.session_state.game_page)

switch_page("round_select")
