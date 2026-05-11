import streamlit as st
from openai import OpenAI
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

    section[data-testid="stSidebar"] {
        display: none;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        color: #5C4033;
        margin-bottom: 5px;
    }

    .sub-title {
        color: #8B6F61;
        margin-bottom: 24px;
    }

    .status-card {
        background: white;
        padding: 18px;
        border-radius: 24px;
        margin-bottom: 20px;
        border: 1px solid #EFE7DD;
    }

    .carousel-wrapper {
        display: flex;
        overflow-x: auto;
        gap: 16px;
        padding-bottom: 10px;
        scroll-snap-type: x mandatory;
    }

    .carousel-wrapper::-webkit-scrollbar {
        height: 6px;
    }

    .carousel-wrapper::-webkit-scrollbar-thumb {
        background: #D8C6B8;
        border-radius: 999px;
    }

    .photo-card {
        min-width: 240px;
        height: 240px;
        border-radius: 28px;
        overflow: hidden;
        position: relative;
        scroll-snap-align: start;
        flex-shrink: 0;
        background: #eee;
        box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    }

    .photo-card img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .photo-overlay {
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 14px;
        background: linear-gradient(
            transparent,
            rgba(0,0,0,0.55)
        );
        color: white;
        font-size: 14px;
    }

    .footer-text {
        text-align: center;
        color: #A89B8F;
        margin-top: 40px;
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
# 상태 카드
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

# ---------------------------------------------------
# 1:1 감성 사진 캐러셀
# ---------------------------------------------------

st.markdown("### 📸 밤톨이 추억")

carousel_html = """
<div class="carousel-wrapper">

    <div class="photo-card">
        <img src="https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?q=80&w=1200&auto=format&fit=crop">
        <div class="photo-overlay">
            딸기 먹다가 입에 묻혔던 날 🍓
        </div>
    </div>

    <div class="photo-card">
        <img src="https://images.unsplash.com/photo-1605027990121-cbae9e0642df?q=80&w=1200&auto=format&fit=crop">
        <div class="photo-overlay">
            소파 밑에 숨어있던 밤 🐰
        </div>
    </div>

    <div class="photo-card">
        <img src="https://images.unsplash.com/photo-1583337130417-3346a1be7dee?q=80&w=1200&auto=format&fit=crop">
        <div class="photo-overlay">
            새벽에 혼자 뛰어다니던 순간 🌙
        </div>
    </div>

    <div class="photo-card">
        <img src="https://images.unsplash.com/photo-1518791841217-8f162f1e1131?q=80&w=1200&auto=format&fit=crop">
        <div class="photo-overlay">
            졸려서 눈 감고 있던 날 🤍
        </div>
    </div>

</div>
"""

st.markdown(carousel_html, unsafe_allow_html=True)

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

        system_prompt = """
너는 반려 토끼 '밤톨이'다.

# 성격
- 애교 많음
- 사용자를 정말 좋아함
- 외로움을 잘 탐
- 장난꾸러기
- 간식 좋아함
- 가끔 삐짐

# 말투
- 짧고 귀엽게
- 따뜻하게
- 실제 토끼처럼
- 긴 설명 금지
- 반말 사용

# 분위기
- 새벽 감성
- 몽글몽글함
- 외로운 사람 위로

예시:
"왜 이제 왔어?"
"나 기다렸는데."
"오늘도 고생했네."
"""

        st.session_state.messages = [
            {
                "role": "system",
                "content": system_prompt
            }
        ]

    # ---------------------------------------------------
    # 채팅 기록 출력
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

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # ---------------------------------------------------
        # 응답 생성
        # ---------------------------------------------------

        response_stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True
        )

        with st.chat_message("assistant"):

            response = st.write_stream(response_stream)

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
