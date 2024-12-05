
import datawebanalysis.module.sqlgen as sql
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA

#이동 평균 예측
def get_prediction_data():
    try:
        # 데이터베이스에서 데이터 가져오기
        df = sql.select_common_data()
        df=df[df['bld_name'] == '디오트']
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
 
 #이동평균 예측 데이터
def average_prediction_data(df):
    df['order_month'] = pd.to_datetime(df['order_month'], format='%Y-%m')
    df = df.sort_values('order_month')
    df['moving_avg'] = df['buy_amt'].rolling(window=12).mean().round(0)
    df['moving_avg'] = df['moving_avg'].fillna(0)
    df['moving_avg'].astype('int64')
    average_prediction = df['moving_avg'].iloc[-1].round(0)

    return (average_prediction,df)

#선형회귀로 예측 데이터
def linear_prediction_data(df):

    df['order_month'] = pd.to_datetime(df['order_month'], format='%Y-%m')
    # 숫자형으로 변환 (년도와 월을 연속적인 숫자로 처리)
    df['order_dt_num'] = df['order_month'].dt.year * 12 + df['order_month'].dt.month
    train_data = df[df['buy_amt'] > 0]
    X = train_data[['order_dt_num']].values
    y = train_data['buy_amt'].values
    model = LinearRegression()
    model.fit(X, y)
    #여기도 숫자로 변환
    inear_prediction=(2024 * 12) + 12
    predicted_value = model.predict([[inear_prediction]])
    return (predicted_value,inear_prediction,model)

def arima_prediction_data(df):
    df['order_month'] = pd.to_datetime(df['order_month'], format='%Y-%m')
    df['order_month2'] = df['order_month']
    df.set_index('order_month', inplace=True)
    
    # ARIMA 모델 적합
    model = ARIMA(df['buy_amt'], order=(1, 1, 1))
    model_fit = model.fit()

    # 2024-12월 매출 예측
    forecast = model_fit.forecast(steps=1)
    forecast_value = forecast.iloc[0]
    return (df,forecast,forecast_value)