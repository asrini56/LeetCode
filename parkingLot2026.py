from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List, Optional, Dict
from datetime import datetime

class VehicleType(IntEnum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3

class Vehicle(ABC):
    @abstractmethod
    def getType(self) -> VehicleType:
        pass

class Bike(Vehicle):
    def getType(self) -> VehicleType:
        return VehicleType.SMALL

class Car(Vehicle):
    def getType(self) -> VehicleType:
        return VehicleType.MEDIUM

class Bus(Vehicle):
    def getType(self) -> VehicleType:
        return VehicleType.LARGE

class Spot(ABC):
    def __init__(self, spot_type: VehicleType):
        self.spot_type = spot_type
        self.vehicle: Optional[Vehicle] = None
    
    @abstractmethod
    def isAvailable(self) -> bool:
        pass
    
    def occupy(self, vehicle: Vehicle) -> None:
        if self.isAvailable():
            self.vehicle = vehicle
        else:
            print("Spot is already occupied.")
    
    def vacate(self) -> None:
        self.vehicle = None

class SmallSpot(Spot):
    def __init__(self):
        super().__init__(VehicleType.SMALL)
    
    def isAvailable(self) -> bool:
        return self.vehicle is None

class MediumSpot(Spot):
    def __init__(self):
        super().__init__(VehicleType.MEDIUM)
    
    def isAvailable(self) -> bool:
        return self.vehicle is None

class LargeSpot(Spot):
    def __init__(self):
        super().__init__(VehicleType.LARGE)
    
    def isAvailable(self) -> bool:
        return self.vehicle is None

class ParkingFeeCalculator:
    # Hourly rates defined by vehicle type
    RATES = {
        VehicleType.SMALL: 5.0,   # $5/hour for bikes
        VehicleType.MEDIUM: 10.0, # $10/hour for cars
        VehicleType.LARGE: 20.0   # $20/hour for buses
    }
    
    @staticmethod
    def calculate_fee(vehicle_type: VehicleType, entry_time: datetime, exit_time: datetime) -> float:
        duration_seconds = (exit_time - entry_time).total_seconds()
        duration_hours = max(1.0, duration_seconds / 3600.0) # Minimum charge of 1 hour
        rate = ParkingFeeCalculator.RATES.get(vehicle_type, 10.0)
        return round(duration_hours * rate, 2)

class ParkingManager:
    def __init__(self, available_spots: Dict[VehicleType, List[Spot]]):
        self.available_spots = available_spots
        # Tracking metadata: maps vehicle -> {"spot": Spot, "entry_time": datetime}
        self.active_parkings: Dict[Vehicle, dict] = {}
    
    def findSpotForVehicle(self, vehicle: Vehicle) -> Optional[Spot]:
        vehicle_type = vehicle.getType()
        
        for spot_type in VehicleType:
            if spot_type >= vehicle_type:
                spots = self.available_spots.get(spot_type, [])
                for spot in spots:
                    if spot.isAvailable():
                        return spot
        return None

    def allocateSlot(self, vehicle: Vehicle) -> Optional[Spot]:
        spot = self.findSpotForVehicle(vehicle)
        if not spot:
            print("No available spot found for this vehicle.")
            return None
        
        spot.occupy(vehicle)
        self.active_parkings[vehicle] = {
            "spot": spot,
            "entry_time": datetime.now()
        }
        print(f"Successfully parked {vehicle.__class__.__name__} at {datetime.now().strftime('%H:%M:%S')}.")
        return spot

    def releaseSlot(self, vehicle: Vehicle) -> Optional[float]:
        if vehicle not in self.active_parkings:
            print("Vehicle not found in the parking lot.")
            return None
        
        parking_info = self.active_parkings[vehicle]
        spot = parking_info["spot"]
        entry_time = parking_info["entry_time"]
        exit_time = datetime.now()
        
        # 1. Calculate Fee
        fee = ParkingFeeCalculator.calculate_fee(vehicle.getType(), entry_time, exit_time)
        
        # 2. Process Payment (Mock implementation)
        self._process_payment(vehicle, fee)
        
        # 3. Vacate Spot and Clean up Records
        spot.vacate()
        del self.active_parkings[vehicle]
        
        print(f"Vehicle {vehicle.__class__.__name__} exited. Spot is now free.")
        return fee

    def _process_payment(self, vehicle: Vehicle, amount: float) -> None:
        print(f"Processing payment of ${amount:.2f} for {vehicle.__class__.__name__}... Payment Successful!")

if __name__ == '__main__':
    parking_slots = {
    VehicleType.SMALL: [SmallSpot()],
    VehicleType.MEDIUM: [MediumSpot()],
    VehicleType.LARGE: [LargeSpot()]}

    # 2. Initialize Parking Manager
    manager = ParkingManager(parking_slots)
    
    # 3. Create vehicles
    car = Car()
    bike = Bike()
    car1 = Car()
    car2 = Car()
    
    # 4. Allocate slots
    manager.allocateSlot(bike)  # Parks in SmallSpot (or upgrades if small is full)
    manager.allocateSlot(car)   # Parks in MediumSpot
    manager.allocateSlot(car1)   # Parks in MediumSpot
    manager.allocateSlot(car2)   # Parks in MediumSpot
