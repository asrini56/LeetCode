import time
import threading


class GPUTokenBucket:
    def __init__(self, quota, refill_rate, reap_interval=1.0):
        self.capacity = quota
        self.tokens = quota
        self.refill_rate = refill_rate  # GPU-hours per second
        self.reap_interval = reap_interval

        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

        self.reservations = {}  # vm_id -> (gpu_count, hours, expires_at)

        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._reap_loop, args=(reap_interval,), daemon=True
        )
        self._thread.start()

    def _reap_loop(self, interval):
        while not self._stop.wait(interval):
            now = time.monotonic()
            with self.lock:
                self.refill()
                expired = [
                    vm for vm, (_, _, exp) in self.reservations.items() if now >= exp
                ]
                for vm in expired:
                    del self.reservations[vm]

    def stop(self):
        self._stop.set()
        self._thread.join(timeout=0.5)

    def refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate,
        )
        self.last_refill = now

    def allocate(self, vm_id, gpu_count, hours):
        cost = gpu_count * hours
        now = time.monotonic()

        with self.lock:
            self.refill()

            if vm_id in self.reservations:
                return False

            if self.tokens < cost:
                return False

            self.tokens -= cost
            self.reservations[vm_id] = (
                gpu_count,
                hours,
                now + hours * 3600,
            )
            return True

    def extend(self, vm_id, additional_hours):
        now = time.monotonic()

        with self.lock:
            self.refill()

            if vm_id not in self.reservations:
                return False

            gpu_count, reserved_hours, expires_at = self.reservations[vm_id]
            cost = gpu_count * additional_hours

            if self.tokens < cost:
                return False

            self.tokens -= cost
            self.reservations[vm_id] = (
                gpu_count,
                reserved_hours + additional_hours,
                expires_at + additional_hours * 3600,
            )
            return True

    def release(self, vm_id, actual_hours):
        with self.lock:
            self.refill()

            if vm_id not in self.reservations:
                return False

            gpu_count, reserved_hours, expires_at = self.reservations.pop(vm_id)
            reserved = gpu_count * reserved_hours
            actual = gpu_count * actual_hours

            if actual > reserved:
                self.reservations[vm_id] = (
                    gpu_count,
                    reserved_hours,
                    expires_at,
                )
                return False

            self.tokens = min(
                self.capacity,
                self.tokens + reserved - actual,
            )
            return True


if __name__ == "__main__":
    # Capacity = 100 GPU-hours, Refill = 10 GPU-hours per day
    bucket = GPUTokenBucket(quota=100, refill_rate=10 / 86400, reap_interval=0.1)

    try:
        # 1. Allocate 4 GPUs for 10 hours -> costs 40, remaining = 60
        print("Allocate vm1:", bucket.allocate("vm1", 4, 10), "Tokens:", bucket.tokens)

        # 2. Duplicate allocation fails
        print("Duplicate vm1:", bucket.allocate("vm1", 2, 2))

        # 3. Extend vm1 by 2 hours -> costs 8, remaining = 52
        print("Extend vm1:", bucket.extend("vm1", 2), "Tokens:", bucket.tokens)

        # 4. Reject release with more hours than reserved (12 > 12)
        print("Over-release vm1:", bucket.release("vm1", 13), "Tokens:", bucket.tokens)

        # 5. Release vm1 after 10 hours -> refunds 4 * (12 - 10) = 8, remaining = 60
        print("Release vm1:", bucket.release("vm1", 10), "Tokens:", bucket.tokens)

        # 6. Short-lived VM that expires via background reaper thread
        # Set expires_at to already in the past to test reap without waiting hours
        bucket.allocate("vm2", 2, 1)
        with bucket.lock:
            gpu, hrs, _ = bucket.reservations["vm2"]
            bucket.reservations["vm2"] = (gpu, hrs, time.monotonic() - 1)

        time.sleep(0.2)  # let background thread sweep
        print("vm2 still in reservations after expiry:", "vm2" in bucket.reservations)
    finally:
        bucket.stop()
