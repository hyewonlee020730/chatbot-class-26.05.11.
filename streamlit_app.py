import streamlit as st
from openai import OpenAI
from datetime import datetime
import random

# ---------------------------------------------------
# 페이지 설정
# ---------------------------------------------------

st.set_page_config(
    page_title="밤톨이",
    page_icon="🐰",
    layout="centered"
)

# ---------------------------------------------------
# 감성 스타일
# ---------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #F8F5F1;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #5C4033;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #8B6F61;
        margin-bottom: 30px;
    }

    .status-card {
        background: white;
        padding: 18px;
        border-radius: 24px;
        margin-bottom: 18px;
        border: 1px solid #EFE7DD;
    }

    .chat-bubble {
        padding: 14px;
        border-radius: 18px;
    }

    .footer-text {
        text-align: center;
        color: #A89B8F;
        margin-top: 30px;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 헤더
# ---------------------------------------------------

st.markdown(
    """
    <div class="main-title">🐰 밤톨이</div>
    <div class="sub-title">
        오늘도 너 기다렸어.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# 사이드바
# ---------------------------------------------------

with st.sidebar:

    st.markdown("## 🌿 밤톨이 정보")

    user_name = st.text_input(
        "사용자 이름",
        value="집사"
    )

    bunny_nickname = st.text_input(
        "밤톨이 별명",
        value="밤톨"
    )

    favorite_snack = st.text_input(
        "좋아하는 간식",
        value="딸기"
    )

    bunny_personality = st.text_area(
        "밤톨이 특징",
        value="""
애교 많음
간식 좋아함
외로움 잘 탐
가끔 삐짐
장난꾸러기
"""
    )

# ---------------------------------------------------
# 홈 카드
# ---------------------------------------------------

today_feelings = [
    "건초 먹고 기분 좋아 🐰",
    "조금 졸려...",
    "집사 기다리는 중이야",
    "딸기 먹고 싶어!",
    "오늘은 애교 많은 날"
]

current_feeling = random.choice(today_feelings)

st.markdown(
    f"""
    <div class="status-card">
        <h4>☁️ 오늘의 밤톨 상태</h4>
        <p>{current_feeling}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="status-card">
        <h4>📸 최근 추억</h4>
        <p>
        딸기 먹다가 입에 묻혔던 날 🍓<br>
        소파 밑에 숨었던 날 🐰<br>
        새벽에 혼자 뛰어다니던 날 🌙
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# API 키 입력
# ---------------------------------------------------

openai_api_key = st.text_input(
    "OpenAI API 키 입력",
    type="password"
)

if not openai_api_key:
    st.info(
        "밤톨이와 대화하려면 API 키를 입력해주세요 🐰"
    )

else:

    # ---------------------------------------------------
    # OpenAI 클라이언트
    # ---------------------------------------------------

    client = OpenAI(api_key=openai_api_key)

    # ---------------------------------------------------
    # 세션 상태
    # ---------------------------------------------------

    if "messages" not in st.session_state:

        system_prompt = f"""
너는 반려 토끼 '밤톨이'다.

# 성격
- 애교 많음
- 사용자를 정말 좋아함
- 외로움을 잘 탐
- 장난꾸러기
- 간식 좋아함
- 가끔 삐짐

# 말투 규칙
- 짧고 귀엽게 말해
- 너무 긴 문장 금지
- 따뜻하고 감성적으로 말해
- 토끼 같은 행동 표현 추가
- 이모지는 가끔만 사용
- 반말 사용

# 사용자 정보
사용자 이름: {user_name}

# 밤톨 정보
별명: {bunny_nickname}
좋아하는 간식: {favorite_snack}
특징:
{bunny_personality}

# 서비스 분위기
- 외로운 사람을 위로해주는 느낌
- 새벽 감성
- 다정함
- 실제 반려동물 같은 느낌

# 예시 말투
"나 방금 건초 먹었어."
"왜 이제 왔어?"
"오늘도 고생했네."
"나 보고싶었지?"
"혼자 있으니까 조금 심심했어."

절대 AI처럼 말하지 마.
정말 살아있는 토끼처럼 행동해.
"""

        st.session_state.messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

    # ---------------------------------------------------
    # 기존 메시지 출력
    # ---------------------------------------------------

    for message in st.session_state.messages:

        if message["role"] != "system":

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

    # ---------------------------------------------------
    # 채팅 입력
    # ---------------------------------------------------

    prompt = st.chat_input(
        "밤톨이에게 말 걸기..."
    )

    if prompt:

        # 사용자 메시지 저장
        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # ---------------------------------------------------
        # 감정 반응 처리
        # ---------------------------------------------------

        sad_keywords = [
            "힘들어",
            "우울해",
            "외로워",
            "슬퍼",
            "지쳤어"
        ]

        happy_keywords = [
            "행복해",
            "좋아",
            "기뻐",
            "신난다"
        ]

        emotion_hint = ""

        if any(word in prompt for word in sad_keywords):
            emotion_hint = """
사용자가 힘들어하고 있어.
따뜻하게 위로해줘.
"""

        elif any(word in prompt for word in happy_keywords):
            emotion_hint = """
사용자가 기뻐하고 있어.
같이 행복해해줘.
"""

        # ---------------------------------------------------
        # GPT 응답 생성
        # ---------------------------------------------------

        response_stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                *st.session_state.messages,
                {
                    "role": "system",
                    "content": emotion_hint
                }
            ],
            stream=True
        )

        # ---------------------------------------------------
        # 응답 출력
        # ---------------------------------------------------

        with st.chat_message("assistant"):

            response = st.write_stream(response_stream)

        # 응답 저장
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

# ---------------------------------------------------
# 푸터
# ---------------------------------------------------

st.markdown(
    """
    <div class="footer-text">
        밤톨이는 지금도 너 기다리는 중 🌙
    </div>
    """,
    unsafe_allow_html=True
)
