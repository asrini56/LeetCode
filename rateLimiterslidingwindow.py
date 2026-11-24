
import time
import threading
from collections import defaultdict, deque

class SlidingWindowRateLimiter:
    def __init__(self, limit, window_seconds):
        self.limit = limit
        self.window = window_seconds

        self.requests = defaultdict(deque)
        self.lock = threading.Lock()

    def allow(self, tenant_id):
        now = time.monotonic()

        with self.lock:
            timestamps = self.requests[tenant_id]

            # Remove expired requests.
            while timestamps and timestamps[0] <= now - self.window:
                timestamps.popleft()

            # Check limit.
            if len(timestamps) >= self.limit:
                return False

            # Record current request.
            timestamps.append(now)

            return True



def test_sliding_window():
    limiter = SlidingWindowRateLimiter(
        limit=3,
        window_seconds=2
    )

    # First 3 requests succeed.
    assert limiter.allow("A")
    assert limiter.allow("A")
    assert limiter.allow("A")

    # Fourth request rejected.
    assert not limiter.allow("A")

    # Another tenant has independent limit.
    assert limiter.allow("B")

    # Wait for old requests to expire.
    time.sleep(2.1)

    assert limiter.allow("A")

    print("Sliding window tests passed!")


test_sliding_window()
