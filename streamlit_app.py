import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="같이가요 여행 챗봇",
    page_icon="✈️",
)

# 제목
st.title("✈️ 같이가요 여행 챗봇")
st.caption("여행 일정 추천 · 맛집 추천 · 여행 준비를 도와드려요!")

# 사이드바
with st.sidebar:
    st.header("🌍 여행 정보 설정")

    travel_style = st.selectbox(
        "여행 스타일",
        ["힐링", "맛집 탐방", "액티비티", "감성 여행", "부모님과 여행", "혼자 여행"]
    )

    budget = st.selectbox(
        "예산",
        ["가성비", "보통", "럭셔리"]
    )

    days = st.selectbox(
        "여행 기간",
        ["1박 2일", "2박 3일", "3박 4일", "5박 이상"]
    )

# 설명
st.write(
    "원하는 여행지를 입력하면 여행 코스, 맛집, 준비물 등을 추천해드립니다 😊"
)

# API 키 입력
openai_api_key = st.text_input(
    "OpenAI API 키 입력",
    type="password"
)

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")

else:
    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 채팅 기록 저장
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": f"""
                너는 친절한 여행 전문 AI 챗봇이다.
                
                사용자의 여행 스타일은 '{travel_style}' 이다.
                예산 스타일은 '{budget}' 이다.
                여행 기간은 '{days}' 이다.

                사용자가 여행지를 입력하면:
                - 여행 일정 추천
                - 맛집 추천
                - 카페 추천
                - 준비물 추천
                - 여행 팁
                
                을 친절하고 보기 쉽게 추천해줘.
                
                답변은 반드시 한국어로 해줘.
                """
            }
        ]

    # 기존 메시지 출력
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # 채팅 입력
    if prompt := st.chat_input("어디로 여행 가고 싶나요?"):

        # 사용자 메시지 저장
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        # 사용자 메시지 출력
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # 응답 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
