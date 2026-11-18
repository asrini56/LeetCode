"""
CLASS BLUEPRINT:

1. TableStatus (Enum)
   - Variables: AVAILABLE, OCCUPIED
   - Methods: None

2. OrderStatus (Enum)
   - Variables: PLACED, PREPARING, READY, COMPLETED
   - Methods: None

3. MenuItem
   - Variables: item_id, name, price
   - Methods: __init__()

4. Table
   - Variables: table_id, capacity, status, lock
   - Methods: __init__(), occupy(), release()

5. Order
   - Variables: order_id, table_id, items, status, total_amount, lock
   - Methods: __init__(), update_status()

6. RestaurantManager
   - Variables: tables, menu, orders, lock
   - Methods: __init__(), add_table(), add_menu_item(), assign_table(), 
              place_order(), update_order_status(), checkout_and_free_table()
"""

from enum import Enum
import threading
from typing import List, Dict, Optional

class TableStatus(Enum):
    AVAILABLE = 1
    OCCUPIED = 2

class OrderStatus(Enum):
    PLACED = 1
    PREPARING = 2
    READY = 3
    COMPLETED = 4

class MenuItem:
    def __init__(self, item_id: str, name: str, price: float):
        self.item_id = item_id
        self.name = name
        self.price = price

class Table:
    def __init__(self, table_id: int, capacity: int):
        self.table_id = table_id
        self.capacity = capacity
        self.status = TableStatus.AVAILABLE
        self.lock = threading.Lock()

    def occupy(self) -> bool:
        """Thread-safe table occupation check-and-set"""
        with self.lock:
            if self.status == TableStatus.AVAILABLE:
                self.status = TableStatus.OCCUPIED
                return True
            return False

    def release(self):
        with self.lock:
            self.status = TableStatus.AVAILABLE

class Order:
    def __init__(self, order_id: str, table_id: int, items: List[MenuItem]):
        self.order_id = order_id
        self.table_id = table_id
        self.items = items
        self.status = OrderStatus.PLACED
        self.total_amount = sum(item.price for item in items)
        self.lock = threading.Lock()

    def update_status(self, new_status: OrderStatus):
        with self.lock:
            self.status = new_status

class RestaurantManager:
    def __init__(self):
        self.tables: Dict[int, Table] = {}
        self.menu: Dict[str, MenuItem] = {}
        self.orders: Dict[str, Order] = {}
        self.lock = threading.Lock()

    def add_table(self, table: Table):
        with self.lock:
            self.tables[table.table_id] = table

    def add_menu_item(self, item: MenuItem):
        with self.lock:
            self.menu[item.item_id] = item

    def assign_table(self, party_size: int) -> Optional[int]:
        """Finds and atomically reserves an available table matching the party size."""
        for table_id, table in self.tables.items():
            if table.capacity >= party_size and table.occupy():
                return table_id
        return None  # No suitable table available

    def place_order(self, order_id: str, table_id: int, item_ids: List[str]) -> Optional[Order]:
        table = self.tables.get(table_id)
        if not table or table.status != TableStatus.OCCUPIED:
            return None  # Cannot order for an unassigned table

        valid_items = []
        with self.lock:
            for item_id in item_ids:
                item = self.menu.get(item_id)
                if item:
                    valid_items.append(item)

        if not valid_items:
            return None

        order = Order(order_id, table_id, valid_items)
        with self.lock:
            self.orders[order_id] = order
        return order

    def update_order_status(self, order_id: str, new_status: OrderStatus) -> bool:
        order = self.orders.get(order_id)
        if not order:
            return False
        order.update_status(new_status)
        return True

    def checkout_and_free_table(self, table_id: int, order_id: str) -> Optional[float]:
        """Completes the order, processes total payment, and frees the physical table."""
        order = self.orders.get(order_id)
        if not order or order.table_id != table_id:
            return None

        order.update_status(OrderStatus.COMPLETED)
        
        table = self.tables.get(table_id)
        if table:
            table.release()

        with self.lock:
            del self.orders[order_id]

        return order.total_amount
