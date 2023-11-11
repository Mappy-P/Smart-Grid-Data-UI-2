from flask import Blueprint, render_template, request, redirect, url_for
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
    if request.method == "POST":
        datum = request.form["dt"]
        return redirect(url_for("datum", dt = datum))
    else:
        return render_template('demo.html')
    
@views.route('/demo1', methods=['GET', 'POST'])
def demo1():
    optimisation.ChargingPlanner(available_solar, energy_price, injection_price, charge_cap)
    c1 = Car(1, 77, 32, 90)
    c2 = Car(2, 77, 21, 60)
    c3 = Car(3, 74.25, 21, 55)

    cars_to_add = [c1,c2,c3]

    file = open('examples/energie2018-10-09.csv', encoding='utf-8-sig')
    csvreader = csv.reader(file)

    available_solar = []
    for row in csvreader:
        available_solar.append(float(row[0])/10)

    file = open('examples/stroomprijs1-01-18.csv', encoding='utf-8-sig')
    csvreader = csv.reader(file)

    energy_price = []
    for row in csvreader:
        energy_price.append(float(row[0])/100) #prijs in cent

    charge_cap = 11/4
    injection_price = 0.1

    planner = optimisation.ChargingPlanner(available_solar, energy_price, injection_price, charge_cap)
    for car in cars_to_add:
        optimisation.planner.add_car(car.get_to_charge_left(), car.get_start(), car.get_end())

    laadschema = optimisation.planner.get_scheme()
    
    return f"<h1>{laadschema}</h1>"

@views.route("/<datum>")
def datum(dt):
    optimisation.ChargingPlanner(available_solar, energy_price, injection_price, charge_cap)
    c1 = Car(1, 77, 32, 90)
    c2 = Car(2, 77, 21, 60)
    c3 = Car(3, 74.25, 21, 55)

    cars_to_add = [c1,c2,c3]

    file = open('examples/energie2018-10-09.csv', encoding='utf-8-sig')
    csvreader = csv.reader(file)

    available_solar = []
    for row in csvreader:
        available_solar.append(float(row[0])/10)

    file = open('examples/stroomprijs1-01-18.csv', encoding='utf-8-sig')
    csvreader = csv.reader(file)

    energy_price = []
    for row in csvreader:
        energy_price.append(float(row[0])/100) #prijs in cent

    charge_cap = 11/4
    injection_price = 0.1

    planner = optimisation.ChargingPlanner(available_solar, energy_price, injection_price, charge_cap)
    for car in cars_to_add:
        optimisation.planner.add_car(car.get_to_charge_left(), car.get_start(), car.get_end())

    laadschema = optimisation.planner.get_scheme()
    
    return f"<h1>{laadschema}</h1>"