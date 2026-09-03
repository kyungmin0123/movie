import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =======================================
# 기본 설정
# =======================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("영화 데이터를 다양한 그래프로 살펴봅니다.")


# =======================================
# 데이터 불러오기
# =======================================
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

df = pd.read_csv(DATA_URL)

# 숫자형 변환
numeric_columns = [
    "first_scrn",
    "first_show",
    "first_week_audi",
    "total_audi",
    "days_in_top10"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 개봉일 변환
df["openDt"] = pd.to_datetime(
    df["openDt"].astype(str),
    format="%Y%m%d",
    errors="coerce"
)


# =======================================
# 장르 정리
# 여러 장르 중 첫 번째 장르만 사용
# =======================================
df["genre_first"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

df.loc[
    df["genre_first"].isin(["", "nan", "None"]),
    "genre_first"
] = "미상"


# =======================================
# 1. 장르별 영화 수 - 도넛 차트
# =======================================
st.header("1️⃣ 장르별 영화 수")

genre_count = (
    df["genre_first"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["genre", "count"]

fig1 = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.45,
    title="장르별 영화 수"
)

fig1.update_traces(
    textinfo="percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 어떤 장르의 영화가 가장 많은지 알 수 있다.",
    key="graph1_text"
)

st.divider()


# =======================================
# 2. 장르별 영화 관객 수 - 트리맵
# =======================================
st.header("2️⃣ 장르별 영화 관객 수")

treemap_df = df.dropna(
    subset=["genre_first", "movieNm", "total_audi"]
).copy()

fig2 = px.treemap(
    treemap_df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="영화별 총 관객 수"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 어떤 장르의 영화가 많은 관객을 모았는지 알 수 있다.",
    key="graph2_text"
)

st.divider()


# =======================================
# 3. 총 관객 수 분포 - 히스토그램
# =======================================
st.header("3️⃣ 총 관객 수 분포")

hist_df = df.dropna(
    subset=["total_audi"]
).copy()

hist_values = hist_df["total_audi"].astype(float)

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 수: %{x:,}명<br>"
        "영화 수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    xaxis_tickformat=","
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

if len(hist_values) > 0:

    counts, edges = np.histogram(
        hist_values,
        bins=30
    )

    max_bin = int(np.argmax(counts))

    range_start = int(edges[max_bin])
    range_end = int(edges[max_bin + 1])

    max_movie = hist_df.loc[
        hist_df["total_audi"].idxmax(),
        "movieNm"
    ]

    max_audience = int(
        hist_df["total_audi"].max()
    )

    st.info(
        f"📊 **가장 많은 영화가 몰려 있는 구간:** "
        f"{range_start:,}명 ~ {range_end:,}명"
    )

    st.success(
        f"🏆 **가장 많은 관객을 모은 영화:** "
        f"{max_movie} ({max_audience:,}명)"
    )

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 대부분의 영화가 어느 정도의 관객 수를 기록했는지 알 수 있다.",
    key="graph3_text"
)

st.divider()


# =======================================
# 4. 첫날 스크린 수와 총 관객 수 관계
# =======================================
st.header("4️⃣ 첫날 스크린 수와 총 관객 수의 관계")

scatter_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "movieNm",
        "genre_first"
    ]
).copy()

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre_first",
    hover_name="movieNm",
    title="첫날 스크린 수와 총 관객 수",
    labels={
        "first_scrn": "첫날 스크린 수",
        "total_audi": "총 관객 수",
        "genre_first": "장르"
    }
)

fig4.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "첫날 스크린 수: %{x:,}개<br>"
        "총 관객 수: %{y:,}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    xaxis_tickformat=",",
    yaxis_tickformat=","
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 첫날 스크린 수와 총 관객 수 사이의 관계를 알 수 있다.",
    key="graph4_text"
)

st.divider()


# =======================================
# 5. 장르별 총 관객 수 - 박스플롯
# 영화가 10편 이상인 장르만
# =======================================
st.header("5️⃣ 장르별 총 관객 수 분포")

genre_movie_count = (
    df["genre_first"]
    .value_counts()
)

valid_genres = genre_movie_count[
    genre_movie_count >= 10
].index

box_df = df[
    df["genre_first"].isin(valid_genres)
].dropna(
    subset=[
        "genre_first",
        "total_audi",
        "movieNm"
    ]
).copy()

fig5 = px.box(
    box_df,
    x="genre_first",
    y="total_audi",
    points="outliers",
    hover_name="movieNm",
    title="영화가 10편 이상인 장르의 총 관객 수 분포",
    labels={
        "genre_first": "장르",
        "total_audi": "총 관객 수"
    }
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "총 관객 수: %{y:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    yaxis_tickformat=","
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 장르별 총 관객 수의 분포와 이상치를 비교할 수 있다.",
    key="graph5_text"
)

st.divider()


# =======================================
# 6. 버블 산점도
# 버블 크기 = 첫 주 관객
# =======================================
st.header("6️⃣ 첫날 스크린 수와 총 관객 수 - 버블 그래프")

bubble_df = df.dropna(
    subset=[
        "first_scrn",
        "total_audi",
        "first_week_audi",
        "movieNm",
        "genre_first"
    ]
).copy()

bubble_df["bubble_size"] = bubble_df[
    "first_week_audi"
].clip(lower=1)

fig6 = px.scatter(
    bubble_df,
    x="first_scrn",
    y="total_audi",
    size="bubble_size",
    color="genre_first",
    hover_name="movieNm",
    title="첫날 스크린 수와 총 관객 수 (버블 크기 = 첫 주 관객)",
    labels={
        "first_scrn": "첫날 스크린 수",
        "total_audi": "총 관객 수",
        "genre_first": "장르",
        "bubble_size": "첫 주 관객"
    },
    size_max=50
)

fig6.update_traces(
    marker=dict(
        opacity=0.7
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "첫날 스크린 수: %{x:,}개<br>"
        "총 관객 수: %{y:,}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    xaxis_tickformat=",",
    yaxis_tickformat=","
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 첫 주 관객 수가 큰 영화가 어떤 위치에 분포하는지 알 수 있다.",
    key="graph6_text"
)

st.divider()


# =======================================
# 7. 제작 국가 → 장르 선버스트
# 크기 = 영화 편수
# =======================================
st.header("7️⃣ 제작 국가와 장르의 관계")

sunburst_df = df.dropna(
    subset=["nation", "genre_first"]
).copy()

# 제작 국가가 여러 개라면 첫 번째 국가만 사용
sunburst_df["nation_first"] = (
    sunburst_df["nation"]
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

sunburst_df.loc[
    sunburst_df["nation_first"].isin(
        ["", "nan", "None"]
    ),
    "nation_first"
] = "미상"

sunburst_count = (
    sunburst_df
    .groupby(
        ["nation_first", "genre_first"]
    )
    .size()
    .reset_index(
        name="movie_count"
    )
)

fig7 = px.sunburst(
    sunburst_count,
    path=[
        "nation_first",
        "genre_first"
    ],
    values="movie_count",
    title="제작 국가 → 장르별 영화 편수",
    labels={
        "nation_first": "제작 국가",
        "genre_first": "장르",
        "movie_count": "영화 편수"
    }
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

# ★ 7번 그래프 크게 만들기
fig7.update_layout(
    height=850,
    margin=dict(
        l=20,
        r=20,
        t=80,
        b=20
    )
)

st.plotly_chart(
    fig7,
    use_container_width=True
)

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 제작 국가별로 어떤 장르의 영화가 많이 만들어졌는지 알 수 있다.",
    key="graph7_text"
)

st.divider()


# =======================================
# 8. 장르별 TOP 10 유지 기간
# 영화가 10편 이상인 장르만
# =======================================
st.header("8️⃣ 장르별 TOP 10 유지 기간")

days_df = df.dropna(
    subset=[
        "genre_first",
        "days_in_top10"
    ]
).copy()

genre_count_for_days = (
    days_df["genre_first"]
    .value_counts()
)

valid_genres_days = genre_count_for_days[
    genre_count_for_days >= 10
].index

days_df = days_df[
    days_df["genre_first"].isin(
        valid_genres_days
    )
]

genre_days = (
    days_df
    .groupby("genre_first")[
        "days_in_top10"
    ]
    .mean()
    .reset_index()
)

genre_days.columns = [
    "genre",
    "average_days"
]

genre_days = genre_days.sort_values(
    "average_days",
    ascending=False
)

fig8 = px.bar(
    genre_days,
    x="genre",
    y="average_days",
    title="장르별 평균 TOP 10 유지 일수",
    labels={
        "genre": "장르",
        "average_days": "평균 TOP 10 유지 일수"
    },
    text="average_days"
)

fig8.update_traces(
    texttemplate="%{text:.1f}일",
    textposition="outside",
    hovertemplate=(
        "<b>%{x}</b><br>"
        "평균 TOP 10 유지: %{y:.1f}일"
        "<extra></extra>"
    )
)

fig8.update_layout(
    yaxis_title="평균 TOP 10 유지 일수",
    xaxis_title="장르"
)

st.plotly_chart(
    fig8,
    use_container_width=True
)

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "한 문장으로 작성해 보세요.",
    placeholder="예: 어떤 장르의 영화가 TOP 10에 오래 머무르는 경향이 있는지 알 수 있다.",
    key="graph8_text"
)

st.divider()

st.caption("🎬 영화 데이터 그래프 도감 2")
