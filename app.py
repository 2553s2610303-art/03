import streamlit as st
from google import genai
from google.genai import types

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
    layout="centered"
)

st.title("💌 AI 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 상담 챗봇")

# -----------------------------
# API 키 불러오기
# -----------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("Secrets에 GOOGLE_API_KEY가 설정되지 않았습니다.")
    st.stop()

# -----------------------------
# Gemini Client 생성
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요 😊 연애 고민을 편하게 이야기해주세요!"
        }
    ]

# -----------------------------
# 이전 채팅 출력
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 사용자 입력
# -----------------------------
prompt = st.chat_input("연애 고민을 입력하세요...")

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

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # Gemini용 대화 변환
            history_text = ""

            for msg in st.session_state.messages:
                role = "사용자" if msg["role"] == "user" else "상담사"
                history_text += f"{role}: {msg['content']}\n"

            system_prompt = """
            너는 따뜻하고 공감 능력이 뛰어난 연애상담 AI야.
            사용자의 감정을 존중하고,
            현실적이고 부드러운 조언을 제공해.
            절대 공격적이거나 무례하게 말하지 마.
            """

            full_prompt = f"""
            {system_prompt}

            아래는 지금까지의 대화야.

            {history_text}

            상담사 답변:
            """

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=500
                )
            )

            ai_response = response.text

            message_placeholder.markdown(ai_response)

            # AI 응답 저장
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_response
                }
            )

        except Exception as e:
            error_message = f"오류가 발생했습니다: {e}"

            message_placeholder.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message
                }
            )

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.header("⚙️ 설정")

    if st.button("채팅 기록 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "안녕하세요 😊 새로운 고민을 이야기해주세요!"
            }
        ]
        st.rerun()

    st.markdown("---")
    st.markdown("### 💡 커스터마이징")

    st.markdown("""
    system_prompt 부분만 수정하면:
    - 진로 상담
    - 공부 코치
    - 심리 상담
    - 영어 튜터
    - 운동 코치
    
    등으로 쉽게 변경할 수 있습니다.
    """)
