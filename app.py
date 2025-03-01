import streamlit as st
import os

FILE_PATH = "companies.txt"  # 절대 경로 대신 상대 경로 사용

def load_companies(file_path):
    companies = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 10:
                    companies.append({
                        "업체명": parts[0],
                        "업체구분": parts[1],
                        "홈페이지": parts[2],
                        "블로그": parts[3],
                        "인스타그램": parts[4],
                        "작가소개": parts[5],
                        "상품 구성": parts[6],
                        "대표이미지": parts[8],
                        "지역": parts[9]
                    })
    else:
        st.warning("⚠️ 경고: 파일을 찾을 수 없습니다.")
    return companies

# 관리자 모드 활성화 (패스워드: admin123)
admin_mode = st.sidebar.checkbox("관리자 모드 활성화")
if admin_mode:
    password = st.sidebar.text_input("관리자 패스워드", type="password")
    if password != "admin123":
        st.sidebar.error("패스워드가 올바르지 않습니다.")
        admin_mode = False
    else:
        st.sidebar.success("관리자 모드 활성화됨")

# 업체 데이터 로드
companies = load_companies(FILE_PATH)

# 일반 모드: 업체 목록 표시 및 이미지 미리보기 기능
if companies:
    st.title("우리동네 스냅업체 정보")

    # 이미지 미리보기 섹션
    st.sidebar.header("대표 이미지 미리보기")
    selected_company = st.sidebar.selectbox("업체명 선택", [""] + [comp["업체명"] for comp in companies])

    if selected_company:
        selected_data = next((comp for comp in companies if comp["업체명"] == selected_company), None)
        if selected_data:
            image_url = selected_data["대표이미지"]
            if image_url:
                st.sidebar.image(image_url, caption=selected_data["업체명"], use_column_width=True)
            else:
                st.sidebar.info("이미지 URL이 없습니다.")
    
    # 업체 목록 테이블 표시
    st.write("### 업체 목록")
    table_html = """
    <html>
    <head>
    <style>
        table { width: 100%; border-collapse: collapse; margin: 20px 0; font-family: Arial, sans-serif; font-size: 12px; }
        th, td { border: 1px solid #ccc; padding: 6px 10px; text-align: center; }
        th { background-color: #f8f8f8; font-weight: bold; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        a { text-decoration: none; color: #1a73e8; }
        img { vertical-align: middle; }
    </style>
    </head>
    <body>
    <table>
        <tr>
            <th>이름</th>
            <th>홈</th>
            <th>블로그</th>
            <th>인스타</th>
            <th>작가</th>
            <th>상품</th>
        </tr>
    """
    for comp in companies:
        table_html += f"""
        <tr>
            <td>{comp['업체명']}</td>
            <td><a href="{comp['홈페이지']}" target="_blank">홈페이지</a></td>
            <td><a href="{comp['블로그']}" target="_blank">블로그</a></td>
            <td><a href="{comp['인스타그램']}" target="_blank">인스타</a></td>
            <td><a href="{comp['작가소개']}" target="_blank">작가</a></td>
            <td><a href="{comp['상품 구성']}" target="_blank">상품</a></td>
        </tr>
        """
    table_html += """
    </table>
    </body>
    </html>
    """
    st.components.v1.html(table_html, height=600, scrolling=True)

else:
    st.info("표시할 업체 데이터가 없습니다.")
