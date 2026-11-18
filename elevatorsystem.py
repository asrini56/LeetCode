"""
CLASS BLUEPRINT:

1. Direction (Enum)
   - Variables: UP, DOWN, IDLE
   - Methods: None

2. RequestType (Enum)
   - Variables: PICKUP_UP, PICKUP_DOWN, DESTINATION
   - Methods: None

3. Request
   - Variables: floor, type
   - Methods: __init__(), get_floor(), get_type(), __eq__(), __hash__()

4. Elevator
   - Variables: car_id, current_floor, direction, requests, min_floor, max_floor
   - Methods: __init__(), get_current_floor(), get_direction(), add_request(), 
              step(), has_requests_ahead(), has_requests_at_or_beyond()

5. ElevatorController
   - Variables: min_floor, max_floor, elevators
   - Methods: __init__(), request_elevator(), step(), select_best_elevator(), 
              find_committed_to_floor(), find_nearest_idle(), find_nearest()
"""

from enum import Enum

class Direction(Enum):
    UP = 1
    DOWN = 2
    IDLE = 3

class RequestType(Enum):
    PICKUP_UP = 1
    PICKUP_DOWN = 2
    DESTINATION = 3

class Request:
    def __init__(self, floor: int, type: RequestType):
        self.floor = floor
        self.type = type

    def get_floor(self) -> int:
        return self.floor

    def get_type(self) -> RequestType:
        return self.type

    def __eq__(self, other):
        if not isinstance(other, Request):
            return False
        return self.floor == other.floor and self.type == other.type

    def __hash__(self):
        return hash((self.floor, self.type))

class Elevator:
    def __init__(self, car_id: int, min_floor: int = 0, max_floor: int = 9):
        self.car_id = car_id
        self.current_floor = 0
        self.direction = Direction.IDLE
        self.requests = set()
        self.min_floor = min_floor
        self.max_floor = max_floor

    def get_current_floor(self) -> int:
        return self.current_floor

    def get_direction(self) -> Direction:
        return self.direction

    def add_request(self, request: Request) -> bool:
        if not (self.min_floor <= request.get_floor() <= self.max_floor):
            return False
        if request.get_floor() == self.current_floor:
            return True  # Already here
        if request in self.requests:
            return False  # Duplicate request
        
        self.requests.add(request)
        return True

    def step(self):
        """Simulates one time-tick of movement and state processing (LOOK/SCAN algorithm)."""
        if not self.requests:
            self.direction = Direction.IDLE
            return

        # If IDLE, determine initial direction based on the nearest request
        if self.direction == Direction.IDLE:
            nearest = None
            min_distance = float('inf')
            
            for req in self.requests:
                distance = abs(req.get_floor() - self.current_floor)
                if distance < min_distance or (distance == min_distance and (nearest is None or req.get_floor() < nearest.get_floor())):
                    min_distance = distance
                    nearest = req
            
            self.direction = Direction.UP if nearest.get_floor() > self.current_floor else Direction.DOWN

        # Check if we need to service any requests at the current floor
        pickup_type = RequestType.PICKUP_UP if self.direction == Direction.UP else RequestType.PICKUP_DOWN
        pickup_request = Request(self.current_floor, pickup_type)
        destination_request = Request(self.current_floor, RequestType.DESTINATION)

        if pickup_request in self.requests or destination_request in self.requests:
            self.requests.discard(pickup_request)
            self.requests.discard(destination_request)
            if not self.requests:
                self.direction = Direction.IDLE
            return

        # If no requests ahead in current direction, reverse direction
        if not self.has_requests_ahead(self.direction):
            self.direction = Direction.DOWN if self.direction == Direction.UP else Direction.UP
            return

        # Move one floor in the current direction
        if self.direction == Direction.UP:
            self.current_floor += 1
        elif self.direction == Direction.DOWN:
            self.current_floor -= 1

    def has_requests_ahead(self, dir: Direction) -> bool:
        for request in self.requests:
            if dir == Direction.UP and request.get_floor() > self.current_floor:
                return True
            if dir == Direction.DOWN and request.get_floor() < self.current_floor:
                return True
        return False

    def has_requests_at_or_beyond(self, floor: int, dir: Direction) -> bool:
        for request in self.requests:
            if dir == Direction.UP and request.get_floor() >= floor:
                if request.get_type() in (RequestType.PICKUP_UP, RequestType.DESTINATION):
                    return True
            if dir == Direction.DOWN and request.get_floor() <= floor:
                if request.get_type() in (RequestType.PICKUP_DOWN, RequestType.DESTINATION):
                    return True
        return False

class ElevatorController:
    def __init__(self, num_elevators: int = 3, min_floor: int = 0, max_floor: int = 9):
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.elevators = [Elevator(car_id=i, min_floor=min_floor, max_floor=max_floor) for i in range(num_elevators)]

    def request_elevator(self, floor: int, request_type: RequestType) -> bool:
        if not (self.min_floor <= floor <= self.max_floor):
            return False
        if request_type == RequestType.DESTINATION:
            return False  # Destination requests must be sent directly to a specific car

        request = Request(floor, request_type)
        best_elevator = self.select_best_elevator(request)
        
        if best_elevator is None:
            return False

        return best_elevator.add_request(request)

    def step(self):
        """Advances the simulation tick for all elevator cars."""
        for elevator in self.elevators:
            elevator.step()

    def select_best_elevator(self, request: Request) -> Elevator:
        # Priority 1: Find an elevator already committed and moving towards this floor in the right direction
        best = self.find_committed_to_floor(request)
        if best is not None:
            return best

        # Priority 2: Find the nearest IDLE elevator
        best = self.find_nearest_idle(request.get_floor())
        if best is not None:
            return best

        # Priority 3: Fallback to the nearest elevator overall
        return self.find_nearest(request.get_floor())

    def find_committed_to_floor(self, request: Request) -> Elevator:
        floor = request.get_floor()
        direction = Direction.UP if request.get_type() == RequestType.PICKUP_UP else Direction.DOWN

        best = None
        min_distance = float('inf')

        for elevator in self.elevators:
            if elevator.get_direction() != direction:
                continue
            
            current_floor = elevator.get_current_floor()
            
            # Position check: elevator must not have already passed the floor
            if (direction == Direction.UP and current_floor > floor) or \
               (direction == Direction.DOWN and current_floor < floor):
                continue
            
            # Horizon check: elevator must guarantee service past this floor
            if not elevator.has_requests_at_or_beyond(floor, direction):
                continue
            
            distance = abs(current_floor - floor)
            if distance < min_distance:
                min_distance = distance
                best = elevator

        return best

    def find_nearest_idle(self, floor: int) -> Elevator:
        nearest = None
        min_distance = float('inf')

        for elevator in self.elevators:
            if elevator.get_direction() != Direction.IDLE:
                continue

            distance = abs(elevator.get_current_floor() - floor)
            if distance < min_distance:
                min_distance = distance
                nearest = elevator

        return nearest

    def find_nearest(self, floor: int) -> Elevator:
        nearest = self.elevators[0]
        min_distance = abs(self.elevators[0].get_current_floor() - floor)

        for elevator in self.elevators:
            distance = abs(elevator.get_current_floor() - floor)
            if distance < min_distance:
                min_distance = distance
                nearest = elevator

        return nearest
