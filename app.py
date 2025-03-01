import streamlit as st
import os

FILE_PATH = "companies.txt"  # 절대 경로 대신 상대 경로 사용

def load_companies(file_path):
    companies = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("|")
                # 각 줄은 10개 항목: 업체명, 업체구분, 홈페이지, 블로그, 인스타그램, 작가소개, 상품 구성, 가격, 대표이미지, 지역
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

st.title("Marry U")

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

# 관리자 모드일 때만 입력 폼 표시
selected_data = None
if admin_mode and companies:
    company_names = [comp["업체명"] for comp in companies]
    selected_company = st.sidebar.selectbox("수정할 업체 선택", options=[""] + company_names)
    if selected_company:
        selected_data = next((comp for comp in companies if comp["업체명"] == selected_company), None)

if admin_mode:
    st.header("업체 정보 입력 (관리자 모드)")
    name = st.text_input("업체명", value=selected_data["업체명"] if selected_data else "")
    category = st.text_input("업체구분", value=selected_data["업체구분"] if selected_data else "")
    homepage = st.text_input("홈페이지", value=selected_data["홈페이지"] if selected_data else "")
    blog = st.text_input("블로그", value=selected_data["블로그"] if selected_data else "")
    instagram = st.text_input("인스타그램", value=selected_data["인스타그램"] if selected_data else "")
    artist = st.text_input("작가소개", value=selected_data["작가소개"] if selected_data else "")
    product = st.text_input("상품 구성", value=selected_data["상품 구성"] if selected_data else "")
    rep_img = st.text_input("대표이미지", value=selected_data["대표이미지"] if selected_data else "")
    
    # '지역' 항목: 기본 옵션 목록을 "충청", "경기(남부)"로 설정 (체크박스 형태: multiselect)
    region_options = ["충청", "경기(남부)"]
    default_regions = []
    if selected_data and selected_data["지역"]:
        default_regions = [r.strip() for r in selected_data["지역"].split(",")]
    selected_regions = st.multiselect("지역", options=region_options, default=default_regions)
    region = ",".join(selected_regions)

    col1, col2, col3, col4 = st.columns(4)
    if col1.button("업체 추가"):
        if not name:
            st.error("업체명을 입력하세요.")
        else:
            new_data = {
                "업체명": name,
                "업체구분": category,
                "홈페이지": homepage,
                "블로그": blog,
                "인스타그램": instagram,
                "작가소개": artist,
                "상품 구성": product,
                "대표이미지": rep_img,
                "지역": region
            }
            companies.append(new_data)
            save_all_companies(companies, FILE_PATH)
            st.success("업체 정보가 추가되었습니다.")
            st.experimental_rerun()
    
    if col2.button("수정"):
        if not selected_company:
            st.error("수정할 업체를 선택하세요.")
        elif not name:
            st.error("업체명을 입력하세요.")
        else:
            for comp in companies:
                if comp["업체명"] == selected_company:
                    comp["업체명"] = name
                    comp["업체구분"] = category
                    comp["홈페이지"] = homepage
                    comp["블로그"] = blog
                    comp["인스타그램"] = instagram
                    comp["작가소개"] = artist
                    comp["상품 구성"] = product
                    comp["대표이미지"] = rep_img
                    comp["지역"] = region
                    break
            save_all_companies(companies, FILE_PATH)
            st.success("업체 정보가 수정되었습니다.")
            st.experimental_rerun()
    
    if col3.button("삭제"):
        if not selected_company:
            st.error("삭제할 업체를 선택하세요.")
        else:
            companies = [comp for comp in companies if comp["업체명"] != selected_company]
            save_all_companies(companies, FILE_PATH)
            st.success("업체 정보가 삭제되었습니다.")
            st.experimental_rerun()
    
    if col4.button("저장"):
        save_all_companies(companies, FILE_PATH)
        st.success("파일에 저장되었습니다.")

# 일반 모드: HTML 테이블로 업체 정보 표시 (일반 모드에서는 '지역' 항목 미표시)
if companies:
    # 아이콘 URL 설정 (테이블용)
    homepage_icon = "https://cdn-icons-png.freepik.com/256/620/620801.png?ga=GA1.1.1596980588.1740342915"
    blog_icon = "https://unclesnap.com/imgs/blog.png"
    instagram_icon = "https://unclesnap.com/imgs/insta.png"
    artist_icon = "https://cdn-icons-png.freepik.com/256/13953/13953830.png?ga=GA1.1.1596980588.1740342915&semt=ais_hybrid"
    product_icon = "https://cdn-icons-png.freepik.com/256/6320/6320013.png?ga=GA1.1.1596980588.1740342915&semt=ais_hybrid"
    
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
        homepage_html_cell = (f'<a href="{comp["홈페이지"]}" target="_blank">'
                              f'<img src="{homepage_icon}" style="width:20px;height:20px;" alt="홈">'
                              f'</a>') if comp["홈페이지"].strip() else ""
        blog_html_cell = (f'<a href="{comp["블로그"]}" target="_blank">'
                          f'<img src="{blog_icon}" style="width:20px;height:20px;" alt="블로그">'
                          f'</a>') if comp["블로그"].strip() else ""
        instagram_html_cell = (f'<a href="{comp["인스타그램"]}" target="_blank">'
                               f'<img src="{instagram_icon}" style="width:20px;height:20px;" alt="인스타">'
                               f'</a>') if comp["인스타그램"].strip() else ""
        artist_html_cell = (f'<a href="{comp["작가소개"]}" target="_blank">'
                            f'<img src="{artist_icon}" style="width:20px;height:20px;" alt="작가">'
                            f'</a>') if comp["작가소개"].strip() else ""
        product_html_cell = (f'<a href="{comp["상품 구성"]}" target="_blank">'
                             f'<img src="{product_icon}" style="width:20px;height:20px;" alt="상품">'
                             f'</a>') if comp["상품 구성"].strip() else ""
        
        table_html += f"""
        <tr>
            <td>{comp['업체명']}</td>
            <td>{homepage_html_cell}</td>
            <td>{blog_html_cell}</td>
            <td>{instagram_html_cell}</td>
            <td>{artist_html_cell}</td>
            <td>{product_html_cell}</td>
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
