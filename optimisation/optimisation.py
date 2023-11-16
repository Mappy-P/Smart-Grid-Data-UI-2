import csv
from optimisation.car import Car

   
class ChargingPlanner:

    def __init__(self, solar_surplus, energy_price, injection_price, charge_cap):
        self.cars = []
        self.number_of_cars = 0
        self.N = 24*4 #quarters per day
        self.solar_surplus = solar_surplus
        self.energy_price = energy_price
        self.injection_price = injection_price
        self.charge_cap = charge_cap
        self.predicted_solar_revenue = 0.
        self.predicted_energy_cost = 0.
        self.energy_to_sell = solar_surplus.copy()
        self.energy_to_buy = [0.]*self.N
        self.EPS = 1E-5

    #start_time inclusive end_time exclusive
    def add_car(self, to_charge, start_time, end_time):
        if (end_time-start_time)*charge_cap < to_charge:
            raise Exception('Car can never be charged :((')
        self.cars.append(Car(self.number_of_cars, to_charge, start_time, end_time))
        self.number_of_cars += 1
        self.__recompute(start_time)

    #don't change whether loading or not for every point in time before offset (this is in the past)
    def update(self, offset, new_solar_surplus, new_energy_prices):
        self.solar_surplus = new_solar_surplus
        self.energy_price = new_energy_prices
        self.__recompute(offset)

    def __recompute(self, offset):
        for car in self.cars:
            car.reset(offset)
        #for car in self.cars:
        #    print(car.get_id(), ' tocharge ',car.get_to_charge_left())
        self.cars.sort(key=lambda car: car.get_to_charge_left()/(car.get_end()-max(car.get_start(), offset)), reverse=True)
        #self.cars.sort(key=lambda car: car.get_end())
        #first loop -- charge with solar surplus
        self.solar_revenue = 0.
        for time in range(offset, self.N):
            self.energy_to_sell[time] = self.solar_surplus[time]

        for time in range(offset, self.N):
            i = 0
            while self.energy_to_sell[time] > 0:
                while i < len(self.cars) and (time < self.cars[i].get_start() or time >= self.cars[i].get_end() or self.cars[i].to_charge <= 0):
                    i += 1

                if i >= len(self.cars):
                    break
                car = self.cars[i]
                charge_amount = min(self.charge_cap, car.get_to_charge_left(), self.energy_to_sell[time])
                #print('tc', car.get_to_charge())
                car.set_charging(time, charge_amount)
                self.energy_to_sell[time] -= charge_amount
                i += 1
        self.predicted_solar_revenue = 0.
        for time in range(self.N):
            if (energy_price[time] >= injection_price): # VRAAG JORIS
                self.predicted_solar_revenue += self.energy_to_sell[time]*injection_price
        self.get_scheme()

        #for car in self.cars:
            #print(car.get_id(), ' tocharge ',car.get_to_charge_left())


        #second loop -- complete charging with electricity grid
        self.predicted_energy_cost = 0.
        for time in range(offset, self.N):
            self.energy_to_buy[time] = 0.
        
        for car in self.cars:
            if car.get_to_charge_left() <= 0:
                continue
            time_price = []
            for time in range(max(car.get_start(),offset), car.get_end()):
                if (car.get_charging(time) >= self.charge_cap):
                    continue
                else:
                    time_price.append((time, self.energy_price[time]))
            time_price.sort(key=lambda x: x[1])
            i = 0
            #print(time_price)
            charging_possible = 0.
            #for (time, price) in time_price:
            #    charging_possible += self.charge_cap-car.get_charging(time)
            #print(charging_possible)

            while car.get_to_charge_left() > self.EPS:
                #print(car.get_id())
                #print(car.get_to_charge_left())

                if (i == len(time_price)):
                    raise Exception('ERROR: not able to charge everything even though we should be able to')
                    break
                else:
                    charge_amount = min(car.get_to_charge_left(), self.charge_cap-                                                                          car.get_charging(time_price[i][0]))
                    car.set_charging(time_price[i][0], charge_amount)
                    self.energy_to_buy[time_price[i][0]] += charge_amount
                    i += 1
        for time in range(self.N):
            self.predicted_energy_cost += self.energy_to_buy[time]*self.energy_price[time]
        self.get_scheme()

    def get_scheme(self): # visual representation of charging scheme
        for car in self.cars:
            for time in range(self.N): 
                if car.get_charging(time) > 11/4*0.99: # hash if car is charging at that point in time at full capacity
                    print('#',end='')
                elif car.get_charging(time) > 0.45: # circle if car is charging at that point in time at partial capacity
                    print('o',end='')
                else: # dit if car is not charging
                    print('.',end='')
            print()
        print('------------------------------------------------------------------------------------------------')

    def get_predicted_energy_cost(self):
        return self.predicted_energy_cost

    def get_real_energy_cost():
        pass

    def get_predicted_solar_revenue(self):
        return self.predicted_solar_revenue

    def get_predicted_profit(self):
        return self.predicted_solar_revenue-self.predicted_energy_cost

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

planner = ChargingPlanner(available_solar, energy_price, injection_price, charge_cap)
for car in cars_to_add:
    planner.add_car(car.get_to_charge_left(), car.get_start(), car.get_end())

#planner.get_scheme()
print(planner.get_predicted_solar_revenue())
print(planner.get_predicted_energy_cost())
print(planner.get_predicted_profit())

file = open('examples/available_solar_example.csv', encoding='utf-8-sig')
csvreader = csv.reader(file)

new_available_solar = []
for row in csvreader:
    new_available_solar.append(float(row[0])/10)

file = open('examples/stroomprijs1-01-18.csv', encoding='utf-8-sig')
csvreader = csv.reader(file)

new_energy_price = []
for row in csvreader:
    new_energy_price.append(float(row[0])/100) #prijs in cent

planner.update(45, new_available_solar, new_energy_price)

print(planner.get_predicted_solar_revenue())
print(planner.get_predicted_energy_cost())
print(planner.get_predicted_profit())


#check validiteit van input data


#optimisation
#N = 24*4 #number of 15-min interval per day
#load_cap = 11/4 #laadpaal capaciteit per kwartier
#revenue = 0
#injection_price = 0.1
#energy_to_sell = available_solar
#for time in range(N):
#    charge_now = int(available_solar[time]/load_cap)
#    cars_charged = 0
#    i = 0
#    while cars_charged < charge_now:
#        while i < len(cars) and (time < sorted_cars[i].get_start() or time >= sorted_cars[i].get_end() or sorted_cars[i].get_charge_kwartier() <= 0):
#            i += 1
#        if i == len(cars):
#            break
#        car = sorted_cars[i]
#        sorted_cars[i].set_charging(time)
#        energy_to_sell[time] -= load_cap
#        cars_charged += 1
#        i += 1
#    revenue += energy_to_sell[time]*injection_price
            



#sorted_id_cars = sorted(sorted_cars, key=lambda x: x.id)
#for car in sorted_id_cars:
#    for time in range(N):
#        if(car.get_charging(time)):
#            print('#',end='')
#        else:
#            print('.',end='')
#    print()

#print('------------------------------------------------------------------------------------------------')

#energy_to_buy = [0]*N
#energy_total_cost = 0

#for car in sorted_cars:
#    if car.get_charge_kwartier() == 0:
#        continue
#    kwartier_prijs = []
#    for time in range(N):
#        if (time < car.get_start() or time >= car.get_end() or car.get_charging(time)):
#            continue
#        kwartier_prijs.append((time, energy_price[time]))
#    kwartier_prijs.sort(key=lambda x: x[1])
#    print(kwartier_prijs)
#    for i in range(car.get_charge_kwartier()):
#        if (car.get_charge_kwartier() > 0):
#            car.set_charging(kwartier_prijs[i][0])
#            energy_to_buy[kwartier_prijs[i][0]] += load_cap
#sorted_id_cars = sorted(sorted_cars, key=lambda x: x.id)
#for time in range(N):
#    energy_total_cost += energy_to_buy[time]*energy_price[time]
#
#for car in sorted_id_cars:
#    for time in range(N):
#        if(car.get_charging(time)):
#            print('#',end='')
#        else:
#            print('.',end='')
#    print()

#print('------------------------------------------------------------------------------------------------')
#for time in range(N):
#    if (energy_to_buy[time] > 0):
#        print('-',end='')
#    elif energy_to_sell[time] > 0:
#        print('+',end='')
#    else:
#        print('0',end='')
#print()
#print(revenue-energy_total_cost)



