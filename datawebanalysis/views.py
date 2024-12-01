"""
Routes and views for the flask application.
"""

from datawebanalysis import app
from datetime import datetime
from flask import render_template,jsonify

from .module.baseanalysis import get_orm_member


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
@app.route('/home/getorgmember',methods=['GET'])
def getorgmember():
    result=""
    try:
        getorgmember =get_orm_member()
        result={
                 "result":"success",
                 "get_orm_member":getorgmember.to_json(orient='records')
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
