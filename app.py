import streamlit as st

# --- 1. 사이드바 디자인 설정 ---
st.sidebar.header("🎨 디자인 설정")
# 배경색과 글자색을 사장님이 직접 조절할 수 있습니다.
bg_color = st.sidebar.color_picker("배경색 선택", "#000000") # 기본 블랙
text_color = st.sidebar.color_picker("글자색 선택", "#FFFFFF") # 기본 화이트

# --- 2. 강력한 CSS 적용 (글자색 강제 고정) ---
st.markdown(f"""
    <style>
    /* 전체 배경색 적용 */
    .stApp {{
        background-color: {bg_color};
    }}
    
    /* 제목, 본문, 라벨 등 모든 글자색을 선택한 색으로 강제 적용 */
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp span, .stApp label {{
        color: {text_color} !important;
    }}

    /* 리뷰 입력창(Textarea): 배경 화이트, 글씨 블랙으로 가독성 1순위 보호 */
    textarea {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        font-size: 1.1rem !important;
        border: 2px solid #FF4B4B !important;
    }}
    
    /* 입력창 내부의 안내 문구(Placeholder) 색상 */
    textarea::placeholder {{
        color: #888888 !important;
    }}

    /* 프라이버시 보호: 상단 헤더, 메뉴, 하단 푸터 완전 제거 */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 앱 메인 콘텐츠 ---
st.title("🚀 AI 리뷰 마스터")
st.markdown("### 사장님의 비즈니스를 위한 최적의 리뷰를 생성합니다.")

# 입력창
review_input = st.text_area(
    "어떤 리뷰를 만들어드릴까요?", 
    placeholder="예: 맛있는 커피, 친절한 매장, 사진 찍기 좋은 곳",
    height=200
)

# 생성 버튼
if st.button("AI 리뷰 생성하기"):
    if review_input:
        st.success("리뷰 생성이 완료되었습니다!")
        # 결과 창 배경과 글씨도 설정에 맞춰 보입니다.
        st.markdown(f"""
            <div style="padding:20px; border-radius:10px; border:1px solid {text_color}; color:{text_color};">
                <strong>[생성된 리뷰 결과]</strong><br><br>
                여기에 AI가 생성한 멋진 리뷰 내용이 표시됩니다.
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("먼저 내용을 입력해 주세요!")