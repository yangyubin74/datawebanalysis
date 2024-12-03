import datawebanalysis.module.sqlgen as sql
import pandas as pd


# 도매와 소매간의 연결강도 분석==> 연결 100개 이상의 도소매 연결
def get_social_network(from_value,to_value):

    df=sql.select_common_data()
    df=df[['whole_code', 'whole_name', 'union_uid']]

    counts = df.groupby('whole_code')['union_uid'].nunique().reset_index()
    counts.columns = ['whole_code', 'retail_count']

    # 상위 5% 임계값 계산
    #threshold = counts['retail_count'].quantile(0.95)
    # 상위 5% 도매 코드 필터링
    #rate_wholesale_codes = counts[counts['retail_count'] >= threshold]['whole_code']
    

    #중위 50%
    # q1 = counts['retail_count'].quantile(0.25)
    # q3 = counts['retail_count'].quantile(0.75)
    # rate_wholesale_codes = counts[(counts['retail_count'] >= q1) & (counts['retail_count'] <= q3)]['whole_code']
    
    # 가장 상위 등수로 추출 
    rate_wholesale_codes = counts.sort_values(by='retail_count', ascending=False).iloc[from_value:to_value]['whole_code']
    filtered_df = df[df['whole_code'].isin(rate_wholesale_codes)]
    
    return filtered_df
    