import datawebanalysis.module.sqlgen as sql
import pandas as pd


# ���ſ� �ҸŰ��� ���ᰭ�� �м�==> ���� 100�� �̻��� ���Ҹ� ����
def get_social_network(from_value,to_value):

    df=sql.select_common_data()
    df=df[['whole_code', 'whole_name', 'union_uid']]

    counts = df.groupby('whole_code')['union_uid'].nunique().reset_index()
    counts.columns = ['whole_code', 'retail_count']

    # ���� 5% �Ӱ谪 ���
    #threshold = counts['retail_count'].quantile(0.95)
    # ���� 5% ���� �ڵ� ���͸�
    #rate_wholesale_codes = counts[counts['retail_count'] >= threshold]['whole_code']
    

    #���� 50%
    # q1 = counts['retail_count'].quantile(0.25)
    # q3 = counts['retail_count'].quantile(0.75)
    # rate_wholesale_codes = counts[(counts['retail_count'] >= q1) & (counts['retail_count'] <= q3)]['whole_code']
    
    # ���� ���� ����� ���� 
    rate_wholesale_codes = counts.sort_values(by='retail_count', ascending=False).iloc[from_value:to_value]['whole_code']
    filtered_df = df[df['whole_code'].isin(rate_wholesale_codes)]
    
    return filtered_df
    