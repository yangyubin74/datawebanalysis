"""
Routes and views for the flask application.
"""

from ast import Import

from numpy import int16
from datawebanalysis import app
from datetime import datetime
from flask import render_template,jsonify

from .module.baseanalysis import get_orm_member,get_build_member,get_build_sales,get_build_sales_month
from .module.socialanalysis import get_social_network
from .module.prediction import get_prediction_data,average_prediction_data,linear_prediction_data,arima_prediction_data
import datawebanalysis.module.common as com
import pandas as pd

TITLE="Dankook University"
YEAR=datetime.now().year

######################################### Home [S] ######################################## 
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title=TITLE,
        year=YEAR
    )

#가입도매, 미 가입도매 ==> 파이차트 getorgmember.to_json(orient='records')
@app.route('/home/getorgmember',methods=['GET'])
def getorgmember():
    result=""
    try:
        (n_count,not_n_count) =get_orm_member()
        com.user_print("가입자분포현황",'#', f"\n 플랫폼 가입자: {n_count} 스마트노트 거입자: {not_n_count}")
        
        build_member=get_build_member()
        com.user_print("상가별분포",'#',build_member.head())

        build_sales=get_build_sales()
        com.user_print("건물별 매출현황",'#',build_sales.head())

        build_sales_month=get_build_sales_month()
        com.user_print("건물별 매출추이",'#',build_sales_month.head())

        piechart=com.genpiechart(
                ['플랫폼가입자','스마트노트가입자'],
                [n_count,not_n_count],''
            )
        barchart=com.genbarchart(build_member,'bld_name','count','','상가','도매수')
        barchart2=com.genbarchart(build_sales,'bld_name','buy_amt','','상가','매출(단위:백억)',12,6)
        linechart=com.genlinechart(build_sales_month,'order_month','buy_amt','bld_name','년/월','매출(단위:백억)',12,8)
        result={
                 "result":"success",
                 "piechart":piechart,
                 "barchart":barchart,
                 "barchart2":barchart2,
                 "linechart":linechart,
                 "build_sales_month":build_sales_month.to_json(orient='records')
               }
    except  Exception as err:
        result={"result":"fail",'error': '%s' %(err)}
    
    return jsonify(result)

######################################### Home [E] ######################################## 

######################################### Social [S] ######################################## 

@app.route('/social')
def social():
    """Renders the contact page."""
    return render_template(
        'social.html',
        title=TITLE,
        year=YEAR
    )

@app.route('/social/getsocaildata/<from_value>/<to_value>',methods=['GET'])
def getsocaildata(from_value,to_value):
    result=""
    try:
        social_network=get_social_network(int16(from_value),int16(to_value))
        networkchart=com.socalnetworkchart(social_network)         
        com.user_print("도매와 소매의 Socail N/W Analysis",'#',social_network.head())
        result={
                 "result":"success",
                 "networkchart":networkchart,
                 "socialdata":social_network.to_json(orient='records')
               }
    except  Exception as err:
        result={"result":"fail",'error': '%s' %(err)}
    
    return jsonify(result)
######################################### Social [E] ######################################## 

@app.route('/kmeans')
def kmeans():
    """Renders the about page."""
    return render_template(
        'kmeans.html',
        title=TITLE,
        year=YEAR
    )

######################################### Prediction [S] ######################################## 
@app.route('/prediction')
def prediction():
    """Renders the about page."""
    return render_template(
        'prediction.html',
        title=TITLE,
        year=YEAR
    )
#이동평균 예측
@app.route('/prediction/getaverageprediction',methods=['GET'])
def getaverageprediction():
    result=""
    try:

        #기본 데이터 조회
        df=get_prediction_data()

        #이동평균 데이터 및 차트
        (average_data,df)=average_prediction_data(df)
        average_data_chart=com.averagepredictionchart(df,average_data)
        new_row = {
            "bld_name": "디오트",
            "order_month": pd.to_datetime("2024-12", format='%Y-%m'),
            "buy_amt": 0,
            "moving_avg": average_data  # 예측된 이동 평균 값
         }

        #선형회귀 예측
        df2=get_prediction_data()
        (predicted_value,inear_prediction,model)=linear_prediction_data(df2)
        linear_data_chart=com.linearregressionchart(df2,predicted_value,inear_prediction,model)
        new_row2 = {
            "bld_name": "디오트",
            "order_month": pd.to_datetime("2024-12", format='%Y-%m'),
            "buy_amt": predicted_value.round(0),
            "order_dt_num":inear_prediction
         }
        #ARIMA 예측
        df3=get_prediction_data()
        (df3,forecast,forecast_value)=arima_prediction_data(df3)
        arima_data_chart=com.arimapredictionchart(df3,forecast)
        new_row3 = {
            "bld_name": "디오트",
            "order_month2": pd.to_datetime("2024-12", format='%Y-%m'),
            "buy_amt": forecast.round(0)  
         }
        
        result={
                 "result":"success",
                 "average_data": pd.concat([df, pd.DataFrame([new_row])], ignore_index=True).to_json(orient='records'),
                 "average_data_chart":average_data_chart,
                 "linear_data_chart":linear_data_chart,
                 "linear_data":pd.concat([df2, pd.DataFrame([new_row2])], ignore_index=True).to_json(orient='records'),
                 "arima_data_chart":arima_data_chart,
                 "arima_data":pd.concat([df3, pd.DataFrame([new_row3])], ignore_index=True).to_json(orient='records')
               }
    except  Exception as err:
        result={"result":"fail",'error': '%s' %(err)}
    
    return jsonify(result)
######################################### Prediction [E] ######################################## 