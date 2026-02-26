import streamlit as st

# --- 1. 테마 및 배경 설정 ---
st.sidebar.header("🎨 디자인 설정")
bg_color = st.sidebar.color_picker("배경색 선택", "#000000")
text_color = st.sidebar.selectbox("글자색 선택", ["#FFFFFF", "#000000"])

# --- 2. CSS 스타일 적용 (프라이버시 및 가독성) ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    textarea {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }}
    /* 프라이버시 보호: 메뉴 및 푸터 숨기기 */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 앱 콘텐츠 ---
st.title("🚀 AI 리뷰 마스터")
review_input = st.text_area("리뷰 내용을 입력하세요")

if st.button("생성하기"):
    st.success("리뷰가 생성되었습니다!")