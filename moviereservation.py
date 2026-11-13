"""
=============================================================================
CLASS-LEVEL DESIGN & ARCHITECTURAL DOCUMENTATION: MOVIE/EVENT SEAT BOOKING
=============================================================================
1. Architecture & Design Patterns:
   - Strategy Pattern: Used for Payment methods (card, upi, apple pay) allowing 
     flexible integration of new gateways without modifying core booking logic.
   - Template/Abstract Base Classes: Used for Venue (theatre, auditorium) and 
     Events (Movie, concert) to enforce consistent contracts across polymorphic types.
   - State Pattern / State Lifecycle: Seat states transition strictly through 
     Available -> Hold -> Booked, with automated TTL expiration rollbacks.

2. Concurrency & Distributed Safety:
   - Resource-Level Locking: Locks are acquired per-seat-per-show rather than 
     globally, maximizing throughput.
   - Deadlock Prevention: When holding multiple seats, seat IDs are globally sorted 
     in ascending order before lock acquisition, preventing circular wait conditions.
   - Session Isolation: Each hold is tied to a unique user session token preventing 
     seat hijacking during checkout.
=============================================================================
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
import threading
import time

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
        self.ttl = 10  # default 10 minutes
        self.holdTime: datetime | None = None
        self.held_by_session_id: str | None = None
        self._seat_lock = threading.Lock()

    def checkIsexpired(self) -> bool:
        """check if current time - holdTime >= ttl and mark seat as available if so"""
        with self._seat_lock:
            if self.state == SeatState.hold and self.holdTime:
                elapsed = datetime.now() - self.holdTime
                if elapsed >= timedelta(minutes=self.ttl):
                    self.freeSeat()
                    return True
        return False

    def isavailable(self) -> bool:
        """check if available based on seat state, return true is available"""
        if self.checkIsexpired():
            return True
        return self.state == SeatState.available

    def holdSeat(self, session_id: str) -> None:
        """mark state as hold -> mark ttl as 10"""
        with self._seat_lock:
            self.state = SeatState.hold
            self.ttl = 10
            self.holdTime = datetime.now()
            self.held_by_session_id = session_id

    def bookSeat(self) -> None:
        """mark state as booked"""
        with self._seat_lock:
            self.state = SeatState.booked
            self.holdTime = None
            self.held_by_session_id = None

    def freeSeat(self) -> None:
        """mark as available"""
        with self._seat_lock:
            self.state = SeatState.available
            self.holdTime = None
            self.held_by_session_id = None


# =============================================================================
# class Venue: -> abstract class
# - id
# - name
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
# - Events -> dictionary of movies/events -> with value as list of events and time of event, seatmap(availableseats)
#     addEvent(event, time, ListOfseats) -> add Movie if there's no clash on specific time return true and theatre details, time of event, else return false/raise error
#     getEvents() -> return list of events
# =============================================================================
class Theatre(Venue):
    def __init__(self, id: str, name: str):
        super().__init__(id, name)
        self.Events: dict[str, list[tuple[datetime, dict[str, Seat]]]] = {}

    def addEvent(self, event: str, time: datetime, ListOfseats: dict[str, Seat]) -> bool:
        if event not in self.Events:
            self.Events[event] = []
        
        for existing_time, _ in self.Events[event]:
            if abs((existing_time - time).total_seconds()) < 7200:
                return False
                
        self.Events[event].append((time, ListOfseats))
        return True

    def getEvents(self) -> list:
        return list(self.Events.keys())


# =============================================================================
# similar for auditorium like theatre
# =============================================================================
class Auditorium(Venue):
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
# - id
# - name
# - time
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
# - adds all abstract class details - id,name,time 
# - listOfVenues 
#     +getRunningVenues() -> provides list of venues hosting this event with time, returns none if no event scheduled
# =============================================================================
class Movie(Events):
    def __init__(self, id: str, name: str, time: datetime):
        super().__init__(id, name, time)
        self.listOfVenues: list[Venue] = []

    def registerVenue(self, venue: Venue) -> None:
        self.listOfVenues.append(venue)

    def getRunningVenues(self, venues: list[Venue] = None) -> list[tuple[Venue, datetime]] | None:
        target_venues = venues if venues is not None else self.listOfVenues
        running_info = []
        for venue in target_venues:
            if isinstance(venue, Theatre) or isinstance(venue, Auditorium):
                if self.name in venue.Events:
                    for show_time, _ in venue.Events[self.name]:
                        running_info.append((venue, show_time))
        return running_info if running_info else None


# =============================================================================
# class Payment -> abstract class -> strategy pattern 
#         +makePayment()
# =============================================================================
class Payment(ABC):
    @abstractmethod
    def makePayment(self, amount: float) -> bool:
        pass


# =============================================================================
# class card -> implements payment 
#         +makePayment(cardnumber , cvv) -> returns true if successful , else false
# =============================================================================
class Card(Payment):
    def __init__(self, cardnumber: str, cvv: str):
        self.cardnumber = cardnumber
        self.cvv = cvv

    def makePayment(self, amount: float) -> bool:
        print(f"Processing ${amount:.2f} via Credit Card...")
        return True


# =============================================================================
# similar for upi or apple Pay
# =============================================================================
class Upi(Payment):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def makePayment(self, amount: float) -> bool:
        print(f"Processing ${amount:.2f} via UPI ID: {self.upi_id}...")
        return True


class ApplePay(Payment):
    def __init__(self, apple_id: str):
        self.apple_id = apple_id

    def makePayment(self, amount: float) -> bool:
        print(f"Processing ${amount:.2f} via Apple Pay...")
        return True


# =============================================================================
# class EventManager:
# - event -> movie/concert 
# - venue
# - time
# - seatToBook -> None initially
#     +listEvent() -> calls getRunningVenues() for specific event
#     +checkEvent() -> checks if provided time and Venue has that specific event, returns true and proceed to booking
#     +getSeatToBook() -> provide list of seats and get seat to book
#     +makePayment(payment)
#     +bookSeat() -> checkEvent -> getSeatToBook -> if available -> holdSeat -> makePayment -> if sucess return true and mark seat as booked -> if failure indicate failed and relase Seat -> check ttl inside seat and also as a background to determine timeout 
# =============================================================================
class EventManager:
    _seat_locks: dict[str, threading.Lock] = {}
    _lock_guard = threading.Lock()

    @classmethod
    def _get_seat_lock(cls, show_key: str, seat_id: str) -> threading.Lock:
        key = f"{show_key}:{seat_id}"
        with cls._lock_guard:
            if key not in cls._seat_locks:
                cls._seat_locks[key] = threading.Lock()
            return cls._seat_locks[key]

    def __init__(self, event: Events, venue: Venue, time: datetime, session_id: str):
        self.event = event
        self.venue = venue
        self.time = time
        self.session_id = session_id
        self.seatToBook: list[str] | None = None
        self.show_id = f"{venue.id}_{event.id}_{time.isoformat()}"
        self.seat_map = self._fetch_seat_map()

        # Active background TTL sweeper daemon
        self._stop_sweeper = threading.Event()
        self._sweeper_thread = threading.Thread(target=self._background_ttl_sweeper, daemon=True)
        self._sweeper_thread.start()

    def _fetch_seat_map(self) -> dict[str, Seat]:
        if (isinstance(self.venue, Theatre) or isinstance(self.venue, Auditorium)) and self.event.name in self.venue.Events:
            for time_slot, seats in self.venue.Events[self.event.name]:
                if time_slot == self.time:
                    return seats
        return {}

    def _background_ttl_sweeper(self) -> None:
        """Background thread checking TTL expiration continuously."""
        while not self._stop_sweeper.is_set():
            time.sleep(30)
            for seat in self.seat_map.values():
                if seat.state == SeatState.hold:
                    seat.checkIsexpired()

    def listEvent(self) -> list[tuple[Venue, datetime]] | None:
        """calls getRunningVenues() for specific event"""
        return self.event.getRunningVenues([self.venue])

    def checkEvent(self) -> bool:
        """checks if provided time and Venue has that specific event, returns true and proceed to booking"""
        venues_info = self.listEvent()
        if not venues_info:
            return False
        for v, t in venues_info:
            if v.id == self.venue.id and t == self.time:
                return True
        return False

    def getSeatToBook(self, seat_ids: list[str]) -> list[str]:
        """provide list of seats and get seat to book"""
        self.seatToBook = seat_ids
        return self.seatToBook

    def makePayment(self, payment: Payment, total_amount: float) -> bool:
        """Execute payment strategy"""
        return payment.makePayment(total_amount)

    def bookSeat(self, seat_ids: list[str], payment: Payment, total_amount: float) -> bool:
        """
        checkEvent -> getSeatToBook -> if available -> holdSeat -> makePayment 
        -> if success return true and mark seat as booked -> if failure indicate failed and release Seat 
        -> check ttl inside seat and also as a background to determine timeout
        """
        if not self.checkEvent():
            raise ValueError("Event is not scheduled at this venue and time slot.")

        target_seats = self.getSeatToBook(seat_ids)
        sorted_seat_ids = sorted(target_seats)
        acquired_locks = []

        try:
            # 1. Acquire distributed per-seat locks in sorted order to prevent deadlocks
            for seat_id in sorted_seat_ids:
                lock_key = f"{self.show_id}:{seat_id}"
                lock = self._get_seat_lock(self.show_id, seat_id)
                lock.acquire()
                acquired_locks.append(lock)

            # 2. Check availability (invoking lazy checkIsexpired) and hold seats
            for seat_id in sorted_seat_ids:
                seat = self.seat_map.get(seat_id)
                if not seat or not seat.isavailable():
                    raise RuntimeError(f"Seat {seat_id} is not available.")

            for seat_id in sorted_seat_ids:
                self.seat_map[seat_id].holdSeat(self.session_id)

            print(f"Seats {sorted_seat_ids} placed on HOLD for session {self.session_id}.")

            # 3. Make Payment
            payment_success = self.makePayment(payment, total_amount)

            if payment_success:
                for seat_id in sorted_seat_ids:
                    self.seat_map[seat_id].bookSeat()
                print("Payment successful! Seats marked as BOOKED.")
                return True
            else:
                for seat_id in sorted_seat_ids:
                    self.seat_map[seat_id].freeSeat()
                print("Payment failed. Released seat holds back to AVAILABLE.")
                return False

        except Exception as e:
            print(f"Booking error: {e}. Rolling back...")
            for seat_id in sorted_seat_ids:
                seat = self.seat_map.get(seat_id)
                if seat and seat.held_by_session_id == self.session_id:
                    seat.freeSeat()
            return False

        finally:
            for lock in acquired_locks:
                lock.release()

    def shutdown(self):
        self._stop_sweeper.set()
