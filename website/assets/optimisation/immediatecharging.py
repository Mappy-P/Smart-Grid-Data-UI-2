import csv

from assets.optimisation.car import Car

class DumbChargingPlanner:

    def __init__(self, solar_surplus, energy_price, injection_price, charge_cap):
        self.cars = []
        self.number_of_cars = 0
        self.N = 24*4 #quarters per day
        self.solar_surplus = solar_surplus
        self.energy_price = energy_price
        self.injection_price = injection_price
        self.charge_cap = charge_cap
        self.solar_revenue = 0.
        self.energy_to_buy = [0] * self.N
        self.energy_cost = 0.

    #start_time inclusive end_time exclusive
    def add_car(self, to_charge, start_time, end_time):
        if (end_time-start_time)*charge_cap < to_charge:
            raise Exception('Car can never be charged :((')
        self.cars.append(Car(self.number_of_cars, to_charge, start_time, end_time))
        self.number_of_cars += 1
        self.__recompute(0) #offset 0

    #don't change whether loading or not for every point in time before offset (this is in the past)
    def update(self, offset, new_solar_surplus, new_energy_prices):
        self.solar_surplus = new_solar_surplus
        self.energy_price = new_energy_prices
        self.__recompute(offset)
        self.solar_surplus = new_solar_surplus
        self.energy_price = new_energy_prices
        self.__recompute(offset)

    def __recompute(self, offset = 0):
        self.cars.sort(key=lambda car: car.get_end())
        #first loop -- charge with solar surplus
        self.solar_revenue = 0.
        energy_to_sell = self.solar_surplus
        
        for car in self.cars:
            for time in range(car.get_start(), car.get_end() + 1):
                if car.get_to_charge_left() > 0:
                    charge_amount = min(charge_cap, car.get_to_charge_left())
                    energy_to_sell[time] -= charge_amount
                    car.set_charging(time, charge_amount)
                else:
                    charge_amount = min(charge_cap, car.get_to_charge_left())
                    car.set_charging(time, charge_amount)
                    self.energy_to_buy[time] += charge_amount
                    self.energy_cost += charge_amount * energy_price[time]
        self.solar_revenue = injection_price*sum(energy_to_sell)
        
        
 
    def get_scheme(self): # visual representation of charging scheme
        for car in self.cars:
            for time in range(self.N):
                if car.get_charging(time) > 0:
                    print('#',end='') # hash for if car is charging at that point in time
                else:
                    print('.',end='') # dot otherwise
            print()
        print('------------------------------------------------------------------------------------------------')

    def get_expected_energy_cost(self):
        return self.energy_cost

    def get_real_energy_cost():
        pass

    def get_solar_revenue(self):
        return self.solar_revenue

    def get_profit(self):
        return self.solar_revenue - self.energy_cost

    def get_cars(self):
        return self.cars


#c1 = Car(1, 77, 32, 90)
#c2 = Car(2, 77, 21, 60)
#c3 = Car(3, 74.25, 21, 55)

#cars_to_add = [c1,c2,c3]

#file = open('website/assets/optimisation/examples/energie2018-10-09.csv', encoding='utf-8-sig')
#csvreader = csv.reader(file)

#available_solar = []
#for row in csvreader:
#    available_solar.append(float(row[0])/10)

#file = open('website/assets/optimisation/examples/stroomprijs1-01-18.csv', encoding='utf-8-sig')
#csvreader = csv.reader(file)

#energy_price = []
#for row in csvreader:
#    energy_price.append(float(row[0])/100) #prijs in cent

#charge_cap = 11/4
#injection_price = 0.1

#planner = DumbChargingPlanner(available_solar, energy_price, injection_price, charge_cap)
#for car in cars_to_add:
#    planner.add_car(car.get_to_charge_left(), car.get_start(), car.get_end())

#planner.get_scheme()
#print(planner.get_profit())
#print(planner.get_expected_energy_cost())
#print(planner.get_solar_revenue())
