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
        #print(typeOfCalculation)
        #print(request.form.get('startDate'))
        #print(request.form.get('endDate'))
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
            if start < 0 or duration + start > 2082:
                predictie = None
                datums = None
                werkelijk = None
                soort = None
                flash("Choose a start-date and end-date between 16-01-2018 and 29-09-2023!", category='error')
                return render_template('demo.html', result = predictie, datums = datums, werkelijk = werkelijk)
            if typeOfCalculation == '1':
                predictionResults = models.predictConsumptie(start, duration)
            elif typeOfCalculation == '2':
                predictionResults = models.predictProductie(start, duration)
            elif typeOfCalculation == '3':
                predictionResults = models.predictPrijzen(start, duration)
            elif typeOfCalculation == '4':
                cars = list()
                for i in range(6):
                    #print("i: ", i)
                    try:
                        #print(request.form.get(('aankomstUur' + str(i + 1))))
                        aankomst = int(request.form.get(('aankomstUur' + str(i + 1)))[0:2])*4 + int(request.form.get(('aankomstUur' + str(i + 1)))[3:])/15
                        aankomst = int(aankomst)
                        #print(aankomst)
                        vertrek = int(request.form.get(('vertrekUur' + str(i + 1)))[0:2])*4 + int(request.form.get(('vertrekUur' + str(i + 1)))[3:])/15
                        vertrek = int(vertrek)
                        #print(vertrek)
                        #print('auto ' + str(i + 1))
                        #print(request.form.get('percentageGewenst1'))
                        #print(request.form.get('percentageGewenst' + str(i + 1)))
                        teLaden = float(request.form.get('percentageGewenst' + str(i + 1))) - float(request.form.get('percentageAankomst' + str(i + 1)))
                        #print("here")
                        optie = int(request.form.get('optie' + str(i+1)))
                        #print("there")
                        print("optie: ", optie)
                        totalebatterij = 1
                        if optie == 1:
                            totalebatterij = 15
                        elif optie == 2:
                            totalebatterij = 75
                        else:
                            print("niet de bedoeling")

                        newcar = Car(i + 1, teLaden/100.0 * totalebatterij, aankomst, vertrek)
                        cars.append(newcar)
                    except:

                        break

                cars = np.asarray(cars)
                #print('Dit zijn de autos:')
                #print(cars)

                xs, yys_smart, yys_dumb, predicted_smart_cost, real_smart_cost, predicted_dumb_cost, real_dumb_cost = models.simulate(start, cars)
                power_smart = [sum(col) for col in zip(*yys_smart)]
                power_dumb = [sum(col) for col in zip(*yys_dumb)]
                #print(power_smart)
                #print(power_dumb)
                predicted_smart_cost = str(round(predicted_smart_cost/100, 2))
                real_smart_cost = str(round(real_smart_cost/100, 2))
                predicted_dumb_cost = str(round(predicted_dumb_cost/100, 2))
                real_dumb_cost = str(round(real_dumb_cost/100, 2))
                predictie = None
                datums = None
                werkelijk = None
                soort = None
                #print(len(cars))
                #print(len(yys_smart))
                return render_template('charge.html', xs = xs, smart = yys_smart, dumb = yys_dumb, predicted_smart_cost = predicted_smart_cost, real_smart_cost = real_smart_cost, predicted_dumb_cost = predicted_dumb_cost, real_dumb_cost = real_dumb_cost, power_smart = power_smart, power_dumb = power_dumb)
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

#@views.route('/charge', methods=['GET', 'POST'])
#def charge():
#    xs = []
#    yys_smart = [[]]
#    yys_dumb = [[]]
#
#    if request.method == 'POST':
#        chosen_date = datetime.strptime(request.form.get('chosenDate'), '%Y-%m-%d')
#        beginDateData = datetime.strptime('2018-01-16', '%Y-%m-%d')
#        date = (chosen_date - beginDateData).days
#        c1 = Car(1, 77, 32, 90)
#        c2 = Car(2, 66, 25, 60)
#     c3 = Car(3, 63.25, 25, 55)

#     cars_to_add = [c1,c2,c3]
#     xs, yys_smart, yys_dumb, predicted_smart_cost, real_smart_cost, predicted_dumb_cost, real_dumb_cost = models.simulate(date, cars_to_add)
#     predicted_smart_cost = str(round(predicted_smart_cost/100, 2))
#     real_smart_cost = str(round(real_smart_cost/100, 2))
#     predicted_dumb_cost = str(round(predicted_dumb_cost/100, 2))
#     real_dumb_cost = str(round(real_dumb_cost/100, 2))
#     #print(real_dumb_cost)
#     #yys_smart = zip(yys_smart)
#     #yys_dumb = zip(yys_dumb)
#     return render_template('charge.html', xs = xs, smart = yys_smart, dumb = yys_dumb, predicted_smart_cost = predicted_smart_cost, real_smart_cost = real_smart_cost, predicted_dumb_cost = predicted_dumb_cost, real_dumb_cost = real_dumb_cost)

# return render_template('charge.html', xs = xs, smart = yys_smart, dumb = yys_dumb)