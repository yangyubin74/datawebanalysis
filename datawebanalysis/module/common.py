import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 비GUI 백엔드 설정
import matplotlib.pyplot as plt
from scipy.stats import zscore
import seaborn as sns
from sklearn.ensemble import IsolationForest
import base64
from io import BytesIO
import random


plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows의 경우 '맑은 고딕'
plt.rcParams['axes.unicode_minus'] = False  # 음수 기호 깨짐 방지

def user_print(title, border_char="#",content=""):
        
    border = border_char * 20
    print(f"\n{border} {title}[S] {border}")
    print(content);
    print(f"{border} {title}[E] {border}")


# IQR을 이용한 이상치 탐지
def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers

#Z-Score를 이용한 이상치 탐지
#일반적으로 Z-Score가 3을 초과하면 이상치로 간주
def detect_outliers_zscore(df, column):

    # Z-Score 계산
    df['z_score'] = zscore(df[column].dropna())
    # Z-Score 기준 이상치 탐지
    outliers = df[df['z_score'].abs() > 3]
    user_print('Z-Score based outliers','*',outliers)

#박스 플롯(Box Plot) 시각화
def box_plot(data,title,vert=False):
    plt.boxplot(data, vert=False)
    plt.title(title)
    plt.xlabel('Value')
    plt.show()

#분포 확인 (히스토그램/커널 밀도 플롯)
def seaborn(df,column):
    sns.histplot(df[column].dropna(), kde=True)
    plt.title(f"Distribution of '{column}'")
    plt.show()
#산점도
def scatter(df,column1,column2):
    plt.scatter(df[column2], df[column1])
    plt.title('일자별 분포')
    plt.xlabel( f'구매 일자 {(column2)}')
    plt.ylabel(f'구매 금액 {(column1)}')
    plt.grid(True)
    plt.show()


#Isolation Forest 이상탐지(머신러닝 모델 활용)
# 데이터의 5%를 이상치로 간주
def isolationforest(df,column):
    model = IsolationForest(contamination=0.05)  
    df['anomaly'] = model.fit_predict(df[[column]])   

    # 이상치 확인
    anomalies = df[df['anomaly'] == -1]
    user_print('Isolation Forest Detected Anomalies','*',anomalies)

#파이차트 생성
def genpiechart(labels, sizes, Title="Pie Chart"):
    """
    labels: 각 항목의 이름 리스트 (예: ['N', 'Not N'])
    sizes: 각 항목의 크기 리스트 (예: [3, 4])
    title: 파이 차트의 제목 (기본값: "Pie Chart")
    """
    plt.figure(figsize=(6, 6))
    plt.pie(
        sizes,
        labels=labels,
        autopct=lambda p: f'{p:.1f}%' if p > 0 else '',  # 퍼센트 레이블
        startangle=90
    )
    if Title !="" :
        plt.title(Title, fontsize=16)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64_piechart = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()           

    plt.close()              
    return image_base64_piechart

def genbarchart(df,x_colomn,y_colum,Title,x_lable,y_label):
    """
    x_colomns=df["bld_name"]
    y_colums==df["count"]
    """

    random_colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(df))]

    plt.figure(figsize=(8, 6))
    plt.bar(df[x_colomn], df[y_colum], color=random_colors)

    if Title !="" :
        plt.title(Title, fontsize=16)

    plt.xlabel(x_lable, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.xticks(fontsize=10, rotation=90) 
    plt.yticks(fontsize=10) 
    
    plt.tight_layout()
    plt.show()
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64_piechart = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()           

    plt.close()              
    return image_base64_piechart
