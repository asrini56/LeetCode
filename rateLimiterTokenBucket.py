
import time
import threading


class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill

        self.tokens = min(
            self.capacity,
            self.tokens + elapsed * self.refill_rate
        )

        self.last_refill = now

    def allow(self, cost=1):
        if cost <= 0:
            raise ValueError("Cost must be positive")

        if cost > self.capacity:
            return False

        with self.lock:
            self.refill()

            if self.tokens >= cost:
                self.tokens -= cost
                return True

            return False


class RateLimiter:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate

        self.buckets = {}
        self.lock = threading.Lock()

    def allow(self, tenant_id, cost=1):
        with self.lock:
            if tenant_id not in self.buckets:
                self.buckets[tenant_id] = TokenBucket(
                    self.capacity,
                    self.refill_rate
                )

            bucket = self.buckets[tenant_id]

        return bucket.allow(cost)

def test_basic():
    limiter = RateLimiter(
        capacity=3,
        refill_rate=1
    )

    assert limiter.allow("A") is True
    assert limiter.allow("A") is True
    assert limiter.allow("A") is True

    # Bucket is empty.
    assert limiter.allow("A") is False

    print("Basic test passed")

def test_tenant_isolation():
    limiter = RateLimiter(
        capacity=2,
        refill_rate=1
    )

    assert limiter.allow("A") is True
    assert limiter.allow("A") is True
    assert limiter.allow("A") is False

    # Tenant B has an independent bucket.
    assert limiter.allow("B") is True

    print("Tenant isolation passed")
