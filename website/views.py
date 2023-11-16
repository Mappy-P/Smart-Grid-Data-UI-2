from flask import Blueprint, render_template, request, redirect, url_for
#from optimisation.optimisation import ChargingPlanner

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
        startDate = request.form.get('startDate')
        endDate = request.form.get('endDate')
    return render_template('demo.html')

@views.route('/aboutus')
def aboutus():
    return render_template('about_us.html')