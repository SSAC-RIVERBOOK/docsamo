import streamlit as st


player_path_arr = [
    "Asset/Player/idle.gif",
    "Asset/Player/attack.gif",
    "Asset/Player/hit.gif",
    "Asset/Player/death.gif",
]
boss_path_arr = ["Asset/Boss/idle.gif", "Asset/Boss/attack.gif"]


def check_player_status(player_status):
    if player_status == "idle":
        return player_path_arr[0]
    elif player_status == "attack":
        return player_path_arr[1]
    elif player_status == "hit":
        return player_path_arr[2]
    elif player_status == "death":
        return player_path_arr[3]


def check_boss_status(boss_status):
    if boss_status == "idle":
        return boss_path_arr[0]
    elif boss_status == "attack":
        return boss_path_arr[1]


if "player_status" not in st.session_state:
    st.session_state.player_status = "idle"
if "boss_status" not in st.session_state:
    st.session_state.boss_status = "idle"
if "round" not in st.session_state:
    st.session_state.round = 1
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 2
if "boss_hp" not in st.session_state:
    st.session_state.boss_hp = 5


col1, col2, col3 = st.columns([1, 2, 2])
with col1:
    st.image(check_player_status(st.session_state.player_status), width=300)
with col2:
    st.write("")
with col3:
    st.image(check_boss_status(st.session_state.boss_status))

col4, col5, col6 = st.columns([1, 1, 1])
with col4:
    if st.button("attack"):
        if st.session_state.round % 4 == 1:
            st.session_state.player_status = "attack"
            st.session_state.round += 1
            st.session_state.boss_hp -= 1
            st.rerun()
with col5:
    st.write("")
with col6:
    if st.button("진행"):
        if st.session_state.round % 4 == 3:
            st.session_state.round += 1
            st.session_state.player_status = "hit"
            st.session_state.boss_status = "attack"
            st.session_state.player_hp -= 1
            if st.session_state.player_hp <= 0:
                st.session_state.player_status = "death"
            st.rerun()
        elif (
            st.session_state.round % 4 == 2
            or st.session_state.round % 4 == 0
            and st.session_state.player_hp > 0
        ):
            st.session_state.round += 1
            st.session_state.player_status = "idle"
            st.session_state.player_status = "idle"
            st.rerun()
