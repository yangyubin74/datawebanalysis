import datawebanalysis.module.sqlgen as sql
import pandas as pd

#########################플랫폼 가입도매 와 미 가입도매 분포#########################

#가입자, 비가입자 분포
def get_orm_member():

    rows=sql.select_org_member()
    if not rows:
       return pd.DataFrame(columns=['whole_name', 'org_nm'])
    
    # 데이터프레임 생성
    df = pd.DataFrame(rows, columns=['whole_name', 'org_nm'])
    #중복제거
    df = df.drop_duplicates(subset=['whole_name', 'org_nm'])     

    grouped_result = df.groupby(['whole_name', 'org_nm']).size().reset_index(name='count')

    not_n_count = grouped_result[grouped_result['org_nm'] == 'N']['count'].sum()  # 'N'의 총 개수
    n_count = grouped_result[grouped_result['org_nm'] != 'N']['count'].sum()  # 'N'이 아닌 값의 총 개수

    return (n_count,not_n_count)

def get_build_member():
    rows=sql.select_build_member()
    if not rows:
        return pd.DataFrame(columns=['bld_name','whole_name'])
    
    # 데이터프레임 생성
    df = pd.DataFrame(rows, columns=['bld_name','whole_name'])

    #중복제거
    df = df.drop_duplicates(subset=['bld_name','whole_name'])     

    grouped_result = df.groupby(['bld_name']).size().reset_index(name='count')
    return grouped_result

