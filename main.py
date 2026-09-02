import streamlit as st
import pandas as pd
import plotly.express as px


# ==================================================
# 기본 설정
# ==================================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("영화의 장르, 관객 수, 개봉 정보 등의 분포와 관계를 살펴봅니다.")


# ==================================================
# 데이터 불러오기
# ==================================================
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

df = pd.read_csv(DATA_URL)


# ==================================================
# 데이터 전처리
# ==================================================

# 개봉일을 실제 날짜 형식으로 변환
df["openDt"] = pd.to_datetime(
    df["openDt"].astype(str),
    format="%Y%m%d",
    errors="coerce"
)

# 숫자형 데이터 변환
number_columns = [
    "first_scrn",
    "first_show",
    "first_week_audi",
    "total_audi",
    "days_in_top10"
]

for col in number_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )


# 장르가 여러 개 적혀 있는 경우 첫 번째 장르만 사용
df["genre_first"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

# 빈 장르는 미상으로 처리
df.loc[
    df["genre_first"].isin(["", "nan"]),
    "genre_first"
] = "미상"


# ==================================================
# 그래프 1
# ==================================================
st.header("📊 그래프 1. 장르별 영화 편수")

# 장르별 영화 편수 계산
genre_count = (
    df["genre_first"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화편수"]

# 도넛 그래프
fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화편수",
    hole=0.45,
    title="장르별 영화 편수",
)

# 마우스를 올렸을 때 편수와 비율 표시
fig1.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    legend_title="장르"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.text_input(
    "그래프를 보고 알 수 있는 내용을 한 문장으로 적어 보세요.",
    placeholder="예: 이 기간에 개봉한 영화 중 특정 장르의 영화가 가장 큰 비중을 차지한다.",
    key="graph1_comment"
)


# ==================================================
# 그래프 2
# ==================================================
st.divider()

st.header("📊 그래프 2")
st.info("앞으로 새로운 그래프가 추가될 영역입니다.")


# ==================================================
# 그래프 3
# ==================================================
st.divider()

st.header("📊 그래프 3")
st.info("앞으로 새로운 그래프가 추가될 영역입니다.")


# ==================================================
# 그래프 4
# ==================================================
st.divider()

st.header("📊 그래프 4")
st.info("앞으로 새로운 그래프가 추가될 영역입니다.")
