"""
Routes and views for the flask application.
"""

from datawebanalysis import app
from datetime import datetime
from flask import render_template,jsonify

from .module.baseanalysis import get_orm_member,get_build_member
import datawebanalysis.module.common as com

TITLE="Dankook University"
YEAR=datetime.now().year

######################################### Ȩ[S] ######################################## 
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
        
        piechart=com.genpiechart(
                ['플랫폼가입자','스마트노트가입자'],
                [n_count,not_n_count],''
            )
        barchart=com.genbarchart(build_member,'bld_name','count','','','')
        result={
                 "result":"success",
                 "piechart":piechart,
                 "barchart":barchart
               }
    except  Exception as err:
        result={"result":"fail",'error': '%s' %(err)}
    
    return jsonify(result)

######################################### Ȩ[E] ######################################## 

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=YEAR,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=YEAR,
        message='Your application description page.'
    )
