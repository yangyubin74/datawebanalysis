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
from .module.prediction import get_average_prediction
import datawebanalysis.module.common as com

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
        build_member=get_build_member()
        build_sales=get_build_sales()
        build_sales_month=get_build_sales_month()
        

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

        average_prediction=get_average_prediction()
       
        result={
                 "result":"success",
                 "average":average_prediction.to_json(orient='records')
               }
        
    except  Exception as err:
        result={"result":"fail",'error': '%s' %(err)}
    
    return jsonify(result)
######################################### Prediction [E] ######################################## 