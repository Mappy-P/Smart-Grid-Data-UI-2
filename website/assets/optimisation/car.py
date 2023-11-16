class Car:
    
    def __init__(self, id, to_charge, start, end):
        self.N = 24*4
        self.id = id
        self.start = start
        self.end  = end
        self.to_charge = to_charge
        self.to_charge_left = to_charge
        self.charging = [0.]*self.N
    
    def get_id(self):
        return self.id
    def get_start(self):
        return self.start
    def get_end(self):
        return self.end
    def get_to_charge(self):
        return self.to_charge
    def get_to_charge_left(self):
        return self.to_charge_left
    def get_charging(self, i):
        return self.charging[i]
    def set_charging(self, i, amount):
        self.charging[i] += amount
        self.to_charge_left -= amount
    def reset(self, offset):
        for time in range(offset, self.N):
            self.to_charge_left +=  self.get_charging(time)
            self.charging[time] = 0.
