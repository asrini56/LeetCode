"""
CLASS BLUEPRINT:

1. BookStatus (Enum)
   - Variables: AVAILABLE, LOANED, LOST, RESERVED
   - Methods: None

2. Book (Metadata)
   - Variables: isbn, title, authors, publisher
   - Methods: __init__()

3. BookItem (Physical Copy)
   - Variables: barcode, book, rack_location, status, lock
   - Methods: __init__(), update_status(), is_available()

4. FineStrategy (ABC)
   - Variables: None
   - Methods: calculate_fine(days_overdue: int) -> float
   |-- StandardFineStrategy: calculate_fine()
   |-- HeavyFineStrategy: calculate_fine()

5. NotificationObserver (ABC)
   - Variables: None
   - Methods: update(member_id: str, message: str)

6. Member (implements NotificationObserver)
   - Variables: member_id, name, borrowed_items, fine_balance, lock
   - Methods: __init__(), update(), add_fine(), pay_fine()

7. LibraryManager (Facade & Orchestrator)
   - Variables: catalog, inventory, members, active_loans, waitlists, fine_strategy, lock
   - Methods: __init__(), add_book(), add_book_item(), register_member(), 
              search_books(), checkout_book(), return_book()
"""

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
import threading
from typing import List, Dict, Optional, Set

# --- 1. Enums & Metadata ---
class BookStatus(Enum):
    AVAILABLE = 1
    LOANED = 2
    LOST = 3
    RESERVED = 4


class Book:
    def __init__(self, isbn: str, title: str, authors: List[str], publisher: str):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.publisher = publisher


class BookItem:
    def __init__(self, barcode: str, book: Book, rack_location: str):
        self.barcode = barcode
        self.book = book
        self.rack_location = rack_location
        self.status = BookStatus.AVAILABLE
        self.lock = threading.Lock()

    def update_status(self, status: BookStatus):
        with self.lock:
            self.status = status

    def is_available(self) -> bool:
        with self.lock:
            return self.status == BookStatus.AVAILABLE


# --- 2. Strategy Pattern: Fine Calculation ---
class FineStrategy(ABC):
    @abstractmethod
    def calculate_fine(self, days_overdue: int) -> float:
        pass


class StandardFineStrategy(FineStrategy):
    def calculate_fine(self, days_overdue: int) -> float:
        rate_per_day = 0.50
        return round(days_overdue * rate_per_day, 2)


class HeavyFineStrategy(FineStrategy):
    def calculate_fine(self, days_overdue: int) -> float:
        rate_per_day = 1.50
        return round(days_overdue * rate_per_day, 2)


# --- 3. Observer Pattern: Waitlist Notifications ---
class NotificationObserver(ABC):
    @abstractmethod
    def update(self, message: str):
        pass


class Member(NotificationObserver):
    def __init__(self, member_id: str, name: str):
        self.member_id = member_id
        self.name = name
        self.borrowed_items: Set[str] = {}  # barcode -> due_date
        self.fine_balance = 0.0
        self.lock = threading.Lock()

    def update(self, message: str):
        print(f"[NOTIFICATION to {self.name} ({self.member_id})]: {message}")

    def add_fine(self, amount: float):
        with self.lock:
            self.fine_balance += amount

    def pay_fine(self, amount: float):
        with self.lock:
            self.fine_balance = max(0.0, self.fine_balance - amount)


# --- 4. Central Library Manager (Facade & Orchestrator) ---
class LibraryManager:
    def __init__(self, fine_strategy: FineStrategy):
        self.catalog: Dict[str, Book] = {}
