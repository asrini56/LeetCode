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
CLASS BLUEPRINT:

1. TicketState (Enum)
   - Variables: available, hold, booked
   - Methods: None

2. Seat
   - Variables: seat_number, row
   - Methods: __init__()

3. Ticket
   - Variables: ticket_id, seat, state, ttl, holdTime
   - Methods: __init__(), checkIsexpired(), isavailable(), holdSeat(), bookSeat(), freeSeat()

4. Venue (ABC)
   - Variables: id, name
   - Methods: __init__(), getEvents()

5. Theatre (inherits Venue)
   - Variables: Events
   - Methods: __init__(), addEvent(), getEvents()

6. Events (ABC)
   - Variables: id, name, time
   - Methods: __init__(), getRunningVenues()

7. Movie (inherits Events)
   - Variables: listOfVenues
   - Methods: __init__(), getRunningVenues()

8. Payment (ABC)
   - Variables: None
   - Methods: makePayment(amount: float) -> bool
   |-- Card: cardnumber, cvv, __init__(), makePayment()
   |-- Upi: upi_id, __init__(), makePayment()

9. EventManager
   - Variables: _locks, _guard, event, venue, time, ticketToBook, ticket_map
   - Methods: __init__(), _fetch_ticket_map(), listEvent(), checkEvent(), 
              getTicketToBook(), makePayment(), bookTicket()
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
import threading

class TicketState(Enum):
    available = 1
    hold = 2
    booked = 3


class Seat:
    def __init__(self, seat_number: str, row: str):
        self.seat_number = seat_number
        self.row = row


class Ticket:
    def __init__(self, ticket_id: str, seat: Seat):
        self.ticket_id = ticket_id
        self.seat = seat
        self.state = TicketState.available
        self.ttl = 10  # minutes
        self.holdTime: datetime | None = None

    def checkIsexpired(self) -> bool:
        if self.state == TicketState.hold and self.holdTime:
            if datetime.now() - self.holdTime >= timedelta(minutes=self.ttl):
                self.freeSeat()
                return True
        return False

    def isavailable(self) -> bool:
        if self.checkIsexpired():
            return True
        return self.state == TicketState.available

    def holdSeat(self) -> None:
        self.state = TicketState.hold
        self.holdTime = datetime.now()

    def bookSeat(self) -> None:
        self.state = TicketState.booked
        self.holdTime = None

    def freeSeat(self) -> None:
        self.state = TicketState.available
        self.holdTime = None


class Venue(ABC):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    @abstractmethod
    def getEvents(self) -> list:
        pass


class Theatre(Venue):
    def __init__(self, id: str, name: str):
        super().__init__(id, name)
        self.Events: dict[str, list[tuple[datetime, dict[str, Ticket]]]] = {}

    def addEvent(self, event: str, time: datetime, ListOftickets: dict[str, Ticket]) -> bool:
        if event not in self.Events:
            self.Events[event] = []
        self.Events[event].append((time, ListOftickets))
        return True

    def getEvents(self) -> list:
        return list(self.Events.keys())


class Events(ABC):
    def __init__(self, id: str, name: str, time: datetime):
        self.id = id
        self.name = name
        self.time = time

    @abstractmethod
    def getRunningVenues(self, venues: list[Venue]) -> list[tuple[Venue, datetime]]:
        pass


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


class EventManager:
    _locks = {}
    _guard = threading.Lock()

    def __init__(self, event: Events, venue: Venue, time: datetime):
        self.event = event
        self.venue = venue
        self.time = time
        self.ticketToBook: list[str] | None = None
        self.ticket_map = self._fetch_ticket_map()

    def _fetch_ticket_map(self) -> dict[str, Ticket]:
        if isinstance(self.venue, Theatre) and self.event.name in self.venue.Events:
            for show_time, tickets in self.venue.Events[self.event.name]:
                if show_time == self.time:
                    return tickets
        return {}

    def listEvent(self) -> list[tuple[Venue, datetime]]:
        return self.event.getRunningVenues([self.venue])

    def checkEvent(self) -> bool:
        for v, t in self.listEvent():
            if v.id == self.venue.id and t == self.time:
                return True
        return False

    def getTicketToBook(self, ticket_ids: list[str]) -> list[str]:
        self.ticketToBook = ticket_ids
        return self.ticketToBook

    def makePayment(self, payment: Payment, amount: float) -> bool:
        return payment.makePayment(amount)

    def bookTicket(self, ticket_ids: list[str], payment: Payment, amount: float) -> bool:
        if not self.checkEvent():
            raise ValueError("Event not scheduled at this venue/time.")

        target_tickets = self.getTicketToBook(ticket_ids)
        sorted_tickets = sorted(target_tickets)
        locked_items = []

        try:
            for ticket_id in sorted_tickets:
                lock_key = f"{self.venue.id}_{self.event.id}_{self.time}_{ticket_id}"
                with EventManager._guard:
                    if lock_key not in EventManager._locks:
                        EventManager._locks[lock_key] = threading.Lock()
                
                EventManager._locks[lock_key].acquire()
                locked_items.append(lock_key)

            for ticket_id in sorted_tickets:
                ticket = self.ticket_map.get(ticket_id)
                if not ticket or not ticket.isavailable():
                    raise RuntimeError(f"Ticket {ticket_id} is unavailable.")

            for ticket_id in sorted_tickets:
                self.ticket_map[ticket_id].holdSeat()

            print(f"Tickets {sorted_tickets} placed on HOLD.")

            if self.makePayment(payment, amount):
                for ticket_id in sorted_tickets:
                    self.ticket_map[ticket_id].bookSeat()
                print("Payment successful! Tickets BOOKED.")
                return True
            else:
                for ticket_id in sorted_tickets:
                    self.ticket_map[ticket_id].freeSeat()
                print("Payment failed. Released tickets back to available.")
                return False

        except Exception as e:
            print(f"Error during booking: {e}. Rolling back...")
            for ticket_id in sorted_tickets:
                ticket = self.ticket_map.get(ticket_id)
                if ticket and ticket.state == TicketState.hold:
                    ticket.freeSeat()
            return False

        finally:
            for lock_key in locked_items:
                EventManager._locks[lock_key].release()
