import csv

from .car import Car

class DumbChargingPlanner:

    def __init__(self, solar_surplus, energy_price, injection_price, charge_cap):
        self.cars = []
        self.number_of_cars = 0
        self.N = 24*4 #quarters per day
        self.solar_surplus = solar_surplus.copy()
        self.energy_price = energy_price.copy()
        self.injection_price = injection_price
        self.charge_cap = charge_cap
        self.predicted_solar_revenue = 0.
        self.energy_to_buy = [0] * self.N
        self.predicted_energy_cost = 0.

    #start_time inclusive end_time exclusive
    def add_car(self, to_charge, start_time, end_time):
        if (end_time-start_time)*self.charge_cap < to_charge:
            raise Exception('Car can never be charged :((')
        self.cars.append(Car(self.number_of_cars, to_charge, start_time, end_time))
        self.number_of_cars += 1
        self.__recompute(0) #offset 0

    #don't change whether loading or not for every point in time before offset (this is in the past)
    def update(self, offset, new_solar_surplus, new_energy_prices):
        for time in range(offset, self.N):
            self.solar_surplus[time] = new_solar_surplus[time]
            self.energy_price[time] = new_energy_prices[time]
        self.__recompute(offset)

    def __recompute(self, offset = 0):
        #print(self.solar_surplus)
        for car in self.cars:
            car.reset(0)
        #self.cars.sort(key=lambda car: car.get_end())
        #first loop -- charge with solar surplus
        self.predicted_solar_revenue = 0.
        self.energy_to_sell = self.solar_surplus.copy()
        #print(self.energy_to_sell)
        self.predicted_energy_cost = 0.
        self.energy_to_buy = [0]*self.N
        
        for car in self.cars:
            for time in range(car.get_start(), car.get_end() + 1):
                if self.energy_to_sell[time] > 0:
                    charge_amount = min(self.charge_cap, car.get_to_charge_left())
                    self.energy_to_sell[time] -= charge_amount
                    car.set_charging(time, charge_amount)
                else:
                    charge_amount = min(self.charge_cap, car.get_to_charge_left())
                    car.set_charging(time, charge_amount)
                    self.energy_to_buy[time] += charge_amount
                    
                    #print(self.predicted_energy_cost)
        #print('injection here')
        #print(self.injection_price)
        for time in range(self.N):
            if (self.energy_price[time] >= 0. and self.energy_to_sell[time] > 0):
                self.predicted_solar_revenue += min(self.energy_price[time], self.injection_price)*self.energy_to_sell[time]
        for time in range(self.N):
            self.predicted_energy_cost += self.energy_to_buy[time]*self.energy_price[time]
        self.cars.sort(key=lambda x: x.get_id())

    def get_scheme(self): # visual representation of charging scheme
        for car in self.cars:
            for time in range(self.N):
                if car.get_charging(time) > 0:
                    print('#',end='') # hash for if car is charging at that point in time
                else:
                    print('.',end='') # dot otherwise
            print()
        print('------------------------------------------------------------------------------------------------')

    def get_predicted_solar_revenue(self):
        return self.predicted_solar_revenue

    def get_real_solar_revenue(self, real_solar_surplus, real_energy_price, real_injection_price):
        real_solar_revenue = 0.
        #six = 24
        #ten = 89
        for time in range(self.N):
            if (real_energy_price[time] < 0.):
                continue
            energy_used = 0.
            for car in self.cars:
                energy_used += car.get_charging(time)
            energy_diff = energy_used - real_solar_surplus[time]
            if (energy_diff < 0.):
                real_solar_revenue += (-energy_diff)*min(real_injection_price, real_energy_price[time])
        return real_solar_revenue

    def get_predicted_energy_cost(self):
        return self.predicted_energy_cost

    def get_real_energy_cost(self, real_solar_surplus, real_energy_price):
        real_energy_cost = 0.
        #six = 24
        #ten = 89
        for time in range(self.N):
            energy_used = 0.
            for car in self.cars:
                energy_used += car.get_charging(time)
            energy_diff = energy_used - real_solar_surplus[time]
        
            if (energy_diff > 0.):
                real_energy_cost += energy_diff*real_energy_price[time]

        return real_energy_cost
 
    def get_predicted_profit(self):
        return self.get_predicted_solar_revenue() - self.get_predicted_energy_cost()

    def get_real_profit(self, real_solar_surplus, real_energy_price, real_injection_price):
        #print('predicted optimmised revenue')
        #print(self.predicted_solar_revenue)
        #print('predicted optimised cost')
        #print(self.predicted_energy_cost)
        return self.get_real_solar_revenue(real_solar_surplus, real_energy_price, real_injection_price) - self.get_real_energy_cost(real_solar_surplus, real_energy_price)


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
