from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import models
from datetime import datetime
from .assets import optimisation
from .assets.optimisation.car import Car
import numpy as np

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/about')
def about():
    return render_template('about.html')

@views.route('/data')
def data():
    return render_template('data_optimization.html')

@views.route('/about-us')
def about_us():
    return render_template('about_us.html')

@views.route('/ml')
def ml():
    return render_template('ml.html')

@views.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':
        typeOfCalculation = request.form.get('typeOfCalculation')
        print(typeOfCalculation)
        print(request.form.get('startDate'))
        print(request.form.get('endDate'))
        startDate = datetime.strptime(request.form.get('startDate'), '%Y-%m-%d')
        endDate = datetime.strptime(request.form.get('endDate'), '%Y-%m-%d')

        if startDate > endDate:
            flash("Your end-date cannot be before your start-date", category='error')
            predictie = None
            datums = None
            werkelijk = None
            soort = None
        else:
            duration = (endDate - startDate).days
            beginDateData = datetime.strptime('2018-01-16', '%Y-%m-%d')
            start = (startDate - beginDateData).days
            if typeOfCalculation == '1':
                predictionResults = models.predictConsumptie(start, duration)
            elif typeOfCalculation == '2':
                predictionResults = models.predictProductie(start, duration)
            elif typeOfCalculation == '3':
                predictionResults = models.predictPrijzen(start, duration)
            elif typeOfCalculation == '4':
                cars = list()
                for i in range(5):
                    try:
                        aankomst = int(request.form.get('aankomstUur')[0:2])*4 + int(request.form.get('aankomstUur')[3:])/15
                        vertrek = int(request.form.get('vertrekUur')[0:2])*4 + int(request.form.get('vertrekUur')[3:])/15
                        cars.append(Car(i + 1, float(request.form.get('gewenstPercentage' + str(i + 1))) - float(request.form.get('huidigPercentage' + str(i + 1))), aankomst, vertrek))
                    except:
                        break
                cars = np.asarray(cars)

                xs, yys_smart, yys_dumb = models.simulate(start, cars)
                predictie = None
                datums = None
                werkelijk = None
                soort = None
                return render_template('charge.html', xs = xs, smart = yys_smart, dumb = yys_dumb)
            elif typeOfCalculation == '0':
                flash('Choose the type of calculation you want our model to run.', category='error')
                predictie = None
                datums = None
                werkelijk = None
                soort = None
                return render_template('demo.html', result = predictie, datums = datums, werkelijk = werkelijk)
            predictie = predictionResults[0]
            werkelijk = predictionResults[1]
            soort = predictionResults[2]
            datums = predictionResults[3]
    else:
        predictie = None
        datums = None
        werkelijk = None
        soort = None

    return render_template('demo.html', result = predictie, datums = datums, werkelijk = werkelijk, soort = soort)

@views.route('/charge', methods=['GET', 'POST'])
def charge():
    xs = []
    yys_smart = [[]]
    yys_dumb = [[]]

    if request.method == 'POST':
        chosen_date = datetime.strptime(request.form.get('chosenDate'), '%Y-%m-%d')
        beginDateData = datetime.strptime('2018-01-16', '%Y-%m-%d')
        date = (chosen_date - beginDateData).days
        c1 = Car(1, 77, 32, 90)
        c2 = Car(2, 66, 25, 60)
        c3 = Car(3, 63.25, 25, 55)

        cars_to_add = [c1,c2,c3]
        xs, yys_smart, yys_dumb = models.simulate(date, cars_to_add)
        #yys_smart = zip(yys_smart)
        #yys_dumb = zip(yys_dumb)
        return render_template('charge.html', xs = xs, smart = yys_smart, dumb = yys_dumb)

    return render_template('charge.html', xs = xs, smart = yys_smart, dumb = yys_dumb)