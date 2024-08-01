import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_utils import generate_prompt
from langchain.chains import LLMChain
from utils import switch_page

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model_name="gpt-4o-mini")

prompt_path = "prompts/generate_correct.prompt"
prompt = generate_prompt(prompt_path, "{question}, {first_option}, {second_option}")

question = st.session_state.question

first_option = st.session_state.first_option
second_option = st.session_state.second_option

chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
result = chain(
    {"question": question, "first_option": first_option, "second_option": second_option}
)

st.write(result["text"])
if st.button("이어서 진행해볼까요?"):
    switch_page("round_story")
