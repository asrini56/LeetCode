
import time
import threading
from collections import defaultdict, deque


class GPUSlidingWindow:
    def __init__(self, quota, window_seconds):
        self.quota = quota
        self.window = window_seconds

        # tenant -> deque of (timestamp, gpu_hours)
        self.usage = defaultdict(deque)

        self.lock = threading.Lock()

    def allocate(self, tenant_id, gpu_count, hours):
        if gpu_count <= 0 or hours <= 0:
            raise ValueError("Invalid allocation")

        now = time.monotonic()
        cost = gpu_count * hours

        with self.lock:
            records = self.usage[tenant_id]

            # Remove expired allocations.
            while records and records[0][0] <= now - self.window:
                records.popleft()

            # Calculate current usage.
            used = sum(amount for _, amount in records)

            # Check quota.
            if used + cost > self.quota:
                return False

            # Record allocation.
            records.append((now, cost))

            return True

    def get_usage(self, tenant_id):
        now = time.monotonic()

        with self.lock:
            records = self.usage[tenant_id]

            while records and records[0][0] <= now - self.window:
                records.popleft()

            return sum(amount for _, amount in records)



def test_gpu_sliding_window():
    manager = GPUSlidingWindow(
        quota=100,
        window_seconds=2
    )

    # 4 GPUs * 5 hours = 20
    assert manager.allocate("A", 4, 5)
    assert manager.get_usage("A") == 20

    # 2 GPUs * 10 hours = 20
    assert manager.allocate("A", 2, 10)
    assert manager.get_usage("A") == 40

    # 8 GPUs * 10 hours = 80
    # Total would be 120, so reject.
    assert not manager.allocate("A", 8, 10)

    # Tenant B has independent quota.
    assert manager.allocate("B", 8, 10)

    # Wait for previous allocations to expire.
    time.sleep(2.1)

    assert manager.get_usage("A") == 0
    assert manager.allocate("A", 8, 10)

    print("All GPU sliding-window tests passed!")


test_gpu_sliding_window()
