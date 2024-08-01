import streamlit as st
from PIL import Image
import time
from utils import switch_page, show_user_status, show_user_data, show_menu

st.session_state.game_page = "round_select"

st.title("라운드 선택")


def load_image(img_path):
    return Image.open(img_path)


map_arr = [
    [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 3, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 2, 3, 0, 0, 3, 2, 2, 2, 2, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [3, 2, 2, 2, 2, 0, 0, 0, 3, 2, 2, 2, 2, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 3, 0, 0, 0, 2, 2, 2, 2, 2, 3, 0],
]

round_dict = {
    (6, 4): 1,
    (4, 0): 2,
    (2, 6): 3,
    (0, 11): 4,
    (2, 9): 5,
    (4, 8): 6,
    (6, 13): 7,
}

st.session_state.round = 0


def generate_map(map_arr, img_arr):
    img_size = img_arr[0].size[0]
    map_img = Image.new("RGBA", (img_size * len(map_arr[0]), img_size * len(map_arr)))

    for x in range(len(map_arr[0])):
        for y in range(len(map_arr)):
            map_img.paste(img_arr[map_arr[y][x]], (x * img_size, y * img_size))
    return map_img


img_path_arr = [
    "Asset/background.png",
    "Asset/ladder.png",
    "Asset/land.png",
    "Asset/fire.png",
]
img_arr = [load_image(img_path) for img_path in img_path_arr]

player_img = load_image("Asset/clover.png")
if "player_loc" not in st.session_state:
    st.session_state.player_loc = [0, 6]
map_img = generate_map(map_arr, img_arr)
player_size = player_img.size[0]

with st.container():
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("JOIN"):
            if (
                map_arr[st.session_state.player_loc[1]][st.session_state.player_loc[0]]
                == 3
            ):
                st.session_state.round = round_dict[
                    (st.session_state.player_loc[1], st.session_state.player_loc[0])
                ]
                switch_page("round_game")
        if st.button("LEFT"):
            if st.session_state.player_loc[0] - 1 < 0:
                pass
            elif (
                map_arr[st.session_state.player_loc[1]][
                    st.session_state.player_loc[0] - 1
                ]
                == 0
            ):
                pass
            else:
                st.session_state.player_loc[0] -= 1
    with col2:
        if st.button("UP"):
            if st.session_state.player_loc[1] - 1 < 0:
                pass
            elif (
                map_arr[st.session_state.player_loc[1] - 1][
                    st.session_state.player_loc[0]
                ]
                == 0
            ):
                pass
            else:
                st.session_state.player_loc[1] -= 1
            dir = True
        if st.button("DOWN"):
            if st.session_state.player_loc[1] + 1 >= len(map_arr):
                pass
            elif (
                map_arr[st.session_state.player_loc[1] + 1][
                    st.session_state.player_loc[0]
                ]
                == 0
            ):
                pass
            else:
                st.session_state.player_loc[1] += 1
            dir = False
    with col3:
        st.button("새로고침")
        if st.button("RIGHT"):
            if st.session_state.player_loc[0] + 1 >= len(map_arr[0]):
                pass
            elif (
                map_arr[st.session_state.player_loc[1]][
                    st.session_state.player_loc[0] + 1
                ]
                == 0
            ):
                pass
            else:
                st.session_state.player_loc[0] += 1

player_loc = [loc * player_size for loc in st.session_state.player_loc]
map_img.paste(player_img, player_loc, player_img)

st.image(map_img)

if map_arr[st.session_state.player_loc[1]][st.session_state.player_loc[0]] == 1:
    time.sleep(0.5)
    if dir:
        st.session_state.player_loc[1] -= 1
    else:
        st.session_state.player_loc[1] += 1
    st.rerun()

st.markdown(
    """
    <style>
    .block-container {
        width: 100vw;
        max-width: 816px;
        height: 100vh;
        max-height: 624px;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        border-radius: 10px;
    }
    .st-emotion-cache-1jicfl2 {
        padding-left: 0rem;
        padding-right: 0rem;
    }
    .st-emotion-cache-1jicfl2 {
        padding: 0rem 0rem 0rem;
    }
    .row-widget.stButton {
        display: flex;
        justify-content: center;
    }
    .st-emotion-cache-8542t9 {
        gap: 5rem;
    }
    .st-emotion-cache-bm2z3a {
        display: flex;
        width: 100%;
        overflow: auto;
        -webkit-box-align: center;
        align-items: center;
        justify-content: center;
        flex-direction: row;
    }
    .st-emotion-cache-1vt4y43 {
        width: 150px;
        height: 100px;
        background-color: #D9D9D9;
    }
    .st-emotion-cache-ocqkz7 {
        display: flex;
        flex-wrap: wrap;
        -webkit-box-flex: 1;
        flex-grow: 1;
        -webkit-box-align: stretch;
        align-items: stretch;
        gap: 0rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

show_menu(st.session_state.prev_page)
show_user_data(["유형1", "유형2", "유형3"], [3, 7, 10], True, 400)
show_user_status("이주배경어린이", "마지막 진행상황(챕터-라운드)", border=True)
