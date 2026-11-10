from abc import ABC, abstractmethod
from threading import Lock
from typing import Dict


# --- 1. Domain Entities ---
class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


class Inventory:
    def __init__(self):
        self._stock: Dict[str, int] = {}
        self._products: Dict[str, Product] = {}
        self._lock = Lock()

    def add_product(self, code: str, product: Product, quantity: int):
        with self._lock:
            self._products[code] = product
            self._stock[code] = self._stock.get(code, 0) + quantity

    def get_product(self, code: str) -> Product:
        return self._products.get(code)

    def get_quantity(self, code: str) -> int:
        return self._stock.get(code, 0)

    def deduct(self, code: str):
        with self._lock:
            if self._stock.get(code, 0) > 0:
                self._stock[code] -= 1

    def is_available(self, code: str) -> bool:
        return self.get_quantity(code) > 0


# --- 2. Extensible Payment Subsystem (Strategy Pattern) ---
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass


class CashPayment(PaymentStrategy):
    def __init__(self, inserted_amount: float):
        self.inserted_amount = inserted_amount

    def pay(self, amount: float) -> bool:
        if self.inserted_amount >= amount:
            change = self.inserted_amount - amount
            print(f"[Cash] Payment successful. Collected: ${self.inserted_amount:.2f}. Change returned: ${change:.2f}")
            return True
        else:
            print(f"[Cash] Insufficient cash. Provided: ${self.inserted_amount:.2f}, Required: ${amount:.2f}")
            return False


class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount: float) -> bool:
        print(f"[Credit Card] Processing card ending in {self.card_number[-4:]} for ${amount:.2f}...")
        print("[Credit Card] Authorization approved by bank.")
        return True


class MobileNfcPayment(PaymentStrategy):
    def __init__(self, device_token: str):
        self.device_token = device_token

    def pay(self, amount: float) -> bool:
        print(f"[Mobile NFC] Connecting to secure token device... Charged ${amount:.2f}")
        return True


# --- 3. State Pattern Subsystem ---
class VendingMachineState(ABC):
    @abstractmethod
    def select_product(self, machine, code: str):
        pass

    @abstractmethod
    def make_payment(self, machine, payment_strategy: PaymentStrategy):
        pass

    @abstractmethod
    def dispense(self, machine, code: str):
        pass

    @abstractmethod
    def cancel(self, machine):
        pass


class IdleState(VendingMachineState):
    def select_product(self, machine, code: str):
        product = machine.inventory.get_product(code)
        if not product:
            print("Invalid product code.")
            return
        if not machine.inventory.is_available(code):
            print(f"Product {product.name} is out of stock.")
            return
        
        machine.set_selected_product(code)
        print(f"Selected: {product.name} (${product.price:.2f}). Please provide payment.")
        machine.set_state(machine.get_payment_state())

    def make_payment(self, machine, payment_strategy: PaymentStrategy):
        print("Please select a product first.")

    def dispense(self, machine, code: str):
        print("No transaction in progress.")

    def cancel(self, machine):
        print("Nothing to cancel.")


class PaymentPendingState(VendingMachineState):
    def select_product(self, machine, code: str):
        print("Product already selected. Complete payment or cancel.")

    def make_payment(self, machine, payment_strategy: PaymentStrategy):
        product = machine.inventory.get_product(machine.get_selected_product())
        
        # Execute selected payment strategy
        success = payment_strategy.pay(product.price)
        if success:
            machine.set_state(machine.get_dispensing_state())
            machine.state.dispense(machine, machine.get_selected_product())
        else:
            print("Payment failed. Try another method or cancel.")

    def dispense(self, machine, code: str):
        print("Complete payment before dispensing.")

    def cancel(self, machine):
        print("Transaction cancelled.")
        machine.reset_selection()
        machine.set_state(machine.get_idle_state())


class DispensingState(VendingMachineState):
    def select_product(self, machine, code: str):
        print("Please wait, currently dispensing item.")

    def make_payment(self, machine, payment_strategy: PaymentStrategy):
        print("Please wait, currently dispensing item.")

    def dispense(self, machine, code: str):
        product = machine.inventory.get_product(code)
        machine.inventory.deduct(code)
        print(f"Dispensing item... Enjoy your {product.name}!")
        machine.reset_selection()
        machine.set_state(machine.get_idle_state())

    def cancel(self, machine):
        print("Cannot cancel while dispensing.")


# --- 4. Context Class: VendingMachine ---
class VendingMachine:
    def __init__(self):
        self.inventory = Inventory()
        
        self._idle_state = IdleState()
        self._payment_state = PaymentPendingState()
        self._dispensing_state = DispensingState()
        
        self._current_state = self._idle_state
        self._selected_product_code = None
        self._lock = Lock()

    def set_state(self, state: VendingMachineState):
        self._current_state = state

    def get_idle_state(self): return self._idle_state
    def get_payment_state(self): return self._payment_state
    def get_dispensing_state(self): return self._dispensing_state

    def set_selected_product(self, code: str):
        with self._lock:
            self._selected_product_code = code

    def get_selected_product(self) -> str:
        with self._lock:
            return self._selected_product_code

    def reset_selection(self):
        with self._lock:
            self._selected_product_code = None

    # Public thread-safe transaction endpoints
    def select_product(self, code: str):
        with self._lock:
            self._current_state.select_product(self, code)

    def make_payment(self, payment_strategy: PaymentStrategy):
        with self._lock:
            self._current_state.make_payment(self, payment_strategy)

    def cancel(self):
        with self._lock:
            self._current_state.cancel(self)


# --- 5. Verification Test Run ---
if __name__ == "__main__":
    machine = VendingMachine()

    # Setup inventory
    machine.inventory.add_product("A1", Product("Coke", 1.50), 2)
    machine.inventory.add_product("A2", Product("Chips", 1.00), 1)

    print("--- Test 1: Purchase with Cash ---")
    machine.select_product("A1")
    machine.make_payment(CashPayment(2.00))

    print("\n--- Test 2: Purchase with Credit Card ---")
    machine.select_product("A2")
    machine.make_payment(CreditCardPayment("4111222233334444", "123"))

    print("\n--- Test 3: New Payment Type (Mobile NFC) & Cancellation ---")
    machine.select_product("A1")
    machine.cancel()  # Cancels before payment
