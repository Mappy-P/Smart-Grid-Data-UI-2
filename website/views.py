from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import models
from datetime import datetime
import optimisation

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':
        typeOfCalculation = request.form.get('typeOfCalculation')
        startDate = datetime.strptime(request.form.get('startDate'), '%Y-%m-%d')
        endDate = datetime.strptime(request.form.get('endDate'), '%Y-%m-%d')

        if startDate > endDate:
            flash("Your end-date cannot be before your start-date", category='error')

        else:
            duration = (endDate - startDate).days
            beginDateData = datetime.strptime('2018-01-11', '%Y-%m-%d')
            start = (startDate - beginDateData).days
            predictie = models.predictConsumptie(start, duration)
    else:
        predictie = None

    return render_template('demo.html', result = predictie)