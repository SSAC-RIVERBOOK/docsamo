# 이주 배경 청소년을 위한 게임형 한국어 학습 서비스

스토리텔링 기반의 게임형 한국어 맞춤법 학습 서비스입니다. LLM을 활용하여 동적으로 맞춤법 문제를 생성하고, 게임 형식으로 학습자에게 제공합니다.

## 주요 기능

- 스토리텔링 기반의 게임형 학습 환경 제공
- LLM을 활용한 동적 맞춤법 문제 생성
- 사용자의 학습 진행도 및 성취도 추적(예정)
- 맞춤형 피드백 제공(예정)

## 기술 스택

- Frontend: Streamlit
- Backend: Python
- Database: Redis
- AI/ML: LangChain

## 프로젝트 구조

```
├── Asset/          # 이미지 파일들
├── folktales/      # 예시 전래동화 데이터
├── pages/          # 스트림릿 페이지 컴포넌트
├── prompts/        # LLM 프롬프트 템플릿
├── utils.py        # 유틸리티 함수
├── redis_utils.py  # Redis 관련 유틸리티
├── langchain_utils.py  # LangChain 관련 유틸리티
└── start.py        # 메인 애플리케이션 진입점
```

## 실행 방법

1. Redis 설정
```bash
# Redis 서버 실행
docker run -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

# Redis 초기 데이터 설정
python initialize_redis.py
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
```bash
# .env 파일 생성
OPENAI_API_KEY=your_api_key
```

4. 애플리케이션 실행
```bash
streamlit run start.py
```
