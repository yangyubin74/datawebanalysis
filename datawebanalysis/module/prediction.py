
import datawebanalysis.module.sqlgen as sql
import pandas as pd

#이동 평균 예측
def get_average_prediction():
    try:
        # 데이터베이스에서 데이터 가져오기
        df = sql.select_common_data()

        # 데이터 전처리
        df['buy_amt'] = df['buy_amt'].astype('int64')
        df['order_dt'] = pd.to_datetime(df['order_dt'])
        df['order_month'] = pd.to_datetime(df['order_dt']).dt.to_period('M')

        # 그룹화 및 결과 생성
        filtered_df = df.groupby(['bld_name', 'order_month'], as_index=False)['buy_amt'].sum()
        filtered_df['order_month'] = filtered_df['order_month'].astype(str)

        return filtered_df
    except Exception as e:
        # 에러 로그 추가
        print(f"Error in get_average_prediction: {e}")
        raise  # 예외를 다시 발생시켜 호출자에게 전달