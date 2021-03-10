class Vehicle:
    def __init__(self,license,color):
        self.license = license
        self.color = color

class Car(Vehicle):
    def __init__(self,name,license,color):
        self.name = name
        Vehicle.__init__(self,license,color)
    
    def get(self):
        print(self.name,self.license,self.color)

class Parking:
    def __init__(self,zip):
        self.zip = zip

class Spot(Parking):
    def __init__(self,id,size,zip):
        Parking.__init__(self,zip)
        self.id = id
        self.size = size
        self.car = {}
        self.truck = {}
        self.carCap = 0
        self.truckCap = 0
    
    def placeVehicle(self,vehicle):
        self.vehicle = vehicle
        if self.vehicle.name == "car":
            if len(self.car) < 100:
                self.car[self.vehicle.license] = (self.vehicle.name,self.carCap)
                self.carCap+=1
            elif len(self.truck) < 100:
                self.truck[self.vehicle.license] = (self.vehicle.name,self.truckCap)
                self.truckCap+=1
        elif self.vehicle.name == "truck":
            if len(self.truck)< 100:
                self.truck[self.vehicle.license] = (self.vehicle.name,self.truckCap)
                self.truckCap+=1
    def removeVehicle(self,vehicle):
        self.vehicle = vehicle
        if self.vehicle.license in self.car:
            del self.car[self.vehicle.license]
            self.carCap-=1
        elif self.vehicle.license in self.truck:
            del self.truck[self.vehicle.license]
            self.truckCap-=1
    def get(self,vehicle):
        self.vehicle = vehicle
        if self.vehicle.license in self.car:
            print(self.car[self.vehicle.license])
        elif self.vehicle.license in self.truck:
            print(self.truck[self.vehicle.license])
car1 = Car("car","123","black")
car2 = Car("car","1","black")
truck = Car("truck","1234","grey")
spot = Spot(1,200,123)
spot.placeVehicle(car1)
spot.placeVehicle(car2)
spot.get(car2)
spot.placeVehicle(truck)
spot.get(truck)

