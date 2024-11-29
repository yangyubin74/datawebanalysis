
import pandas as pd
import common as com
import sqlgen as sql

file_path = 'D:\\work\\analysis_data.csv'

columns = [
    'bld_name', 'flr_name', 'whole_no_name', 'whole_code', 'whole_name',
    'org_nm','union_uid', 'order_dt', 'buy_amt', 'return_yn', 'refund_yn', 'last_appr_status'
]

df = pd.read_csv(file_path,header=None, names=columns)

# 헤더명 할당과 값 할당
df = pd.read_csv(file_path,header=None, names=columns)

############################################################# Step1. 결측치 확인
com.user_print("결측치 확인","*",pd.isna(df).sum())

# 1. 'whole_no_name'이 결측치인 행 삭제
df = df.dropna(subset=['whole_no_name'])

# 2. 'org_nm' 결측치를 "N"으로 대체
df['org_nm'] = df['org_nm'].fillna("N")

# 3. 'return_yn' 결측치를 "N"으로 대체
df['return_yn'] = df['return_yn'].fillna("N")

# 결측치 재확인
com.user_print("결측치 재확인","*",df.isna().sum())

# 데이터 일부 확인
#com.user_print("데이터 일부 확인","*",df.head())

############################################################# Step2. 이상치 확인
# 기술 통계 확인
com.user_print("기술 통계 확인","*",df.describe())

# 이상치 확인
outliers = com.detect_outliers_iqr(df,'buy_amt')
com.user_print("이상치확인","*",outliers)

#boxplot 확인
com.box_plot(df['buy_amt'].dropna(),'Boxplot 이상치 확인')

#Z-Score
com.detect_outliers_zscore(df,'buy_amt')

# 이상치를 NaN으로 대체
#df.loc[df['z_score'].abs() > 3, 'buy_amt'] = None

# NaN을 중간값으로 대체
#df['buy_amt'] = df['buy_amt'].fillna(df['buy_amt'].median())

#분포 확인==>데이터가 많아서 그릴수 없음
#com.seaborn(df,'buy_amt')
#com.scatter(df,'buy_amt','order_dt')

#Isolation Forest 이상탐지
#com.isolationforest(df,'buy_amt')

############################################################# Step3. 표준화와 정규화(Skip)

#DB 생성
sql.create_db()
#DB Insert
sql.insert_db(df)


