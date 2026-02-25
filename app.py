import streamlit as st
from openai import OpenAI


# 1. 페이지 설정 및 디자인
st.set_page_config(page_title="리뷰 마스터 AI", page_icon="📝")
st.markdown(
    """
    <style>
    .main {
        background-color: #f6f7f9;
    }

    :root {
        --point-color: #03C75A;
    }

    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: var(--point-color);
        color: white;
        font-weight: 600;
        border: none;
        box-shadow: 0 3px 8px rgba(3, 199, 90, 0.35);
    }

    .stButton>button:hover {
        background-color: #02b250;
    }

    .stTextArea textarea {
        border-radius: 10px;
        border: 1px solid #dfe3e8;
        background-color: #ffffff;
    }

    .result-box {
        background-color: #e6fff1;
        border: 1px solid #03C75A;
        padding: 1.1rem 1rem;
        border-radius: 12px;
        margin-top: 0.8rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. 사이드바 설정
with st.sidebar:
    st.title("⚙️ 설정")
    api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
    st.info("키는 본인의 OpenAI 계정에서 발급받은 것을 사용하세요.")
    st.caption(
        "이 앱은 사용자 본인의 API Key를 사용하므로 안전하며, "
        "개발자는 어떤 데이터도 저장하지 않습니다."
    )


def generate_reply(api_key: str, review: str, tone: str) -> str:
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "너는 베테랑 온라인 쇼핑몰 사장님이야. "
                    f"고객 리뷰에 대해 {tone} 말투로 감사와 공감을 담아 답글을 작성해줘. "
                    "가게의 신뢰가 느껴지도록 부드럽지만 단호하게 안내해주고, "
                    "이모지도 자연스럽게 섞어줘."
                ),
            },
            {"role": "user", "content": review},
        ],
    )
    return response.choices[0].message.content


# 3. 메인 화면 UI
st.title("🚀 리뷰 마스터 AI")
st.subheader("리뷰 답글 다는 시간을 1분으로 줄여드립니다.")

with st.expander("📖 사용 가이드", expanded=False):
    st.markdown(
        """
        **1️⃣ OpenAI API Key 발급 방법**
        - `https://platform.openai.com` 에 접속해 로그인합니다.
        - 상단 메뉴에서 **API Keys** 메뉴로 이동합니다.
        - **Create new secret key** 버튼을 눌러 새 키를 발급받습니다.
        - 발급된 키를 복사해 이 앱의 **사이드바 입력창**에 붙여넣습니다.

        **2️⃣ 리뷰 복사 방법 (예시 – 네이버 스마트스토어)**
        - 스마트스토어 판매자센터에서 **상품 리뷰 관리** 메뉴로 이동합니다.
        - 답글을 달고 싶은 리뷰의 내용을 마우스로 드래그하여 선택합니다.
        - `Ctrl + C` (또는 마우스 우클릭 → 복사)를 눌러 복사합니다.
        - 이 화면의 **고객 리뷰 입력 칸**에 `Ctrl + V`로 붙여넣습니다.

        **3️⃣ 답글 활용 팁**
        - 필요한 경우, 생성된 답글을 조금 수정해서 매장 톤에 딱 맞게 다듬어 사용하세요.
        - 자주 쓰는 멘트는 메모장에 저장해두고, AI가 만든 답글과 섞어 쓰면 더 효율적입니다.
        """
    )

review_content = st.text_area(
    "고객 리뷰를 여기에 붙여넣으세요:",
    placeholder="예: 배송이 너무 느려요. 상품은 괜찮네요.",
    height=150,
)

col1, _ = st.columns(2)
with col1:
    tone = st.radio(
        "원하는 말투를 선택하세요:",
        ["친절하고 따뜻하게", "유머러스하고 위트있게", "정중하고 전문적으로"],
    )

# 4. 답글 생성 로직
result = None
if st.button("✨ AI 답글 생성하기"):
    if not api_key:
        st.error("왼쪽 사이드바에 API Key를 먼저 입력해주세요!")
    elif not review_content:
        st.warning("리뷰 내용을 입력해주세요.")
    else:
        try:
            with st.spinner("AI가 사장님 빙의 중... 잠시만 기다려주세요."):
                result = generate_reply(api_key, review_content, tone)

            st.success("답글이 완성되었습니다! 아래 내용을 복사해서 사용해 주세요.")
            st.balloons()
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# 5. 결과 출력 영역 (항상 같은 위치에 표시)
st.markdown("### ✨ AI 답글 결과")

if result:
    # 시각적으로 강조된 박스 안에 결과 표시
    st.markdown(
        "<div class='result-box'>"
        "<span style='font-size:0.9rem; font-weight:600;'>복사용 텍스트</span>",
        unsafe_allow_html=True,
    )
    st.text_area(
        label="",
        value=result,
        height=220,
        key="result_text_area",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("위에 고객 리뷰를 입력하고, 말투를 선택한 뒤 **AI 답글 생성하기** 버튼을 눌러보세요.")
