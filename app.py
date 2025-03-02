import streamlit as st
import os
from streamlit_sortables import sort_items

FILE_PATH = "/Users/atin5/Desktop/app/companies.txt"  # 절대 경로 대신 상대 경로 사용

# 업체 데이터 로드 함수

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

# 업체 데이터 저장 함수

def save_all_companies(companies, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        for comp in companies:
            line = "|".join([
                comp.get("업체명", ""),
                comp.get("업체구분", ""),
                comp.get("홈페이지", ""),
                comp.get("블로그", ""),
                comp.get("인스타그램", ""),
                comp.get("작가소개", ""),
                comp.get("상품 구성", ""),
                "",  # 가격 자리 (사용하지 않음)
                comp.get("대표이미지", ""),
                comp.get("지역", "")
            ])
            f.write(line + "\n")

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

# 일반 모드 및 관리자 모드에서 표 표시
if companies:
    st.write("업체 목록")
    homepage_icon = "https://cdn-icons-png.freepik.com/256/620/620801.png"
    blog_icon = "https://unclesnap.com/imgs/blog.png"
    instagram_icon = "https://unclesnap.com/imgs/insta.png"
    artist_icon = "https://cdn-icons-png.freepik.com/256/13953/13953830.png"
    product_icon = "https://cdn-icons-png.freepik.com/256/6320/6320013.png"

    table_html = """
    <table style='width:80%; border-collapse: collapse; font-size: 12px; margin:auto;'>
        <tr>
            <th style='border: 1px solid #ddd; padding: 6px; text-align: center;'>업체명</th>
            <th style='border: 1px solid #ddd; padding: 6px; text-align: center;'>홈</th>
            <th style='border: 1px solid #ddd; padding: 6px; text-align: center;'>인스타</th>
            <th style='border: 1px solid #ddd; padding: 6px; text-align: center;'>블로그</th>
            <th style='border: 1px solid #ddd; padding: 6px; text-align: center;'>상품</th>
            <th style='border: 1px solid #ddd; padding: 6px; text-align: center;'>작가</th>
        </tr>
    """

    for comp in companies:
        table_html += f"<tr><td style='border: 1px solid #ddd; padding: 6px; text-align: center;'>{comp['업체명']}</td>"
        for key, icon in zip(
            ['홈페이지', '인스타그램', '블로그', '상품 구성', '작가소개'],
            [homepage_icon, instagram_icon, blog_icon, product_icon, artist_icon]
        ):
            if comp[key]:
                table_html += f"<td style='border: 1px solid #ddd; padding: 6px; text-align: center;'>"
                table_html += f"<a href='{comp[key]}' target='_blank'><img src='{icon}' style='width:20px; height:20px;'></a>"
                table_html += "</td>"
            else:
                table_html += "<td style='border: 1px solid #ddd; padding: 6px; text-align: center;'></td>"
        table_html += "</tr>"

    table_html += "</table>"
    st.markdown(table_html, unsafe_allow_html=True)

# 관리자 모드에서 사이드바를 통한 업체 정보 입력, 수정, 삭제 및 저장 기능
if admin_mode:
    st.sidebar.header("업체 정보 입력 및 수정")
    selected_data = None
    if companies:
        company_names = [comp["업체명"] for comp in companies]
        selected_company = st.sidebar.selectbox("수정할 업체 선택", options=[""] + company_names)
        if selected_company:
            selected_data = next((comp for comp in companies if comp["업체명"] == selected_company), None)

    name = st.sidebar.text_input("업체명", value=selected_data["업체명"] if selected_data else "")
    category = st.sidebar.text_input("업체구분", value=selected_data["업체구분"] if selected_data else "")
    homepage = st.sidebar.text_input("홈페이지", value=selected_data["홈페이지"] if selected_data else "")
    blog = st.sidebar.text_input("블로그", value=selected_data["블로그"] if selected_data else "")
    instagram = st.sidebar.text_input("인스타그램", value=selected_data["인스타그램"] if selected_data else "")
    artist = st.sidebar.text_input("작가소개", value=selected_data["작가소개"] if selected_data else "")
    product = st.sidebar.text_input("상품 구성", value=selected_data["상품 구성"] if selected_data else "")
    region = st.sidebar.text_input("지역", value=selected_data["지역"] if selected_data else "")

    st.sidebar.markdown("---")
    if st.sidebar.button("업체 추가") and name:
        companies.append({
            "업체명": name,
            "업체구분": category,
            "홈페이지": homepage,
            "블로그": blog,
            "인스타그램": instagram,
            "작가소개": artist,
            "상품 구성": product,
            "대표이미지": "",
            "지역": region
        })
        save_all_companies(companies, FILE_PATH)
        st.experimental_rerun()

    if st.sidebar.button("수정") and selected_data:
        selected_data.update({
            "업체명": name,
            "업체구분": category,
            "홈페이지": homepage,
            "블로그": blog,
            "인스타그램": instagram,
            "작가소개": artist,
            "상품 구성": product,
            "지역": region
        })
        save_all_companies(companies, FILE_PATH)
        st.experimental_rerun()

    if st.sidebar.button("삭제") and selected_data:
        companies = [comp for comp in companies if comp["업체명"] != selected_company]
        save_all_companies(companies, FILE_PATH)
        st.experimental_rerun()

    if st.sidebar.button("저장"):
        save_all_companies(companies, FILE_PATH)
        st.success("파일에 저장되었습니다.")
