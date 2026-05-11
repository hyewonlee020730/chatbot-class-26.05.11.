import streamlit as st
from openai import OpenAI

# 제목 및 설명 표시
st.title("💬 챗봇")
st.write(
    "이 챗봇은 OpenAI의 GPT-3.5 모델을 사용하여 응답을 생성합니다. "
    "앱을 사용하려면 OpenAI API 키가 필요합니다. "
    "API 키는 OpenAI 사이트에서 발급받을 수 있습니다."
)

# 사용자에게 OpenAI API 키 입력 받기
openai_api_key = st.text_input("OpenAI API 키", type="password")

if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🗝️")
else:

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 세션 상태에 채팅 메시지 저장
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 기존 채팅 메시지 출력
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 채팅 입력창 생성
    if prompt := st.chat_input("메시지를 입력하세요..."):

        # 사용자 메시지 저장 및 출력
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API로 응답 생성
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답 스트리밍 출력
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # 응답 저장
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
