from datetime import date, timedelta
from enum import IntEnum
import random
from threading import Lock
from typing import Dict, Optional


class CompartmentSize(IntEnum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class Compartment:
    def __init__(self, compartment_id: str, size: CompartmentSize):
        self.compartment_id = compartment_id
        self.size = size
        self.is_free = True
        self._lock = Lock()

    def occupy(self):
        with self._lock:
            self.is_free = False

    def free(self):
        with self._lock:
            self.is_free = True

    def open_door(self):
        print(f"[Hardware] Opening compartment {self.compartment_id} ({self.size.name})...")


class AccessToken:
    def __init__(self, code: str, expiration: date, compartment: Compartment):
        self.code = code
        self.expiration = expiration
        self.compartment = compartment

    def is_expired(self) -> bool:
        return date.today() > self.expiration


class Locker:
    def __init__(self, compartments: list[Compartment]):
        self.compartments = compartments
        self.access_tokens: Dict[str, AccessToken] = {}
        self._lock = Lock()

    def deposit_package(self, size: CompartmentSize) -> Optional[str]:
        with self._lock:
            compartment_allocated = None
            
            # Best-Fit Allocation Strategy
            for compartment in self.compartments:
                if compartment.is_free and compartment.size >= size:
                    if not compartment_allocated or compartment.size < compartment_allocated.size:
                        compartment_allocated = compartment

            if not compartment_allocated:
                print("No suitable compartment available.")
                return None

            compartment_allocated.occupy()
            compartment_allocated.open_door()

            access_token = self._generate_access_token(compartment_allocated)
            self.access_tokens[access_token.code] = access_token
            
            print(f"Package deposited into compartment {compartment_allocated.compartment_id}.")
            return access_token.code

    def pickup_package(self, code: str) -> bool:
        with self._lock:
            if code not in self.access_tokens:
                print("Invalid access code.")
                return False

            token = self.access_tokens[code]

            if token.is_expired():
                print("Access code has expired. Processing return...")
                self._handle_expired_package(code)
                return False

            compartment = token.compartment
            compartment.open_door()
            compartment.free()

            del self.access_tokens[code]
            print("Package successfully picked up!")
            return True

    def _handle_expired_package(self, code: str):
        token = self.access_tokens.get(code)
        if token:
            compartment = token.compartment
            compartment.open_door()
            compartment.free()
            del self.access_tokens[code]
            print(f"[Courier Sweep] Expired package retrieved from compartment {compartment.compartment_id}.")

    def _generate_access_token(self, compartment: Compartment) -> AccessToken:
        code = f"{random.randint(0, 999999):06d}"
        expiration = date.today() + timedelta(days=7)
        return AccessToken(code, expiration, compartment)
