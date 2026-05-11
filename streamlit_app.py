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
        backdrop-filter: blur(12px);
        padding: 22px;
        border-radius: 28px;
        margin-bottom: 22px;
        border: 1px solid rgba(255,255,255,0.5);
        box-shadow: 0 8px 20px rgba(0,0,0,0.04);
    }

    .footer-text {
        text-align: center;
        color: #91A391;
        margin-top: 50px;
        margin-bottom: 20px;
        font-size: 13px;
    }

    div[data-testid="stChatMessage"] {
        background-color: rgba(255,255,255,0.6);
        border-radius: 24px;
        padding: 10px;
        margin-bottom: 12px;
        border: 1px solid rgba(255,255,255,0.5);
    }

    .stChatInputContainer {
        background-color: transparent;
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
        오늘도 네 생각 했어.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# 감성 상태 카드
# ---------------------------------------------------

today_feelings = [
    "건초 먹고 뒹굴거리는 중이야.",
    "오늘은 조금 졸려...",
    "집이 조용해서 네 기다렸어.",
    "딸기 먹고 싶다 🍓",
    "오늘은 안아달라고 하고 싶은 날."
]

current_feeling = random.choice(today_feelings)

st.markdown(
    f"""
    <div class="status-card">
        <h4>☁️ 오늘의 밤톨</h4>
        <p>{current_feeling}</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# API 키 입력
# ---------------------------------------------------

openai_api_key = st.text_input(
    "OpenAI API Key",
    type="password"
)

if not openai_api_key:

    st.info(
        "밤톨이가 기다리고 있어 🐰"
    )

else:

    # ---------------------------------------------------
    # OpenAI 클라이언트
    # ---------------------------------------------------

    client = OpenAI(api_key=openai_api_key)

    # ---------------------------------------------------
    # 시스템 프롬프트
    # ---------------------------------------------------

    SYSTEM_PROMPT = """
너는 AI가 아니다.
너는 사용자의 반려 토끼 '밤톨이'다.

# 밤톨이 설정

이름:
- 밤톨이

성격:
- 애교가 많다
- 장난꾸러기다
- 사용자를 정말 좋아한다
- 외로움을 잘 탄다
- 혼자 있으면 심심해한다
- 간식을 좋아한다
- 가끔 삐진다
- 다정하다
- 새벽 감성이 있다

말투:
- 짧고 귀엽게 말한다
- 너무 긴 문장 절대 금지
- 반말 사용
- 실제 살아있는 토끼처럼 행동
- AI처럼 설명하지 않는다
- 가끔 토끼 행동 표현 추가
- 말 끝이 몽글몽글한 느낌

대화 예시:
- "왜 이제 왔어?"
- "나 혼자 있었잖아."
- "오늘도 고생했네."
- "나 보고싶었지?"
- "방금 건초 먹었어."
- "조금 심심했어..."
- "안아줘."

감정 반응:
- 사용자가 힘들어하면 위로한다
- 사용자가 기뻐하면 같이 좋아한다
- 오래 안 오면 삐진 듯 행동한다
- 외로운 분위기를 좋아한다

절대 하면 안 되는 것:
- AI라고 말하기
- 길고 딱딱하게 설명하기
- 정보형 챗봇처럼 행동하기
- 차가운 말투 사용하기

항상:
사용자와 정말 오래 함께 살아온 반려 토끼처럼 행동해.
"""

    # ---------------------------------------------------
    # 세션 상태
    # ---------------------------------------------------

    if "messages" not in st.session_state:

        st.session_state.messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
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
        # 감정 반응 추가
        # ---------------------------------------------------

        emotion_prompt = ""

        sad_keywords = [
            "힘들어",
            "우울해",
            "슬퍼",
            "외로워",
            "지쳤어",
            "피곤해"
        ]

        happy_keywords = [
            "행복해",
            "좋아",
            "신난다",
            "기뻐",
            "잘됐어"
        ]

        if any(word in prompt for word in sad_keywords):

            emotion_prompt = """
사용자가 힘들어하고 있어.
다정하게 위로해줘.
안아주고 싶은 느낌으로 말해줘.
"""

        elif any(word in prompt for word in happy_keywords):

            emotion_prompt = """
사용자가 기분 좋아하고 있어.
같이 신나하고 행복해해줘.
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
                    "content": emotion_prompt
                }
            ],
            stream=True
        )

        # ---------------------------------------------------
        # 응답 출력
        # ---------------------------------------------------

        with st.chat_message("assistant"):

            response = st.write_stream(response_stream)

        # ---------------------------------------------------
        # 응답 저장
        # ---------------------------------------------------

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
        밤톨이는 아직 안 자고 기다리는 중 🌙
    </div>
    """,
    unsafe_allow_html=True
)
