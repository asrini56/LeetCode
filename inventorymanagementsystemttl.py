from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
import threading
import time

# --- Enums ---
class ReservationStatus(Enum):
    ACTIVE = 1
    COMMITTED = 2
    EXPIRED = 3
    RELEASED = 4


# --- 1. Observer Interface for Alerts ---
class AlertListener(ABC):
    @abstractmethod
    def on_low_stock(self, warehouse_id: str, product_id: str, current_stock: int):
        pass

class ConsoleAlertListener(AlertListener):
    def on_low_stock(self, warehouse_id: str, product_id: str, current_stock: int):
        print(f"[ALERT] Warehouse '{warehouse_id}' low stock for Product '{product_id}'. Available: {current_stock}")


# --- 2. Stock Reservation Entity ---
class StockReservation:
    def __init__(self, reservation_id: str, product_id: str, warehouse_id: str, quantity: int, ttl_seconds: int = 300):
        self.reservation_id = reservation_id
        self.product_id = product_id
        self.warehouse_id = warehouse_id
        self.quantity = quantity
        self.expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
        self.status = ReservationStatus.ACTIVE

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at

    def update_status(self, new_status: ReservationStatus):
        self.status = new_status


# --- 3. Warehouse Entity ---
class Warehouse:
    def __init__(self, warehouse_id: str):
        self.warehouse_id = warehouse_id
        self.stock: dict[str, int] = {}          # Physical stock counts
        self.reserved: dict[str, int] = {}       # Stock currently locked in active carts
        self.thresholds: dict[str, int] = {}     # Per-warehouse product thresholds
        self.lock = threading.Lock()

    def set_threshold(self, product_id: str, threshold: int):
        with self.lock:
            self.thresholds[product_id] = threshold

    def add_stock(self, product_id: str, quantity: int):
        with self.lock:
            self.stock[product_id] = self.stock.get(product_id, 0) + quantity

    def remove_stock(self, product_id: str, quantity: int) -> bool:
        """Direct removal (e.g., direct fulfillment without prior cart reservation)"""
        with self.lock:
            available = self.get_available_stock_unlocked(product_id)
            if available < quantity:
                return False
            self.stock[product_id] = self.stock.get(product_id, 0) - quantity
            return True

    def reserve_stock(self, product_id: str, quantity: int) -> bool:
        """Moves units from available to reserved pool during checkout"""
        with self.lock:
            available = self.get_available_stock_unlocked(product_id)
            if available < quantity:
                return False
            self.reserved[product_id] = self.reserved.get(product_id, 0) + quantity
            return True

    def commit_reservation(self, product_id: str, quantity: int):
        """Converts a temporary reservation into a permanent stock reduction"""
        with self.lock:
            self.reserved[product_id] = max(0, self.reserved.get(product_id, 0) - quantity)
            self.stock[product_id] = max(0, self.stock.get(product_id, 0) - quantity)

    def release_reservation_stock(self, product_id: str, quantity: int):
        """Returns expired or cancelled reserved stock back to the available pool"""
        with self.lock:
            self.reserved[product_id] = max(0, self.reserved.get(product_id, 0) - quantity)

    def get_available_stock(self, product_id: str) -> int:
        with self.lock:
            return self.get_available_stock_unlocked(product_id)

    def get_available_stock_unlocked(self, product_id: str) -> int:
        physical = self.stock.get(product_id, 0)
        locked = self.reserved.get(product_id, 0)
        return physical - locked

    def is_below_threshold(self, product_id: str) -> bool:
        with self.lock:
            available = self.get_available_stock_unlocked(product_id)
            threshold = self.thresholds.get(product_id, 0)
            return available <= threshold


# --- 4. Central Inventory Manager ---
class InventoryManager:
    def __init__(self):
        self.warehouses: dict[str, Warehouse] = {}
        self.reservations: dict[str, StockReservation] = {}
        self.alert_listeners: list[AlertListener] = []
        self.global_lock = threading.Lock()

        # Background worker setup for TTL reservation cleanup
        self._running = True
        self._cleanup_thread = threading.Thread(target=self._background_ttl_worker, daemon=True)
        self._cleanup_thread.start()

    def add_warehouse(self, warehouse: Warehouse):
        with self.global_lock:
            self.warehouses[warehouse.warehouse_id] = warehouse

    def register_alert_listener(self, listener: AlertListener):
        with self.global_lock:
            self.alert_listeners.append(listener)

    def receive_shipment(self, warehouse_id: str, product_id: str, quantity: int):
        warehouse = self._get_warehouse_or_raise(warehouse_id)
        warehouse.add_stock(product_id, quantity)

    def create_checkout_reservation(self, reservation_id: str, warehouse_id: str, product_id: str, quantity: int, ttl_seconds: int = 300) -> bool:
        """Step 1 of checkout: Temporarily hold stock for a customer"""
        warehouse = self._get_warehouse_or_raise(warehouse_id)
        
        # Attempt to lock stock in the warehouse
        success = warehouse.reserve_stock(product_id, quantity)
        if not success:
            return False

        with self.global_lock:
            self.reservations[reservation_id] = StockReservation(reservation_id, product_id, warehouse_id, quantity, ttl_seconds)
        return True

    def commit_checkout_reservation(self, reservation_id: str) -> bool:
        """Step 2 of checkout: Payment succeeded, permanently deduct stock"""
        with self.global_lock:
            reservation = self.reservations.get(reservation_id)
            if not reservation or reservation.status != ReservationStatus.ACTIVE:
                return False
            
            if reservation.is_expired():
                reservation.update_status(ReservationStatus.EXPIRED)
                return False

            reservation.update_status(ReservationStatus.COMMITTED)
            warehouse = self.warehouses[reservation.warehouse_id]
            warehouse.commit_reservation(reservation.product_id, reservation.quantity)

            # Check if permanent reduction breached low-stock threshold
            self._check_and_trigger_alerts(warehouse, reservation.product_id)
            return True

    def transfer_stock(self, from_warehouse_id: str, to_warehouse_id: str, product_id: str, quantity: int) -> bool:
        if from_warehouse_id == to_warehouse_id:
            return False

        source = self._get_warehouse_or_raise(from_warehouse_id)
        dest = self._get_warehouse_or_raise(to_warehouse_id)

        # Enforce deadlock-free consistent lock ordering
        first_lock, second_lock = sorted([source, dest], key=lambda w: w.warehouse_id)

        with first_lock.lock:
            with second_lock.lock:
                available_source = source.get_available_stock_unlocked(product_id)
                if available_source < quantity:
                    return False
                source.stock[product_id] -= quantity
                dest.stock[product_id] = dest.stock.get(product_id, 0) + quantity

        self._check_and_trigger_alerts(source, product_id)
        return True

    def find_warehouses_for_fulfillment(self, product_id: str, quantity: int) -> list[str]:
        eligible = []
        with self.global_lock:
            for wh_id, warehouse in self.warehouses.items():
                if warehouse.get_available_stock(product_id) >= quantity:
                    eligible.append(wh_id)
        return eligible

    def _get_warehouse_or_raise(self, warehouse_id: str) -> Warehouse:
        with self.global_lock:
            if warehouse_id not in self.warehouses:
                raise ValueError(f"Warehouse {warehouse_id} not found.")
            return self.warehouses[warehouse_id]

    def _check_and_trigger_alerts(self, warehouse: Warehouse, product_id: str):
        if warehouse.is_below_threshold(product_id):
            current_stock = warehouse.get_available_stock(product_id)
            with self.global_lock:
                for listener in self.alert_listeners:
                    listener.on_low_stock(warehouse.warehouse_id, product_id, current_stock)

    def _background_ttl_worker(self):
        """Background thread that automatically sweeps and releases expired cart reservations"""
        while self._running:
            time.sleep(2)  # Poll every 2 seconds
            with self.global_lock:
                for res_id, reservation in list(self.reservations.items()):
                    if reservation.status == ReservationStatus.ACTIVE and reservation.is_expired():
                        reservation.update_status(ReservationStatus.EXPIRED)
                        warehouse = self.warehouses.get(reservation.warehouse_id)
                        if warehouse:
                            warehouse.release_reservation_stock(reservation.product_id, reservation.quantity)
