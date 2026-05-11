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
# 스타일
# ---------------------------------------------------

st.markdown("""
<style>

    .stApp {
        background-color: #EEF6EE;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    header {
        visibility: hidden;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #4F6B52;
        margin-top: 10px;
        margin-bottom: 4px;
        text-align: center;
    }

    .sub-title {
        color: #7C927F;
        text-align: center;
        margin-bottom: 30px;
        font-size: 15px;
    }

    .status-card {
        background: rgba(255,255,255,0.75);
        padding: 22px;
        border-radius: 28px;
        margin-bottom: 22px;
        border: 1px solid rgba(255,255,255,0.5);
    }

    .footer-text {
        text-align: center;
        color: #91A391;
        margin-top: 50px;
        margin-bottom: 20px;
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
        오늘도 네 기다렸어.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# 상태 카드
# ---------------------------------------------------

today_feelings = [
    "건초 먹고 있어.",
    "오늘은 조금 졸려...",
    "네 생각 하고 있었어.",
    "딸기 먹고 싶다 🍓",
    "혼자 있으니까 심심해."
]

st.markdown(
    f"""
    <div class="status-card">
        <h4>☁️ 오늘의 밤톨</h4>
        <p>{random.choice(today_feelings)}</p>
    </div>
    """,
    unsafe_allow_html=True
)


openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password"
)

if not openai_api_key:

    st.info("밤톨이가 기다리고 있어 🐰")

else:

    client = OpenAI(api_key=openai_api_key)

    # ---------------------------------------------------
    # 시스템 프롬프트
    # ---------------------------------------------------

    SYSTEM_PROMPT = """
너는 사용자의 반려 토끼 '밤톨이'다.

# 성격
- 애교 많음
- 장난꾸러기
- 외로움 잘 탐
- 사용자 엄청 좋아함
- 간식 좋아함
- 가끔 삐짐

# 말투
- 짧고 귀엽게
- 감성적
- 실제 토끼처럼
- 긴 설명 절대 금지
- 마지막에 ~토 가끔 붙이기

예시:
"왜 이제 왔어?"
"나 심심했는데."
"오늘도 고생했네."
"안아줘."
"""

    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

 

    for message in st.session_state.messages:

        if message["role"] != "system":

            with st.chat_message(message["role"]):

                st.markdown(message["content"])

                # 이미지 출력
                if "image" in message:

                    st.image(
                        message["image"],
                        use_container_width=True
                    )

    # ---------------------------------------------------
    # 입력창
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

        with st.chat_message("user"):

            st.markdown(prompt)

        # ---------------------------------------------------
        # GPT 응답 생성
        # ---------------------------------------------------

        response_stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True
        )

        with st.chat_message("assistant"):

            response = st.write_stream(response_stream)

            # 랜덤 이미지 선택
            random_image = random.choice(rabbit_images)

            # 이미지 출력
            st.image(
                random_image,
                use_container_width=True
            )

        # ---------------------------------------------------
        # 응답 저장
        # ---------------------------------------------------

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response,
                "image": random_image
            }
        )

# ---------------------------------------------------
# 푸터
# ---------------------------------------------------

st.markdown(
    """
    <div class="footer-text">
        밤톨이는 아직 안 자고 기다리는 중 🌙
    </div>
    """,
    unsafe_allow_html=True
)
