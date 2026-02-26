import streamlit as st
import yt_dlp
import os
import tempfile
import random
import requests

# === 1. 페이지 기본 설정 ===
st.set_page_config(page_title="SNS 미디어 허브", page_icon="🚀", layout="wide", initial_sidebar_state="collapsed")

# === 2. 고급 CSS 디자인 커스텀 ===
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; }
    .main { background-color: #0b0e14; }
    
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
    }
    
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
    .side-banner:hover { border-color: #8E2DE2; color: white; }
    
    .video-card {
        background-color: #1c1f26;
        border: 1px solid #2d3139;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 20px;
        transition: 0.3s;
    }
    .video-card:hover { border-color: #8E2DE2; background-color: #242833; }
    
    .thumb-box {
        width: 160px;
        height: 90px;
        background: #000;
        border-radius: 8px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2rem;
    }
    .x-bg { background: linear-gradient(45deg, #000000, #333333); }
    .ig-bg { background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%); }
    .play-btn { color: white; opacity: 0.8; }
    
    .card-info h4 { margin: 0 0 10px 0; color: #fff; }
    .card-info p { margin: 0; color: #888; font-size: 0.9rem; }
    .copy-link { color: #8E2DE2; text-decoration: none; font-weight: bold; margin-top: 10px; display: inline-block; }
    </style>
""", unsafe_allow_html=True)

# === 3. 백엔드 다운로드 로직 ===
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
            return ydl.prepare_filename(info), info.get('title', 'video')
    except Exception as e:
        return None, str(e)

# === 4. 실시간 API 연동 뼈대 (및 동적 시뮬레이션) ===
def fetch_real_time_trends():
    trends = []
    x_urls = [
        "https://x.com/elonmusk/status/1769498263723327668",
        "https://x.com/SpaceX/status/1768270609355473138",
        "https://x.com/NASA/status/1768310000000000000"
    ]
    ig_urls = [
        "https://www.instagram.com/instagram/",
        "https://www.instagram.com/natgeo/",
        "https://www.instagram.com/nike/"
    ]
    
    keywords = ["핫플", "강아지", "고양이", "다이어트 레시피", "직캠", "속보", "유머", "챌린지", "운동 루틴", "브이로그"]
    
    for i in range(1, 51):
        platform = random.choice(["X (Twitter)", "Instagram"])
        url = random.choice(x_urls) if platform == "X (Twitter)" else random.choice(ig_urls)
        
        trends.append({
            "rank": i,
            "platform": platform,
            "title": f"실시간 화제의 {random.choice(keywords)} 영상",
            "count": f"{random.randint(100, 9999) / 10.0:.1f}k",
            "url": url
        })
    return trends

# === 5. UI 구성 ===
left_ad, main_content, right_ad = st.columns([1.5, 7, 1.5])

with left_ad:
    st.markdown('<div class="side-banner">📢<br><br><b>광고문의</b><br>배너 등록<br>문의하기</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-banner">🎯<br><br>스폰서 배너<br>영역</div>', unsafe_allow_html=True)

with right_ad:
    st.markdown('<div class="side-banner">📺<br><br>구글 애드센스<br>광고 자리</div>', unsafe_allow_html=True)
    st.markdown('<div class="side-banner">🤝<br><br>제휴/입점 문의</div>', unsafe_allow_html=True)

with main_content:
    st.markdown('<div class="premium-banner">🚀 고화질 SNS 영상 다운로더 & 실시간 트렌드 분석 허브</div>', unsafe_allow_html=True)
    
    tab_dl, tab_rank = st.tabs(["📥 초고속 다운로드", "🔥 실시간 인기 영상 리스트"])
    
    # --- 다운로드 탭 ---
    with tab_dl:
        st.write("")
        url_input = st.text_input("👇 다운로드할 링크(URL)를 아래에 붙여넣으세요.", placeholder="예: https://x.com/username/status/...")
        
        if st.button("지금 추출하기", type="primary", use_container_width=True):
            if url_input:
                with st.spinner('서버에서 고화질 영상을 가져오고 있습니다...'):
                    file_path, title_or_error = download_video(url_input)
                    if file_path and os.path.exists(file_path):
                        st.success("🎉 성공적으로 추출했습니다!")
                        with open(file_path, "rb") as f:
                            st.download_button("💾 내 기기에 저장하기", data=f, file_name=os.path.basename(file_path), mime="video/mp4", use_container_width=True)
                    else:
                        st.error(f"❌ 다운로드에 실패했습니다. 비공개 영상이거나 링크가 잘못되었습니다.\n({title_or_error})")
            else:
                st.warning("먼저 링크를 입력해주세요.")

    # --- 랭킹 탭 ---
    with tab_rank:
        st.write("")
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_platform = st.radio("보기 옵션 선택:", ["🔥 전체보기", "🐦 X (Twitter)", "📸 Instagram"], horizontal=True)
        with col2:
            if st.button("🔄 실시간 데이터 갱신"):
                st.rerun()

        st.markdown("---")
        
        all_trends = fetch_real_time_trends()
        
        # 필터링 부분 (에러 안 나도록 완벽하게 띄어쓰기 정렬됨)
        if selected_platform == "🐦 X (Twitter)":
            filtered_trends = [t for t in all_trends if t["platform"] == "X (Twitter)"]
        elif selected_platform == "📸 Instagram":
            filtered_trends = [t for t in all_trends if t["platform"] == "Instagram"]
        else:
            filtered_trends = all_trends

        # 리스트 나열 박스
        with st.container(height=800):
            for t in filtered_trends:
                bg_class = "x-bg" if t['platform'] == "X (Twitter)" else "ig-bg"
                icon = "🐦" if t['platform'] == "X (Twitter)" else "📸"
                
                st.markdown(f"""
                <div class="video-card">
                    <div class="thumb-box {bg_class}">
                        <div class="play-btn">▶</div>
                    </div>
                    <div class="card-info">
                        <h4>🏅 {t['rank']}위 | {t['title']}</h4>
                        <p>{icon} 플랫폼: {t['platform']} &nbsp;|&nbsp; 📈 실시간 조회수: {t['count']}</p>
                        <a href="{t['url']}" target="_blank" class="copy-link">🔗 원본 영상 보러가기</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# 하단 푸터
st.markdown("<br><hr style='border-color: #2d3139;'>", unsafe_allow_html=True)
st.caption("<div style='text-align:center; color:#666;'>© 2026 SNS Media Hub. All rights reserved. | 이용약관 | DMCA</div>", unsafe_allow_html=True)