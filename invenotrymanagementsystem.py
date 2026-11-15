from abc import ABC, abstractmethod
import threading

# --- 1. Observer Interface for Pluggable Alerts ---
class AlertListener(ABC):
    @abstractmethod
    def on_low_stock(self, warehouse_id: str, product_id: str, current_stock: int):
        pass

class ConsoleAlertListener(AlertListener):
    def on_low_stock(self, warehouse_id: str, product_id: str, current_stock: int):
        print(f"[ALERT] Warehouse '{warehouse_id}' low stock for Product '{product_id}'. Remaining: {current_stock}")


# --- 2. Warehouse Entity ---
class Warehouse:
    def __init__(self, warehouse_id: str):
        self.warehouse_id = warehouse_id
        self.stock: dict[str, int] = {}          # ProductId -> Quantity
        self.thresholds: dict[str, int] = {}     # ProductId -> Warehouse-specific threshold
        self.lock = threading.Lock()

    def set_threshold(self, product_id: str, threshold: int):
        with self.lock:
            self.thresholds[product_id] = threshold

    def add_stock(self, product_id: str, quantity: int):
        with self.lock:
            self.stock[product_id] = self.stock.get(product_id, 0) + quantity

    def remove_stock(self, product_id: str, quantity: int) -> bool:
        """Enforces invariant: rejects operations resulting in negative inventory"""
        with self.lock:
            current = self.stock.get(product_id, 0)
            if current < quantity:
                return False
            self.stock[product_id] = current - quantity
            return True

    def get_available_stock(self, product_id: str) -> int:
        with self.lock:
            return self.stock.get(product_id, 0)

    def is_below_threshold(self, product_id: str) -> bool:
        with self.lock:
            current = self.stock.get(product_id, 0)
            threshold = self.thresholds.get(product_id, 0)
            return current <= threshold


# --- 3. Central Inventory Manager ---
class InventoryManager:
    def __init__(self):
        self.warehouses: dict[str, Warehouse] = {}
        self.alert_listeners: list[AlertListener] = []
        self.global_lock = threading.Lock()

    def add_warehouse(self, warehouse: Warehouse):
        with self.global_lock:
            self.warehouses[warehouse.warehouse_id] = warehouse

    def register_alert_listener(self, listener: AlertListener):
        with self.global_lock:
            self.alert_listeners.append(listener)

    def receive_shipment(self, warehouse_id: str, product_id: str, quantity: int):
        warehouse = self._get_warehouse_or_raise(warehouse_id)
        warehouse.add_stock(product_id, quantity)

    def fulfill_order(self, warehouse_id: str, product_id: str, quantity: int) -> bool:
        warehouse = self._get_warehouse_or_raise(warehouse_id)
        
        success = warehouse.remove_stock(product_id, quantity)
        if not success:
            return False

        self._check_and_trigger_alerts(warehouse, product_id)
        return True

    def transfer_stock(self, from_warehouse_id: str, to_warehouse_id: str, product_id: str, quantity: int) -> bool:
        if from_warehouse_id == to_warehouse_id:
            return False

        source = self._get_warehouse_or_raise(from_warehouse_id)
        dest = self._get_warehouse_or_raise(to_warehouse_id)

        # Senior Touch: Sort locks alphabetically by ID to prevent deadlocks during concurrent transfers
        first_lock, second_lock = sorted([source, dest], key=lambda w: w.warehouse_id)

        with first_lock.lock:
            with second_lock.lock:
                current_source_stock = source.stock.get(product_id, 0)
                if current_source_stock < quantity:
                    return False
                source.stock[product_id] = current_source_stock - quantity
                dest.stock[product_id] = dest.stock.get(product_id, 0) + quantity

        self._check_and_trigger_alerts(source, product_id)
        return True

    def find_warehouses_for_fulfillment(self, product_id: str, quantity: int) -> list[str]:
        """Returns a list of warehouse IDs capable of fulfilling the requested quantity"""
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
