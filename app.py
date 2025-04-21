
import streamlit as st
import pandas as pd
from PIL import Image
import os
from datetime import datetime

st.set_page_config(layout="centered")

if "data" not in st.session_state:
    st.session_state.data = []
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

# 로고 표시
st.image("WORK_TALK_logo.png", width=150)

st.markdown("## 사진 1장 업로드 ➞ 질문 4개 응답 ➞ 저장 ➞ 다음 사진 순서대로 진행해 주세요.")

with st.form("entry_form", clear_on_submit=True):
    name = st.text_input("이름", key="name")
    dept = st.text_input("부서", key="dept")
    uploaded_file = st.file_uploader("📷 작업 사진 업로드", type=["jpg", "jpeg", "png"], key="photo")

    if uploaded_file is not None:
        st.image(uploaded_file, use_column_width=True)

        q1 = st.text_input("어떤 작업을 하고 있는 건가요?", key="q1")
        q2 = st.text_input("이 작업은 왜 위험하다고 생각하나요?", key="q2")
        q3 = st.radio("이 작업은 얼마나 자주 하나요?", ["연 1-2회", "반기 1-2회", "월 2-3회", "주 1회 이상", "매일"], key="q3")
        q4 = st.radio("이 작업은 얼마나 위험하다고 생각하나요?", [
            "약간의 위험: 일회용 밴드 치료 필요 가능성 있음",
            "조금 위험: 병원 치료 필요. 1~2일 치료 및 휴식",
            "위험: 보름 이상의 휴식이 필요한 중상 가능성 있음",
            "매우 위험: 불가역적 장애 또는 사망 가능성 있음"
        ], key="q4")

    submitted = st.form_submit_button("💾 저장하기")

if submitted and uploaded_file is not None:
    st.success("✅ 저장 완료! 다음 사진을 입력해 주세요.")
    st.session_state.data.append({
        "이름": name,
        "부서": dept,
        "파일명": uploaded_file.name,
        "질문1": q1,
        "질문2": q2,
        "질문3": q3,
        "질문4": q4,
        "업로드시간": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open(os.path.join("uploaded", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.download_button("📥 결과 다운로드 (CSV)", data=df.to_csv(index=False), file_name="worktalk_result.csv", mime="text/csv")
