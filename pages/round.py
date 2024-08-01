import streamlit as st
from utils import show_menu

st.session_state.game_page = "round"

show_menu(st.session_state.prev_page)
