"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template,jsonify
from datawebanalysis import app
from .module.baseanalysis import get_orm_member


TITLE="Y2B Company"
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
    result=get_orm_member()
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
