"""
CLASS BLUEPRINT:

1. VehicleType (IntEnum)
   - SMALL = 1
   - MEDIUM = 2
   - LARGE = 3

2. Vehicle (ABC)
   - getType() -> VehicleType
   |-- Bike: getType()
   |-- Car: getType()
   |-- Bus: getType()

3. Spot (ABC)
   - spot_type: VehicleType
   - vehicle: Optional[Vehicle]
   - isAvailable() -> bool
   - occupy(vehicle: Vehicle) -> None
   - vacate() -> None
   |-- SmallSpot
   |-- MediumSpot
   |-- LargeSpot

4. ParkingFeeCalculator
   - RATES: Dict[VehicleType, float]
   - calculate_fee(vehicle_type, entry_time, exit_time) -> float

5. PaymentStrategy (ABC)
   - pay(amount: float) -> bool
   |-- CreditCardPayment: card_number, pay()
   |-- CashPayment: pay()
   |-- UPIPayment: upi_id, pay()

6. ParkingManager
   - available_spots: Dict[VehicleType, List[Spot]]
   - active_parkings: Dict[Vehicle, dict]
   - findSpotForVehicle(vehicle) -> Optional[Spot]
   - allocateSlot(vehicle) -> Optional[Spot]
   - releaseSlot(vehicle, payment_strategy) -> Optional[float]
   - _process_payment(vehicle, amount) -> None

7. ParkingLot (Facade)
   - parkingManager: ParkingManager
   - park_vehicle(vehicle) -> None
   - remove_vehicle(vehicle, payment_strategy) -> None
"""

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
    RATES = {
        VehicleType.SMALL: 5.0,
        VehicleType.MEDIUM: 10.0,
        VehicleType.LARGE: 20.0
    }
    
    @staticmethod
    def calculate_fee(vehicle_type: VehicleType, entry_time: datetime, exit_time: datetime) -> float:
        duration_seconds = (exit_time - entry_time).total_seconds()
        duration_hours = max(1.0, duration_seconds / 3600.0)
        rate = ParkingFeeCalculator.RATES.get(vehicle_type, 10.0)
        return round(duration_hours * rate, 2)

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number
        
    def pay(self, amount: float) -> bool:
        print(f"Charging ${amount:.2f} to Credit Card ending in {self.card_number[-4:]}... Approved!")
        return True

class CashPayment(PaymentStrategy):
    def pay(self, amount: float) -> bool:
        print(f"Accepted cash payment of ${amount:.2f}. Dispensing change...")
        return True

class UPIPayment(PaymentStrategy):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id
        
    def pay(self, amount: float) -> bool:
        print(f"Initiating UPI request to {self.upi_id} for ${amount:.2f}... Success!")
        return True

class ParkingManager:
    def __init__(self, available_spots: Dict[VehicleType, List[Spot]]):
        self.available_spots = available_spots
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
        print(f"Successfully parked {vehicle.__class__.__name__}.")
        return spot

    def releaseSlot(self, vehicle: Vehicle, payment_strategy: PaymentStrategy) -> Optional[float]:
        if vehicle not in self.active_parkings:
            print("Vehicle not found in the parking lot.")
            return None
        
        parking_info = self.active_parkings[vehicle]
        spot = parking_info["spot"]
        entry_time = parking_info["entry_time"]
        exit_time = datetime.now()
        
        fee = ParkingFeeCalculator.calculate_fee(vehicle.getType(), entry_time, exit_time)
        
        success = payment_strategy.pay(fee)
        if not success:
            print("Payment failed. Vehicle cannot exit.")
            return None
        
        spot.vacate()
        del self.active_parkings[vehicle]
        
        print(f"Vehicle {vehicle.__class__.__name__} exited successfully.")
        return fee

class ParkingLot:
    def __init__(self, spots_config: Dict[VehicleType, List[Spot]]):
        self.parkingManager = ParkingManager(spots_config)
    
    def park_vehicle(self, vehicle: Vehicle):
        spot = self.parkingManager.allocateSlot(vehicle)
        if spot:
            print(f"-> {vehicle.__class__.__name__} parked.\n")
        else:
            print("-> No slot available.\n")
    
    def remove_vehicle(self, vehicle: Vehicle, payment_strategy: PaymentStrategy):
        fee = self.parkingManager.releaseSlot(vehicle, payment_strategy)
        if fee is not None:
            print(f"-> Total Paid: ${fee:.2f}\n")


if __name__ == '__main__':
    spots_config = {
        VehicleType.SMALL: [SmallSpot(), SmallSpot()],
        VehicleType.MEDIUM: [MediumSpot(), MediumSpot()],
        VehicleType.LARGE: [LargeSpot()]
    }
    
    parking_lot = ParkingLot(spots_config)
    bike = Bike()
    car1 = Car()
    
    parking_lot.park_vehicle(bike)
    parking_lot.park_vehicle(car1)
    
    cc_payment = CreditCardPayment("1234-5678-9876-5432")
    parking_lot.remove_vehicle(car1, cc_payment)
