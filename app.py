import streamlit as st

# --- 1. 배경색 및 테마 설정 (사이드바) ---
st.sidebar.header("🎨 디자인 설정")
bg_color = st.sidebar.color_picker("배경색을 선택하세요", "#000000") # 기본값 블랙
text_color = st.sidebar.selectbox("글자색을 선택하세요", ["#FFFFFF", "#F8F9FA", "#E0E0E0", "#000000"])

# --- 2. 동적 스타일 적용 (CSS) ---
st.markdown(f"""
    <style>
    /* 전체 배경색 및 기본 글자색 설정 */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* 리뷰 입력창 스타일: 배경 화이트, 글씨 블랙 고정 */
    textarea {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-size: 1.1rem !important;
        border-radius: 10px !important;
    }}
    
    /* 입력창 라벨(제목) 글자색 */
    .stTextArea label p {{
        color: {text_color} !important;
        font-weight: bold;
    }}

    /* 버튼 스타일 커스텀 */
    .stButton>button {{
        border-radius: 20px;
        background-color: #FF4B4B;
        color: white;
    }}

    /* 프라이버시 설정: 헤더/푸터 숨기기 */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 앱 콘텐츠 영역 ---
st.title("🚀 AI 리뷰 마스터")
st.write("사장님만의 특별한 리뷰를 생성해보세요.")

review_input = st.text_area("여기에 리뷰 내용을 입력하거나 키워드를 적어주세요.", placeholder="예: 커피가 맛있고 사장님이 친절해요!")

if st.button("AI 리뷰 생성하기"):
    st.success("멋진 리뷰가 생성되었습니다! (여기에 AI 로직이 들어갑니다)")
    # 생성된 결과 출력 부분
    st.markdown(f"<div style='color:{text_color}'>여기에 생성된 리뷰 결과가 표시됩니다.</div>", unsafe_allow_html=True)