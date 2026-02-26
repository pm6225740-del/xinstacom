import streamlit as st
import yt_dlp
import os
import tempfile
import random

# === 1. 페이지 기본 설정 ===
# 초기 로딩 시 우측 상단 메뉴바를 최소화하기 위해 initial_sidebar_state="collapsed" 적용
st.set_page_config(page_title="SNS 미디어 허브", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

# === 2. 고급 CSS 디자인 커스텀 ===
# 우측 상단 쓸모없는 툴바 제거 및 전체적인 가독성/디자인 업그레이드
st.markdown("""
    <style>
    /* Streamlit 기본 메뉴 숨기기 */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* 폰트 및 배경 설정 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] {
        font-family: 'Pretendard', sans-serif;
    }
    .main { background-color: #0b0e14; }
    
    /* 세련된 광고/공지 배너 (그라데이션 효과) */
    .premium-banner {
        background: linear-gradient(135deg, #4A00E0 0%, #8E2DE2 100%);
        border-radius: 12px;
        padding: 25px 20px;
        text-align: center;
        color: white;
        font-weight: 800;
        font-size: 1.1rem;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(142, 45, 226, 0.3);
        letter-spacing: 0.5px;
    }
    
    /* 사이드 배너 (스토어 홍보용 등) */
    .side-banner {
        background: #1a1d24;
        border: 1px solid #2d3139;
        border-radius: 10px;
        padding: 30px 10px;
        text-align: center;
        color: #a0aabf;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }
    .side-banner:hover {
        border-color: #8E2DE2;
        color: white;
        transform: translateY(-2px);
    }
    
    /* 탭 디자인 강조 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-size: 1.1rem;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# === 3. 백엔드 로직 ===
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'outtmpl': tempfile.gettempdir() + '/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            return file_path, info.get('title', 'video')
    except Exception as e:
        return None, str(e)

# 50개 더미 랭킹 데이터 생성 함수
@st.cache_data
def generate_50_trends():
    platforms = ["Instagram", "X (Twitter)"]
    keywords = ["핫플", "강아지", "고양이", "다이어트 레시피", "직캠", "속보", "유머", "챌린지", "운동 루틴", "브이로그", "O.OPICS 폰케이스 리뷰"]
    trends = []
    
    for i in range(1, 51):
        trends.append({
            "rank": i,
            "platform": random.choice(platforms),
            "title": f"실시간 화제의 {random.choice(keywords)} 영상",
            "count": f"{random.randint(10, 999) / 10.0:.1f}k",
            # 플레이 테스트용 무료 공개 샘플 영상 URL
            "video_url": "https://www.w3schools.com/html/mov_bbb.mp4" 
        })
    return trends

# === 4. 레이아웃 및 UI 구성 ===
left_ad, main_content, right_ad = st.columns([1.5, 7, 1.5])

# [좌측 광고]
with left_ad:
    st.markdown('<div class="side-banner">✨<br><br><b>O.OPICS</b><br>트렌디한 폰 액세서리<br>구경하기</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-banner">🎯<br><br>스폰서 배너<br>영역</div>', unsafe_allow_html=True)

# [우측 광고]
with right_ad:
    st.markdown('<div class="side-banner">📺<br><br>구글 애드센스<br>광고 자리</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-banner">🤝<br><br>제휴/입점 문의</div>', unsafe_allow_html=True)

# [중앙 메인 영역]
with main_content:
    st.markdown('<div class="premium-banner">🚀 고화질 SNS 영상 다운로더 & 실시간 트렌드 분석 허브</div>', unsafe_allow_html=True)
    
    # 탭 구성
    tab_dl, tab_rank = st.tabs(["📥 초고속 다운로드", "🔥 실시간 TOP 50 랭킹 영상보기"])
    
    # --- 탭 1: 다운로드 ---
    with tab_dl:
        st.write("")
        url_input = st.text_input(
            "👇 다운로드할 링크(URL)를 아래에 붙여넣으세요.",
            placeholder="예: https://x.com/username/status/123456..."
        )
        
        if st.button("지금 추출하기", type="primary", use_container_width=True):
            if url_input:
                with st.spinner('서버에서 고화질 영상을 가져오고 있습니다. 잠시만 대기해주세요...'):
                    file_path, title_or_error = download_video(url_input)
                    
                    if file_path and os.path.exists(file_path):
                        st.success(f"🎉 성공적으로 추출했습니다! ({title_or_error[:20]}...)")
                        with open(file_path, "rb") as f:
                            st.download_button(
                                label="💾 내 기기에 저장하기",
                                data=f,
                                file_name=os.path.basename(file_path),
                                mime="video/mp4",
                                use_container_width=True
                            )
                    else:
                        st.error(f"❌ 다운로드에 실패했습니다. 링크를 다시 확인해주세요.\n(상세 오류: {title_or_error})")
            else:
                st.warning("먼저 링크를 입력해주세요.")

    # --- 탭 2: 실시간 랭킹 (영상 바로보기 추가) ---
    with tab_rank:
        st.markdown("💡 **목록을 클릭하면 영상을 바로 시청**할 수 있습니다. (현재는 샘플 영상이 재생됩니다.)")
        
        trends_data = generate_50_trends()
        
        for t in trends_data:
            # expander를 사용해 클릭 시 영상이 펼쳐지도록 구현
            expander_title = f"🏅 {t['rank']}위 | [{t['platform']}] {t['title']} | 📈 {t['count']}회 시청"
            with st.expander(expander_title):
                # 1. 영상 플레이어 표시
                st.video(t['video_url'])
                
                # 2. 개별 영상 다운로드 버튼 (샘플)
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.caption(f"이 영상은 {t['platform']}에서 현재 가장 핫한 트렌드입니다.")
                with col2:
                    st.download_button(
                        label="이 영상 다운로드",
                        data=b"dummy video data", # 실제 서비스 시 이 부분을 추출된 파일로 변경
                        file_name=f"trend_video_{t['rank']}.mp4",
                        key=f"dl_btn_{t['rank']}",
                        use_container_width=True
                    )

# --- 푸터 ---
st.markdown("<br><hr style='border-color: #2d3139;'>", unsafe_allow_html=True)
st.caption("<div style='text-align:center; color:#666;'>© 2026 SNS Media Hub. All rights reserved. | 이용약관 | DMCA | 개인정보처리방침</div>", unsafe_allow_html=True)