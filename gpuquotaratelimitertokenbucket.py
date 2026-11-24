
import time
import threading

class GPUTokenBucket:
    def __init__(self, quota, refill_rate):
        self.capacity = quota
        self.tokens = quota
        self.refill_rate = refill_rate  # GPU-hours per second

        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        self.reservations = {}

    def refill(self):
        now = time.monotonic()

        elapsed = now - self.last_refill

        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate
        )

        self.last_refill = now

    def allocate(self, vm_id, gpu_count, hours):
        cost = gpu_count * hours

        with self.lock:
            self.refill()

            if vm_id in self.reservations:
                return False

            if self.tokens < cost:
                return False

            self.tokens -= cost
            self.reservations[vm_id] = (
                gpu_count, hours
            )

            return True

    def extend(self, vm_id, additional_hours):
        with self.lock:
            self.refill()

            if vm_id not in self.reservations:
                return False

            gpu_count, reserved_hours = self.reservations[vm_id]

            cost = gpu_count * additional_hours

            if self.tokens < cost:
                return False

            self.tokens -= cost

            self.reservations[vm_id] = (
                gpu_count,
                reserved_hours + additional_hours
            )

            return True

    def release(self, vm_id, actual_hours):
        with self.lock:
            if vm_id not in self.reservations:
                return False

            gpu_count, reserved_hours = self.reservations.pop(vm_id)

            reserved = gpu_count * reserved_hours
            actual = gpu_count * actual_hours

            if actual > reserved:
                self.reservations[vm_id] = (
                    gpu_count, reserved_hours
                )
                return False

            self.tokens = min(
                self.capacity,
                self.tokens + reserved - actual
            )

            return True

# Capacity = 100 GPU-hours
# Refill = 10 GPU-hours per day

bucket = GPUTokenBucket(
    quota=100,
    refill_rate=10 / 86400
)

# Reserve 40 GPU-hours
bucket.allocate("vm1", 4, 10)

# Remaining = 60

# After one day, approximately 10 tokens refill.

# Remaining = 70

# Release VM after using only 8 hours.
bucket.release("vm1", 8)

# Refund unused 8 GPU-hours.
# Remaining = 102, capped at 100.
