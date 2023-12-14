from .assets.optimisation.optimisation import ChargingPlanner
from .assets.optimisation.immediatecharging import DumbChargingPlanner
from .assets.optimisation.car import Car


def simulate_day(date, cars, predicted_consumption, predicted_consumption12, real_consumption, predicted_production, predicted_production12, real_production, predicted_prices, predicted_prices12, real_prices): # dynamic, 1 update

    average_predicted_price = sum(predicted_prices)/len(predicted_prices)
    average_real_price = sum(real_prices)/len(real_prices)
    predicted_injection_price = max(0, average_predicted_price/10)
    real_injection_price = max(0, average_real_price/10)
    charge_cap = 11/4

    predicted_surplus = [max(0., x-y) for x, y in zip(predicted_production, predicted_consumption)]
    predicted_surplus12 = [max(0., x-y) for x, y in zip(predicted_production12, predicted_consumption12)]
    print("pred surplus 12 len: ", len(predicted_surplus12))
    real_surplus = [max(0., x-y) for x, y in zip(real_production, real_consumption)]

    #print("prices")
    #print(predicted_prices)
    #print(real_prices)
    #print("surplus")
    #print(predicted_surplus)
    #print(real_surplus)
    #print("injection")
    #print(predicted_injection_price)
    #print(real_injection_price)


    #print(predicted_surplus)
    smartplanner = ChargingPlanner(predicted_surplus, predicted_prices, predicted_injection_price, charge_cap)
    #print(predicted_surplus)
    dumbplanner = DumbChargingPlanner(predicted_surplus, predicted_prices, predicted_injection_price, charge_cap)
    #print(predicted_surplus)

    for car in cars:
        smartplanner.add_car(car.get_to_charge_left(), car.get_start(), car.get_end())
        dumbplanner.add_car(car.get_to_charge_left(), car.get_start(), car.get_end())

    charged_cars_smart = smartplanner.get_cars()
    charged_cars_dumb = dumbplanner.get_cars()
    #print(len(charged_cars_smart))

    xs, yys_smart = charge_vis_data(charged_cars_smart)
    xs, yys_dumb = charge_vis_data(charged_cars_dumb)
    predicted_smart_cost = -smartplanner.get_predicted_profit()
    real_smart_cost = -smartplanner.get_real_profit(real_surplus, real_prices, real_injection_price)
    predicted_dumb_cost = -dumbplanner.get_predicted_profit()
    real_dumb_cost = -dumbplanner.get_real_profit(real_surplus, real_prices, real_injection_price)

    smartplanner.update(12*4, predicted_surplus12, predicted_prices12)
    dumbplanner.update(12*4, predicted_surplus12, predicted_prices12)

    charged_cars_smart_upd = smartplanner.get_cars()
    charged_cars_dumb_upd = dumbplanner.get_cars()

    xs_upd, yys_smart_upd = charge_vis_data(charged_cars_smart_upd)
    xs_upd, yys_dumb_upd = charge_vis_data(charged_cars_dumb_upd)
    predicted_smart_cost_upd = -smartplanner.get_predicted_profit()
    real_smart_cost_upd = -smartplanner.get_real_profit(real_surplus, real_prices, real_injection_price)
    predicted_dumb_cost_upd = -dumbplanner.get_predicted_profit()
    real_dumb_cost_upd = -dumbplanner.get_real_profit(real_surplus, real_prices, real_injection_price)

    print(predicted_smart_cost)
    print(predicted_smart_cost_upd)
    print(real_smart_cost)
    print(real_smart_cost_upd)
    print(predicted_dumb_cost)
    print(predicted_dumb_cost_upd)
    print(real_dumb_cost)
    print(real_dumb_cost_upd)
    #print(yys_smart)
    #print(yys_dumb)
    return xs_upd, yys_smart_upd, yys_dumb_upd, predicted_smart_cost_upd, real_smart_cost_upd, predicted_dumb_cost_upd, real_dumb_cost_upd

def charge_vis_data(cars):
    N = 24*4
    xs = [str(x//4)+":"+str((x % 4)*15).ljust(-len(str((x % 4)*15))) for x in range(N)]
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
