import streamlit as st
st.title('잠 잘자는 법')
st.write('import streamlit as st

st.set_page_config(page_title="잠 잘자는 법", page_icon="🛌")

st.title("💤 잠 잘자는 법 추천")

# 수면 관련 팁 리스트
sleep_tips = [
    "📅 규칙적인 수면 시간 지키기",
    "📵 자기 전 전자기기 멀리하기",
    "☕ 카페인 섭취 피하기",
    "🏃‍♂️ 낮에 가벼운 운동하기",
    "🛁 따뜻한 샤워나 목욕",
    "🧘‍♀️ 명상이나 심호흡으로 마음 안정",
    "🌙 방을 어둡게 하고 시원하게 유지",
]

# 사용자가 보고 싶은 팁 선택
selected_tip = st.selectbox("보고 싶은 수면 팁 선택", sleep_tips)

st.success(f"추천 팁: {selected_tip}")')
