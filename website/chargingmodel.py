from assets.optimisation.optimisation import ChargingPlanner
from assets.optimisation.immediatecharging import DumbChargingPlanner
from assets.optimisation.car import Car
import models

def simulate_day(date, cars): # not dynamic: no updates on predicted data
    predicted_consumption, real_consumption = models.predictConsumptie(date, 0)
    predicted_production, real_production = models.predictProductie(date, 0)
    predicted_prices, real_prices = models.predictPrijzen(date, 0)

    predicted_consumption = [x * 0.8 for x in predicted_consumption]
    real_consumption = [x * 0.8 for x in real_consumption]

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

    create_charge_vis(charged_cars_dumb)
    create_charge_vis(charged_cars_smart)


def create_charge_vis(cars):
    N = 24*4
    for car in cars:
        for time in range(N): 
            if car.get_charging(time) > 11/4*0.99: # hash if car is charging at that point in time at full capacity
                print('#',end='')
            elif car.get_charging(time) > 0.45: # circle if car is charging at that point in time at partial capacity
                print('o',end='')
            else: # dit if car is not charging
                print('.',end='')
        print()
    print('------------------------------------------------------------------------------------------------')
    
c1 = Car(1, 77, 32, 90)
c2 = Car(2, 77, 21, 60)
c3 = Car(3, 74.25, 21, 55)

cars_to_add = [c1,c2,c3]
simulate_day(123, cars_to_add)
