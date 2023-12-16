from .car import Car

class ChargingPlanner:

    def __init__(self, solar_surplus, energy_price, injection_price, charge_cap):
        self.cars = []
        self.number_of_cars = 0
        self.N = 24*4 #quarters per day
        self.solar_surplus = solar_surplus.copy()
        self.energy_price = energy_price.copy()
        self.injection_price = injection_price
        self.charge_cap = charge_cap
        self.predicted_solar_revenue = 0.
        self.predicted_energy_cost = 0.
        self.energy_to_sell = solar_surplus.copy()
        self.energy_to_buy = [0.]*self.N
        self.EPS = 1E-5
        self.six = 6*4
        self.ten = 22*4+1

    #start_time inclusive end_time exclusive
    def add_car(self, to_charge, start_time, end_time):
        if (end_time-start_time)*self.charge_cap < to_charge:
            raise Exception('Car can never be charged :((')
        self.cars.append(Car(self.number_of_cars, to_charge, start_time, end_time))
        self.number_of_cars += 1
        self.__recompute(start_time)

    #don't change whether loading or not for every point in time before offset (this is in the past)
    def update(self, offset, new_solar_surplus, new_energy_prices):
        for time in range(offset, self.N):
            self.solar_surplus[time] = new_solar_surplus[time]
            self.energy_price[time] = new_energy_prices[time]
        self.__recompute(offset)

    def __recompute(self, offset):
        print(self.solar_surplus)
        for car in self.cars:
            car.reset(offset)

        self.cars.sort(key=lambda car: car.get_to_charge_left()/(car.get_end()-max(car.get_start(), offset)), reverse=True)
        #first loop -- charge with solar surplus
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
                car.set_charging(time, charge_amount)
                self.energy_to_sell[time] -= charge_amount
                i += 1
        self.predicted_solar_revenue = 0.
        for time in range(self.six, self.ten):
            if (self.energy_price[time] >= 0 and self.energy_to_sell[time] > 0.):
                self.predicted_solar_revenue += self.energy_to_sell[time]*min(self.injection_price, self.energy_price[time])
        self.get_scheme()

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
            charging_possible = 0.

            while car.get_to_charge_left() > self.EPS:

                if (i == len(time_price)):
                    raise Exception('ERROR: not able to charge everything even though we should be able to')
                    break
                else:
                    charge_amount = min(car.get_to_charge_left(), self.charge_cap-car.get_charging(time_price[i][0]))
                    car.set_charging(time_price[i][0], charge_amount)
                    self.energy_to_buy[time_price[i][0]] += charge_amount
                    i += 1
        for time in range(self.six, self.ten):
            self.predicted_energy_cost += self.energy_to_buy[time]*self.energy_price[time]
        self.cars.sort(key=lambda x: x.get_id())
        self.get_scheme()

    def get_cars(self):
        return self.cars

    def get_predicted_energy_cost(self):
        return self.predicted_energy_cost

    def get_real_energy_cost(self, real_solar_surplus, real_energy_price):
        real_energy_cost = 0.
        for time in range(self.six, self.ten):
            energy_used = 0.
            for car in self.cars:
                energy_used += car.get_charging(time)
            energy_diff = energy_used - real_solar_surplus[time]
        
            if (energy_diff > 0.):
                real_energy_cost += energy_diff*real_energy_price[time]

        return real_energy_cost

    def get_predicted_solar_revenue(self):
        return self.predicted_solar_revenue

    def get_real_solar_revenue(self, real_solar_surplus, real_energy_price, real_injection_price):
        real_solar_revenue = 0.
        for time in range(self.six, self.ten):
            if (real_energy_price[time] < 0.):
                continue
            energy_used = 0.
            for car in self.cars:
                energy_used += car.get_charging(time)
            energy_diff = energy_used - real_solar_surplus[time]
            if (energy_diff < 0.):
                real_solar_revenue += (-energy_diff)*min(real_injection_price, real_energy_price[time])
        return real_solar_revenue

    def get_predicted_profit(self):
        return self.predicted_solar_revenue-self.predicted_energy_cost

    def get_real_profit(self, real_solar_surplus, real_energy_price, real_injection_price):
        return self.get_real_solar_revenue(real_solar_surplus, real_energy_price, real_injection_price)-self.get_real_energy_cost(real_solar_surplus, real_energy_price)

