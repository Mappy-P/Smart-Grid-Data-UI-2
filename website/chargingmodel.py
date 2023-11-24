from .assets.optimisation.optimisation import ChargingPlanner
from .assets.optimisation.immediatecharging import DumbChargingPlanner
from .assets.optimisation.car import Car


def simulate_day(date, cars, predicted_consumption, real_consumption, predicted_production, real_production, predicted_prices, real_prices): # not dynamic: no updates on predicted data

    average_predicted_price = sum(predicted_prices)/len(predicted_prices)
    average_real_price = sum(real_prices)/len(real_prices)
    predicted_injection_price = max(0, average_predicted_price/10)
    real_injection_price = max(0, average_real_price/10)
    charge_cap = 11/4

    predicted_surplus = [x-y for x, y in zip(predicted_production, predicted_consumption)]

    smartplanner = ChargingPlanner(predicted_surplus, predicted_prices, predicted_injection_price, charge_cap)
    dumbplanner = DumbChargingPlanner(predicted_surplus, predicted_prices, predicted_injection_price, charge_cap)

    for car in cars:
        smartplanner.add_car(car.get_to_charge_left(), car.get_start(), car.get_end())
        dumbplanner.add_car(car.get_to_charge_left(), car.get_start(), car.get_end())

    charged_cars_smart = smartplanner.get_cars()
    charged_cars_dumb = dumbplanner.get_cars()
    print(len(charged_cars_smart))

    xs, yys_smart = charge_vis_data(charged_cars_smart)
    xs, yys_dumb = charge_vis_data(charged_cars_dumb)
    return xs, yys_smart, yys_dumb

def charge_vis_data(cars):
    N = 24*4
    xs = [*range(N)]
    yys = []
    for car in cars:
        ys = []
        for time in range(N):
            ys.append(car.get_charging(time))
        yys.append(ys)
    return xs, yys
    
#c1 = Car(1, 77, 32, 90)
#c2 = Car(2, 77, 21, 60)
#c3 = Car(3, 74.25, 21, 55)

#cars_to_add = [c1,c2,c3]
#simulate_day(0, cars_to_add)
