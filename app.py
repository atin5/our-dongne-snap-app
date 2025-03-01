import streamlit as st
import os

FILE_PATH = os.path.join(os.path.dirname(__file__), "companies.txt")

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
    return sorted(companies, key=lambda x: x["업체명"])

def save_all_companies(companies, file_path):
    try:
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
                    "",  
                    comp.get("대표이미지", ""),
                    comp.get("지역", "")
                ])
                f.write(line + "\n")
        st.success("파일에 저장되었습니다.")
    except Exception as e:
        st.error(f"파일 저장에 실패했습니다: {e}")

admin_mode = st.sidebar.checkbox("관리자 모드 활성화")
if admin_mode:
    password = st.sidebar.text_input("관리자 패스워드", type="password")
    if password != "admin123":
        st.sidebar.error("패스워드가 올바르지 않습니다.")
        admin_mode = False
    else:
        st.sidebar.success("관리자 모드 활성화됨")

companies = load_companies(FILE_PATH)
selected_data = None
if admin_mode and companies:
    company_names = [comp["업체명"] for comp in companies]
    company_names.sort()
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
            st.experimental_rerun()

    if col2.button("수정"):
        if not selected_company:
            st.error("수정할 업체를 선택하세요.")
        elif not name:
            st.error("업체명을 입력하세요.")
        else:
            for comp in companies:
                if comp["업체명"] == selected_company:
                    comp.update(new_data)
                    break
            save_all_companies(companies, FILE_PATH)
            st.experimental_rerun()

    if col3.button("삭제"):
        if not selected_company:
            st.error("삭제할 업체를 선택하세요.")
        else:
            companies = [comp for comp in companies if comp["업체명"] != selected_company]
            save_all_companies(companies, FILE_PATH)
            st.experimental_rerun()

if companies:
    companies = sorted(companies, key=lambda x: x["업체명"], reverse=False)
    for comp in companies:
        st.markdown(f"### {comp['업체명']}")
        st.write(f"홈페이지: {comp['홈페이지']}")
        st.write(f"블로그: {comp['블로그']}")
        st.write(f"인스타그램: {comp['인스타그램']}")
        st.write(f"작가소개: {comp['작가소개']}")
        st.write(f"상품 구성: {comp['상품 구성']}")
        st.write(f"대표이미지: {comp['대표이미지']}")
        st.write(f"지역: {comp['지역']}")
else:
    st.info("표시할 업체 데이터가 없습니다.")
