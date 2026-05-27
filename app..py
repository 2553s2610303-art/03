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
st.caption("Gemini 2.5 Flash Lite 기반")

# -----------------------------
# API KEY
# -----------------------------
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("Secrets에 GOOGLE_API_KEY를 설정해주세요.")
    st.stop()

# -----------------------------
# Gemini Client
# -----------------------------
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# -----------------------------
# 세션 초기화
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "안녕하세요 😊 연애 고민을 편하게 이야기해주세요!"
        }
    ]

# -----------------------------
# 채팅 출력
# -----------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# 입력창
# -----------------------------
prompt = st.chat_input("메시지를 입력하세요...")

if prompt:

    # 입력 길이 제한
    if len(prompt) > 1000:
        st.warning("1000자 이하로 입력해주세요.")
        st.stop()

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

    # AI 응답
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        try:
            # 이전 대화 기록 구성
            history_text = ""

            for msg in st.session_state.messages:
                role = "사용자" if msg["role"] == "user" else "상담사"
                history_text += f"{role}: {msg['content']}\n"

            # 시스템 프롬프트
            system_prompt = """
            너는 따뜻하고 공감 능력이 뛰어난 연애상담 AI야.
            사용자의 감정을 존중하고 현실적인 조언을 제공해.
            친절하고 부드럽게 대답해.
            """

            full_prompt = f"""
            {system_prompt}

            아래는 지금까지의 대화 내용이야.

            {history_text}

            상담사 답변:
            """

            # Gemini 호출
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=500
                )
            )

            # 안전한 응답 처리
            ai_response = ""

            if response.candidates:
                candidate = response.candidates[0]

                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, "text") and part.text:
                            ai_response += part.text

            if not ai_response.strip():
                ai_response = "답변을 생성하지 못했습니다. 다시 시도해주세요."

            # 출력
            message_placeholder.markdown(ai_response)

            # 저장
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_response
                }
            )

        except Exception as e:

            error_message = f"""
오류가 발생했습니다.

가능한 원인:
- API 키 오류
- Gemini 서버 오류
- 입력 제한 초과
- 일시적인 네트워크 문제

에러 내용:
{str(e)}
"""

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

    st.header("⚙️ 메뉴")

    if st.button("채팅 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "안녕하세요 😊 새로운 고민을 이야기해주세요!"
            }
        ]
        st.rerun()

    st.markdown("---")

    st.markdown("""
### 💡 사용 방법
- 연애 고민 상담
- 썸 고민
- 이별 고민
- 재회 고민
- 인간관계 고민

등 자유롭게 질문하세요.
""")
