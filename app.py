#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# annotated text
# lottie


# In[ ]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import platform

# 한글 폰트 설정
# if platform.system() == 'Windows':
#     plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
# elif platform.system() == 'Darwin':  # MacOS
#     plt.rcParams['font.family'] = 'AppleGothic'
# else:
#     plt.rcParams['font.family'] = 'NanumGothic'  # Linux 환경 (예: Colab)

# plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@100..900&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit 전체 화면 확장
st.set_page_config(layout="wide")

# 데이터 설정
data = pd.DataFrame({
    'Name': ['성장성', '수익성', '안전성', '생산성', '활동성', '유동성'],
    'Bo': [80, 20, 80, 40, 60, 70],  # 대상 회사 값
    'Soo': [50, 50, 50, 50, 50, 50],  # 동일 업종 평균 값
})

# 옵션 및 색상 매핑
options = ["매우 나쁨", "나쁨", "보통", "좋음", "매우 좋음"]
colors = {
    "매우 나쁨": "#ff4d4d",  # 빨강
    "나쁨": "#ff9999",      # 연빨강
    "보통": "#ffd700",      # 노랑
    "좋음": "#90ee90",      # 연초록
    "매우 좋음": "#32cd32"  # 초록
}

# Custom CSS
st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .buttons {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 0;
    }
    button {
        width: 100%;
        height: 40px;
        border: 1px solid #ddd;
        background-color: #f0f0f0;
        cursor: not-allowed;  /* 클릭 비활성화 */
        pointer-events: none; /* 클릭 이벤트 비활성화 */
    }
    </style>
""", unsafe_allow_html=True)

# 경영진단 항목별 요약 타이틀 중앙 정렬
st.markdown('<div class="title">경영진단 항목별 요약</div>', unsafe_allow_html=True)

# 데이터 차이를 계산하여 Description 및 절대 기준으로 Level 생성
def generate_description_and_level(row):
    difference = row['Bo'] - row['Soo']
    
    # Description 생성
    if difference > 0:
        description = f"동일 업종 평균 대비 {abs(difference):.1f}% 높음"
    elif difference < 0:
        description = f"동일 업종 평균 대비 {abs(difference):.1f}% 낮음"
    else:
        description = "동일 업종 평균과 동일"
    
    # Level 생성 (절대 기준)
    if row['Bo'] >= 80:
        level = "매우 좋음"
    elif row['Bo'] >= 60:
        level = "좋음"
    elif row['Bo'] >= 40:
        level = "보통"
    elif row['Bo'] >= 20:
        level = "나쁨"
    else:
        level = "매우 나쁨"
    
    return description, level

data[['Description', 'Level']] = data.apply(
    lambda row: pd.Series(generate_description_and_level(row)), axis=1
)

# 레이더 차트 생성
categories = data['Name']
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]  # 닫힌 도형을 만들기 위해 첫 값을 추가

values_bo = data['Bo'].tolist() + [data['Bo'][0]]
values_soo = data['Soo'].tolist() + [data['Soo'][0]]

# 고정 크기로 설정 (화면 비율 고려)
fig_width = 8  # 너비
fig_height = 8 * 0.6  # 높이를 60%로 설정

fig, ax = plt.subplots(figsize=(fig_width, fig_height), subplot_kw=dict(polar=True))
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(1)  # 반시계 방향으로 설정

# 기본 원형 그리드 제거
ax.spines['polar'].set_visible(False)  # 원형 축선 제거
ax.yaxis.set_visible(False)  # 반지름 축 레이블 제거

# 축과 레이블 설정
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)

# 다각형 점선 및 100점 실선 추가
levels = [20, 40, 60, 80, 100]
for level in levels:
    ax.plot(angles, [level] * len(angles), '-', color='darkgrey', linewidth=1.2)

# 동일 업종 데이터
ax.plot(angles, values_soo, color='blue', linewidth=2, label='동일 업종 평균')
ax.fill(angles, values_soo, color='blue', alpha=0.25)

# 대상 회사 데이터
ax.plot(angles, values_bo, color='orange', linewidth=2, label='대상 회사')
ax.fill(angles, values_bo, color='orange', alpha=0.25)

# 범례 및 타이틀 설정
ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

# Streamlit 레이아웃
col1, col2, col3, col4 = st.columns([0.1, 0.4, 0.4, 0.1])  # 컬럼 비율 동일

# 데이터 설명 및 버튼 생성
with col2:
    for index, row in data.iterrows():
        # Description, Name, Buttons가 한 행에 위치하도록 설정
        
        st.markdown(f"""
            <div style="display: flex; flex-direction: row; align-items: center; margin-bottom: 5px;">
                <div style="width: 50%; font-weight: bold;">{row['Name']}</div>
                <div style="width: 50%; text-align: right;">{row['Description']}</div>
        """, unsafe_allow_html=True)
        buttons_html = ""
        for opt in options:
            color = colors[opt] if opt == row['Level'] else "#f0f0f0"
            buttons_html += f'<button style="background-color: {color}; margin-bottom: 5px;">{opt}</button>'
    

        # 아래 버튼 배치
        st.markdown(f"""
            <div class="buttons" style="margin-bottom: 10px;">
                {buttons_html}
            </div>
        """, unsafe_allow_html=True)  
        
# 오른쪽 레이더 차트 표시
with col3:
    st.pyplot(fig)


# In[ ]:





# In[ ]:


# import streamlit as st
# import plotly.graph_objects as go

# # 항목 및 고정 점수 정의
# categories = ['성장성', '수익성', '거래처 안정성', '재무 안정성', '현금흐름']
# scores = [80, 70, 85, 90, 75]  # 고정된 점수

# # 점수 범위와 레벨 정의
# levels = ['매우 나쁨', '나쁨', '보통', '좋음', '매우 좋음']
# score_to_level = {
#     '매우 나쁨': range(0, 21),
#     '나쁨': range(21, 41),
#     '보통': range(41, 61),
#     '좋음': range(61, 81),
#     '매우 좋음': range(81, 101)
# }

# # 점수를 평가 레벨로 변환
# def get_level(score):
#     for level, rng in score_to_level.items():
#         if score in rng:
#             return level
#     return "Unknown"

# # 평가 결과 요약 텍스트 생성
# def render_result_row(category, score):
#     level = get_level(score)
#     row = f"**{category}**  \n"
#     for l in levels:
#         if l == level:
#             row += f"<span style='background-color:lightblue;padding:5px;border-radius:5px;'>{l}</span> "
#         else:
#             row += f"{l} "
#     return row

# # 레이더 차트 데이터
# categories_closed = categories + [categories[0]]  # 폐곡선 생성
# scores_closed = scores + [scores[0]]

# # 레이더 차트 생성
# fig = go.Figure()

# fig.add_trace(go.Scatterpolar(
#     r=scores_closed,
#     theta=categories_closed,
#     fill='toself',
#     name="평가 결과",
#     marker=dict(color='blue')
# ))

# # 레이아웃 설정
# fig.update_layout(
#     polar=dict(
#         radialaxis=dict(
#             visible=True,
#             range=[0, 100]
#         )
#     ),
#     showlegend=False
# )

# # 평가 결과와 차트 배치
# left_col, right_col = st.columns([1, 2])

# # 평가 결과 표시
# with left_col:
#     st.subheader("평가 결과 요약")
#     for category, score in zip(categories, scores):
#         st.markdown(render_result_row(category, score), unsafe_allow_html=True)

# # 레이더 차트 출력
# with right_col:
#     st.subheader("Radar Chart")
#     st.plotly_chart(fig)


# In[2]:





# In[ ]:




