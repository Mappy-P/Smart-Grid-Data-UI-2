from optimisation.optimisation import ChargingPlanner
from optimisation.immediatecharging import DumbChargingPlanner

def simulate_day(date, cars): # not dynamic: no updates on predicted data
    predicted_consumption, real_consumption = models.predictConsumptie(date, 0)
    predicted_production, real_production = predictedProductie(date, 0)
    predicted_prices, real_prices = predictPrijzen(date, 0)

    predicted_consumption = [x * 0.8 for x in predicted_consumption]
    real_consumption = [x * 0.8 for x in real_consumption]

    average_predicted_price = sum(predicted_prices)/len(predicted_prices)
    average_real_price = sum(real_prices)/len(real_prices)
    predicted_injection_price = max(0, average_predicted_price/10)
    real_injection_price = max(0, average_real_price/10)
    charge_cap = 11/4

    predicted_surplus = predicted_production-predicted_consumption

    planner = ChargingPlanner(predicted_surplus, predicted_prices, predicted_injection_price, charge_cap)
    dumbplanner = DumbChargingPlanner(predicted_surplus, predicted_price, charge_cap)

    charged_cars_smart = planner.get_cars()
    charged_cars_dumb = dumbplanner.get_cars()


def create_charge_vis(cars):
    pass #TODO: create visualisation with matplotlib
    
c1 = Car(1, 77, 32, 90)
c2 = Car(2, 77, 21, 60)
c3 = Car(3, 74.25, 21, 55)

cars_to_add = [c1,c2,c3]
simulate_day(123, cars_to_add)