import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

df = pd.read_csv(URL)

# 숫자형 데이터 변환
numeric_cols = [
    "first_scrn",
    "first_show",
    "first_week_audi",
    "total_audi",
    "days_in_top10"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 개봉일 변환
df["openDt"] = pd.to_datetime(
    df["openDt"].astype(str),
    format="%Y%m%d",
    errors="coerce"
)

# 장르가 여러 개라면 첫 번째 장르만 사용
df["genre_first"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

df["genre_first"] = df["genre_first"].replace("", "미상")


# =========================================================
# 1. 장르별 영화 편수 도넛 그래프
# =========================================================

st.header("1. 장르별 영화 편수")

genre_count = (
    df["genre_first"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["장르", "영화편수"]

fig1 = px.pie(
    genre_count,
    names="장르",
    values="영화편수",
    hole=0.45,
    title="장르별 영화 편수"
)

fig1.update_traces(
    hovertemplate="<b>%{label}</b><br>"
                  "영화 편수: %{value}편<br>"
                  "비율: %{percent}<extra></extra>"
)

fig1.update_layout(
    height=550
)

st.plotly_chart(fig1, use_container_width=True)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="graph1_answer",
    placeholder="장르별 영화 편수의 특징을 한 문장으로 적어 보세요."
)

st.divider()


# =========================================================
# 2. 장르 → 영화 트리맵
# =========================================================

st.header("2. 장르별 영화 총 관객 트리맵")

treemap_df = df[
    ["genre_first", "movieNm", "total_audi"]
].dropna(subset=["movieNm", "total_audi"])

fig2 = px.treemap(
    treemap_df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객"
)

fig2.update_traces(
    hovertemplate="<b>%{label}</b><br>"
                  "총 관객: %{value:,}명"
                  "<extra></extra>"
)

fig2.update_layout(
    height=650
)

st.plotly_chart(fig2, use_container_width=True)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="graph2_answer",
    placeholder="어떤 장르와 영화가 많은 관객을 차지하는지 한 문장으로 적어 보세요."
)

st.divider()


# =========================================================
# 3. 총 관객 히스토그램
# =========================================================

st.header("3. 영화별 총 관객 분포")

hist_df = df.dropna(subset=["total_audi"]).copy()

fig3 = px.histogram(
    hist_df,
    x="total_audi",
    nbins=30,
    title="영화별 총 관객 분포"
)

fig3.update_traces(
    hovertemplate="총 관객: %{x:,}명<br>"
                  "영화 수: %{y}편"
                  "<extra></extra>"
)

fig3.update_xaxes(
    title="총 관객 수"
)

fig3.update_yaxes(
    title="영화 편수"
)

fig3.update_layout(
    height=550
)

st.plotly_chart(fig3, use_container_width=True)

# 대부분의 영화가 몰려 있는 구간 계산
hist_values = hist_df["total_audi"]

min_audi = hist_values.min()
max_audi = hist_values.max()

bins = 10

counts, edges = pd.np.histogram(
    hist_values,
    bins=bins
)

max_bin_index = counts.argmax()

range_start = int(edges[max_bin_index])
range_end = int(edges[max_bin_index + 1])

# 가장 관객이 많은 영화
max_movie_row = hist_df.loc[
    hist_df["total_audi"].idxmax()
]

max_movie_name = max_movie_row["movieNm"]
max_movie_audi = int(max_movie_row["total_audi"])

st.markdown(
    f"**대부분의 영화가 몰려 있는 구간:** "
    f"{range_start:,}명 ~ {range_end:,}명"
)

st.markdown(
    f"**가장 관객이 많은 영화:** "
    f"{max_movie_name} ({max_movie_audi:,}명)"
)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="graph3_answer",
    placeholder="영화의 총 관객 분포와 가장 관객이 많은 영화를 한 문장으로 적어 보세요."
)

st.divider()


# =========================================================
# 4. 개봉일 스크린수와 총 관객 산점도
# =========================================================

st.header("4. 개봉일 스크린수와 총 관객의 관계")

scatter_df = df[
    ["movieNm", "genre_first", "first_scrn", "total_audi"]
].dropna(
    subset=["movieNm", "genre_first", "first_scrn", "total_audi"]
)

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre_first",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객의 관계"
)

fig4.update_traces(
    marker=dict(size=9),
    hovertemplate="<b>%{hovertext}</b><br>"
                  "개봉일 스크린수: %{x:,}개<br>"
                  "총 관객: %{y:,}명"
                  "<extra></extra>"
)

fig4.update_xaxes(
    title="개봉일 스크린수"
)

fig4.update_yaxes(
    title="총 관객"
)

fig4.update_layout(
    height=650,
    legend_title="장르"
)

st.plotly_chart(fig4, use_container_width=True)

st.text_input(
    "이 그래프로 알 수 있는 것",
    key="graph4_answer",
    placeholder="개봉일 스크린수와 총 관객의 관계를 한 문장으로 적어 보세요."
)
