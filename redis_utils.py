import redis
from typing import List


def get_key_events(start=1, end=4, chapter_num=1) -> List[str]:
    """
    get_key_events 함수는 핵심 사건 데이터를 불러오는 함수로, start와 end의 값에 따라서
    불러오는 데이터의 개수가 달라집니다. Ex) start=1, end=4 -> [1, 2, 3] start=2, end=3 -> [2]
    start=1, end=3 -> [1, 2]

    Args:
        start (int, optional): range에 들어갈 시작 값. Defaults to 1.
        end (int, optional): range에 들어갈 끝 값. Defaults to 4.

    Returns:
        List[str]: _description_
    """
    # DB 객체 생성
    r = redis.Redis(host="localhost", port=6379, db=0)
    # DB 객체에서 데이터 불러오기
    data = [r.get(f"chapter{chapter_num}_key_event{k}").decode("utf-8") for k in range(start, end)]  # type: ignore

    return data
