"""
=============================================================================
INTERVIEW-READY SIMPLIFIED LLD: MOVIE/EVENT SEAT BOOKING SYSTEM (~45 MIN)
=============================================================================
Key Interview Checkpoints Covered:
1. Strategy Pattern: Payment processing (Card, UPI).
2. State Management: Seat transitions (Available -> Hold -> Booked) with TTL.
3. Concurrency & Safety: Per-seat lock coordination and deadlock prevention (sorting).
4. Orchestration: EventManager tying validation, holding, and payment together.
=============================================================================
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
import threading

class SeatState(Enum):
    available = 1
    hold = 2
    booked = 3


# =============================================================================
# class Seat:
# - state: SeatState
# - ttl -> 0
# - holdTime -> time
#     +isavailable() -> check if available based on seat state, return true is available
#     +bookSeat() -> mark state as booked
#     +holdSeat() -> mark state as hold -> mark ttl as 10
#     +freeSeat() -> mark as available
#     +checkIsexpired() -> check if current time - holdTime >= ttl and mark seat as available if so
# =============================================================================
class Seat:
    def __init__(self, seat_id: str):
        self.seat_id = seat_id
        self.state = SeatState.available
        self.ttl = 10  # minutes
        self.holdTime: datetime | None = None

    def checkIsexpired(self) -> bool:
        if self.state == SeatState.hold and self.holdTime:
            if datetime.now() - self.holdTime >= timedelta(minutes=self.ttl):
                self.freeSeat()
                return True
        return False

    def isavailable(self) -> bool:
        if self.checkIsexpired():
            return True
        return self.state == SeatState.available

    def holdSeat(self) -> None:
        self.state = SeatState.hold
        self.holdTime = datetime.now()

    def bookSeat(self) -> None:
        self.state = SeatState.booked
        self.holdTime = None

    def freeSeat(self) -> None:
        self.state = SeatState.available
        self.holdTime = None


# =============================================================================
# class Venue: -> abstract class
# - id, name
#     +getEvents() -> list the events in this venue
# =============================================================================
class Venue(ABC):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @abstractmethod
    def getEvents(self) -> list:
        pass


# =============================================================================
# class theatre -> implements venue
# - Events -> dictionary of events with time and seatmaps
#     addEvent() -> add event if no clash
#     getEvents() -> return list of events
# =============================================================================
class Theatre(Venue):
    def __init__(self, id: str, name: str):
        super().__init__(id, name)
        self.Events: dict[str, list[tuple[datetime, dict[str, Seat]]]] = {}

    def addEvent(self, event: str, time: datetime, ListOfseats: dict[str, Seat]) -> bool:
        if event not in self.Events:
            self.Events[event] = []
        self.Events[event].append((time, ListOfseats))
        return True

    def getEvents(self) -> list:
        return list(self.Events.keys())


# =============================================================================
# class Events -> abstract class
# - id, name, time
#     +getRunningVenues()
# =============================================================================
class Events(ABC):
    def __init__(self, id: str, name: str, time: datetime):
        self.id = id
        self.name = name
        self.time = time

    @abstractmethod
    def getRunningVenues(self, venues: list[Venue]) -> list[tuple[Venue, datetime]]:
        pass


# =============================================================================
# class Movie -> implements Events
#     +getRunningVenues() -> provides list of venues hosting this event with time
# =============================================================================
class Movie(Events):
    def __init__(self, id: str, name: str, time: datetime):
        super().__init__(id, name, time)
        self.listOfVenues: list[Venue] = []

    def getRunningVenues(self, venues: list[Venue]) -> list[tuple[Venue, datetime]]:
        running_info = []
        for venue in venues:
            if isinstance(venue, Theatre) and self.name in venue.Events:
                for show_time, _ in venue.Events[self.name]:
                    running_info.append((venue, show_time))
        return running_info if running_info else []


# =============================================================================
# class Payment -> abstract class -> strategy pattern 
#         +makePayment()
# =============================================================================
class Payment(ABC):
    @abstractmethod
    def makePayment(self, amount: float) -> bool:
        pass


class Card(Payment):
    def __init__(self, cardnumber: str, cvv: str):
        self.cardnumber = cardnumber
        self.cvv = cvv

    def makePayment(self, amount: float) -> bool:
        print(f"Processing ${amount:.2f} via Card ending in {self.cardnumber[-4:]}...")
        return True


class Upi(Payment):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def makePayment(self, amount: float) -> bool:
        print(f"Processing ${amount:.2f} via UPI: {self.upi_id}...")
        return True


# =============================================================================
# class EventManager:
# - event, venue, time, seatToBook
#     +listEvent(), +checkEvent(), +getSeatToBook(), +makePayment(), +bookSeat()
# =============================================================================
class EventManager:
    # Simple class-level lock mapping to simulate per-seat distributed locks
    _locks = {}
    _guard = threading.Lock()

    def __init__(self, event: Events, venue: Venue, time: datetime):
        self.event = event
        self.venue = venue
        self.time = time
        self.seatToBook: list[str] | None = None
        self.seat_map = self._fetch_seat_map()

    def _fetch_seat_map(self) -> dict[str, Seat]:
        if isinstance(self.venue, Theatre) and self.event.name in self.venue.Events:
            for show_time, seats in self.venue.Events[self.event.name]:
                if show_time == self.time:
                    return seats
        return {}

    def listEvent(self) -> list[tuple[Venue, datetime]]:
        return self.event.getRunningVenues([self.venue])

    def checkEvent(self) -> bool:
        for v, t in self.listEvent():
            if v.id == self.venue.id and t == self.time:
                return True
        return False

    def getSeatToBook(self, seat_ids: list[str]) -> list[str]:
        self.seatToBook = seat_ids
        return self.seatToBook

    def makePayment(self, payment: Payment, amount: float) -> bool:
        return payment.makePayment(amount)

    def bookSeat(self, seat_ids: list[str], payment: Payment, amount: float) -> bool:
        if not self.checkEvent():
            raise ValueError("Event not scheduled at this venue/time.")

        target_seats = self.getSeatToBook(seat_ids)
        # Deadlock Prevention: Sort seat IDs alphabetically/numerically
        sorted_seats = sorted(target_seats)
        locked_items = []

        try:
            # 1. Acquire locks per seat
            for seat_id in sorted_seats:
                lock_key = f"{self.venue.id}_{self.event.id}_{self.time}_{seat_id}"
                with EventManager._guard:
                    if lock_key not in EventManager._locks:
                        EventManager._locks[lock_key] = threading.Lock()
                
                EventManager._locks[lock_key].acquire()
                locked_items.append(lock_key)

            # 2. Check availability & hold
            for seat_id in sorted_seats:
                seat = self.seat_map.get(seat_id)
                if not seat or not seat.isavailable():
                    raise RuntimeError(f"Seat {seat_id} is unavailable.")

            for seat_id in sorted_seats:
                self.seat_map[seat_id].holdSeat()

            print(f"Seats {sorted_seats} placed on HOLD.")

            # 3. Process Payment
            if self.makePayment(payment, amount):
                for seat_id in sorted_seats:
                    self.seat_map[seat_id].bookSeat()
                print("Payment successful! Seats BOOKED.")
                return True
            else:
                for seat_id in sorted_seats:
                    self.seat_map[seat_id].freeSeat()
                print("Payment failed. Released seats back to available.")
                return False

        except Exception as e:
            print(f"Error during booking: {e}. Rolling back...")
            for seat_id in sorted_seats:
                seat = self.seat_map.get(seat_id)
                if seat and seat.state == SeatState.hold:
                    seat.freeSeat()
            return False

        finally:
            # Release locks
            for lock_key in locked_items:
                EventManager._locks[lock_key].release()
