"""
=============================================================================
ENHANCED PRODUCTION-GRADE DESIGN: MOVIE/EVENT SEAT BOOKING SYSTEM
=============================================================================
Improvements included:
- Active Background Sweeper Thread for proactive TTL expiration cleanup.
- Abstracted Distributed Lock Manager interface simulating Redis locking.
- Clean Service-Oriented separation (`BookingService`, `PaymentService`).
=============================================================================
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
import threading
import time
import uuid

class SeatState(Enum):
    AVAILABLE = 1
    HOLD = 2
    BOOKED = 3


class Seat:
    def __init__(self, seat_id: str):
        self.seat_id = seat_id
        self.state = SeatState.AVAILABLE
        self.ttl_minutes = 10
        self.hold_time: datetime | None = None
        self.held_by_session_id: str | None = None
        self._seat_lock = threading.Lock() # Thread-safe guard for local state mutations

    def check_expired(self) -> bool:
        """Lazy evaluation: checks if hold has exceeded TTL and resets to available."""
        with self._seat_lock:
            if self.state == SeatState.HOLD and self.hold_time:
                if datetime.now() - self.hold_time >= timedelta(minutes=self.ttl_minutes):
                    self.free_seat()
                    return True
        return False

    def is_available(self) -> bool:
        if self.check_expired():
            return True
        return self.state == SeatState.AVAILABLE

    def hold_seat(self, session_id: str) -> None:
        with self._seat_lock:
            self.state = SeatState.HOLD
            self.hold_time = datetime.now()
            self.held_by_session_id = session_id

    def book_seat(self) -> None:
        with self._seat_lock:
            self.state = SeatState.BOOKED
            self.hold_time = None
            self.held_by_session_id = None

    def free_seat(self) -> None:
        with self._seat_lock:
            self.state = SeatState.AVAILABLE
            self.hold_time = None
            self.held_by_session_id = None


class DistributedLockManager:
    """Simulates a Redis Distributed Lock cluster (e.g., Redlock algorithm)."""
    def __init__(self):
        self._locks: dict[str, threading.Lock] = {}
        self._global_guard = threading.Lock()

    def acquire_lock(self, resource_key: str, timeout_sec: float = 5.0) -> bool:
        with self._global_guard:
            if resource_key not in self._locks:
                self._locks[resource_key] = threading.Lock()
        return self._locks[resource_key].acquire(timeout=timeout_sec)

    def release_lock(self, resource_key: str) -> None:
        with self._global_guard:
            if resource_key in self._locks:
                try:
                    self._locks[resource_key].release()
                except RuntimeError:
                    pass # Already released


class Venue(ABC):
    def __init__(self, venue_id: str, name: str):
        self.venue_id = venue_id
        self.name = name

    @abstractmethod
    def get_events(self) -> list:
        pass


class Theatre(Venue):
    def __init__(self, venue_id: str, name: str):
        super().__init__(venue_id, name)
        self.schedule_catalog: dict[str, list[tuple[datetime, dict[str, Seat]]]] = {}

    def get_events(self) -> list:
        return list(self.schedule_catalog.keys())


class PaymentStrategy(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass


class CardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv

    def process_payment(self, amount: float) -> bool:
        print(f"Processing ${amount:.2f} via Credit Card...")
        return True


class BookingService:
    def __init__(self, venue: Venue, show_time: datetime, lock_manager: DistributedLockManager):
        self.venue = venue
        self.show_time = show_time
        self.lock_manager = lock_manager
        self.show_id = f"{venue.venue_id}_{show_time.isoformat()}"
        
        # Start background TTL sweeper daemon
        self._stop_sweeper = threading.Event()
        self._sweeper_thread = threading.Thread(target=self._background_ttl_sweeper, daemon=True)
        self._sweeper_thread.start()

    def _background_ttl_sweeper(self) -> None:
        """Active background sweeper worker to proactively release expired holds."""
        while not self._stop_sweeper.is_set():
            time.sleep(30) # Run check every 30 seconds
            if isinstance(self.venue, Theatre):
                for _, seats in self.venue.schedule_catalog.values():
                    for seat in seats.values():
                        if seat.state == SeatState.HOLD:
                            seat.check_expired()

    def process_booking(self, seat_ids: list[str], session_id: str, payment: PaymentStrategy, total_amount: float) -> bool:
        # Deadlock prevention: globally sort seat IDs
        sorted_seat_ids = sorted(seatids := seat_ids)
        acquired_keys = []

        try:
            # 1. Acquire distributed locks per seat
            for seat_id in sorted_seat_ids:
                lock_key = f"lock:{self.show_id}:{seat_id}"
                if not self.lock_manager.acquire_lock(lock_key, timeout_sec=3.0):
                    raise TimeoutError(f"Could not acquire lock for seat {seat_id}")
                acquired_keys.append(lock_key)

            # 2. Validate availability and apply hold
            seat_map = {}
            if isinstance(self.venue, Theatre):
                for _, seats in self.venue.schedule_catalog.values():
                    seat_map = seats
                    break

            for seat_id in sorted_seat_ids:
                seat = seat_map.get(seat_id)
                if not seat or not seat.is_available():
                    raise RuntimeError(f"Seat {seat_id} is unavailable.")

            for seat_id in sorted_seat_ids:
                seat_map[seat_id].hold_seat(session_id)

            print(f"Seats {sorted_seat_ids} successfully held for session {session_id}.")

            # 3. Execute Payment Strategy
            if payment.process_payment(total_amount):
                for seat_id in sorted_seat_ids:
                    seat_map[seat_id].book_seat()
                print("Payment successful! Booking confirmed.")
                return True
            else:
                for seat_id in sorted_seat_ids:
                    seat_map[seat_id].free_seat()
                print("Payment failed. Released seats.")
                return False

        except Exception as e:
            print(f"Booking failed: {e}. Rolling back...")
            return False

        finally:
            # Release all distributed locks
            for lock_key in acquired_keys:
                self.lock_manager.release_lock(lock_key)

    def shutdown(self):
        self._stop_sweeper.set()
