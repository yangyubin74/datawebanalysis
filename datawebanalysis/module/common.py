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
import networkx as nx
import matplotlib.font_manager as fm
from sklearn.linear_model import LinearRegression

plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows의 경우 '맑은 고딕'
plt.rcParams['axes.unicode_minus'] = False  # 음수 기호 깨짐 방지
# for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
#         print(font)

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
    
    piechart=base64imageGeneration(plt)
    plt.close()              
    return piechart

def genbarchart(df,x_colomn,y_colum,Title,x_lable,y_label,with_size=8,height_size=6):
    """
    x_colomns=df["bld_name"]
    y_colums==df["count"]
    """

    random_colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(df))]

    plt.figure(figsize=(with_size,height_size))
    plt.bar(df[x_colomn], df[y_colum], color=random_colors)

    if Title !="" :
        plt.title(Title, fontsize=16)

    plt.xlabel(x_lable, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.xticks(fontsize=10, rotation=90) 
    plt.yticks(fontsize=10) 
    
    plt.tight_layout()
        
    barchart=base64imageGeneration(plt)
    plt.close()         
       
    return barchart

def genlinechart(df,x_colomn,y_colum,groupName,x_lable,y_label,with_size=8,height_size=6):
    """
     x_colomn: order_month
     y_colum: buy_amt
     groupName: bld_name
    """
    if pd.api.types.is_period_dtype(df[x_colomn]):
        df[x_colomn] = df[x_colomn].dt.to_timestamp()

    plt.figure(figsize=(with_size, height_size))
    for bld_name, group in df.groupby(groupName):
        plt.plot(group[x_colomn], group[y_colum], marker='o', label=bld_name)

    
    plt.xlabel(x_lable)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, 1.05), ncol=len(df['bld_name'].unique()))
    #plt.subplots_adjust(bottom=0.85)
    plt.grid(True)
    plt.tight_layout()
    line_chart=base64imageGeneration(plt)
    plt.close()       
    
    return line_chart

#소셜네트워크 분석 
def socalnetworkchart(df):
    
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_node(row["whole_code"], label=row["whole_name"], type="wholesaler")
        G.add_node(row["union_uid"], type="retailer")
        G.add_edge(row["whole_code"], row["union_uid"])

    plt.figure(figsize=(11, 6))
    pos = nx.spring_layout(G, seed=42,scale=2)  # 시각화를 위한 레이아웃 설정

    wholesaler_nodes = [node for node, attr in G.nodes(data=True) if attr["type"] == "wholesaler"]
    retailer_nodes = [node for node, attr in G.nodes(data=True) if attr["type"] == "retailer"]

    nx.draw_networkx_nodes(G, pos, nodelist=wholesaler_nodes, node_color='dodgerblue', node_size=300,label='Wholesalers')
    nx.draw_networkx_nodes(G, pos, nodelist=retailer_nodes, node_color='limegreen', node_size=50,  label='Retailers')
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5)

    # 노드 라벨 추가
    font_name = fm.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    
    wholesaler_labels = {node: G.nodes[node]["label"] for node in wholesaler_nodes}
    nx.draw_networkx_labels(G, pos, labels=wholesaler_labels, font_size=8,font_family=font_name)

    plt.legend()
    #plt.title("Wholesaler-Retailer Network")
    plt.tight_layout() 
    networkchart=base64imageGeneration(plt)
    plt.close() 

    return networkchart

#이동평균 예측 그리기
def averagepredictionchart(df,average_data):
    
    plt.figure(figsize=(10, 6))
    plt.plot(df['order_month'], df['buy_amt'], label='매출', marker='o')
    plt.plot(df['order_month'], df['moving_avg'], label='12개월 이동 평균', linestyle='--', color='orange')
    plt.axhline(y=average_data, color='red', linestyle='--', label=f'2024-12 예측: {int(average_data):,}원')
    
    plt.xlabel("월", fontsize=12)
    plt.ylabel("매출 (원)", fontsize=12)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    averagechart=base64imageGeneration(plt)
    plt.close() 
    return averagechart

#선형회귀 차트
def linearregressionchart(df,predicted_value,inear_prediction,model ):

    plt.figure(figsize=(10, 6))
    plt.scatter(df['order_dt_num'], df['buy_amt'], color='blue', label='Actual Sales', alpha=0.6)
    plt.plot(df['order_dt_num'], model.predict(df[['order_dt_num']]), color='orange', label='Regression Line')
    plt.scatter([inear_prediction], predicted_value, color='red', label=f'2024-12 Prediction: {int(predicted_value[0]):,}원')
   
    plt.xlabel("Time (Numeric Representation of Year-Month)", fontsize=12)
    plt.ylabel("Sales (Amount in Won)", fontsize=12)
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    linearrechart=base64imageGeneration(plt)
    plt.close() 
    return linearrechart

# base64코드 생성기
def base64imageGeneration(plt):
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64_chart = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()           
              
    return image_base64_chart
